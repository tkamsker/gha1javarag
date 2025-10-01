"""
Upsert module for managing data insertion into Weaviate.
Handles batch processing, retry logic, and error handling.
"""

import time
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging


class UpsertManager:
    """Manages data upsertion to Weaviate with retry logic and error handling."""
    
    def __init__(self, config, weaviate_client, reporting_manager):
        """Initialize upsert manager."""
        self.config = config
        self.weaviate_client = weaviate_client
        self.reporting = reporting_manager
        self.logger = logging.getLogger(__name__)
        
        # Retry configuration
        self.max_retries = config.max_retries
        self.retry_delay = 1  # Initial delay in seconds
        self.max_retry_delay = 60  # Maximum delay in seconds
        
        # Dead letter queue for failed upserts
        self.dead_letter_file = Path(config.output_dir) / 'logs' / 'bad_upserts.jsonl'
        self.dead_letter_file.parent.mkdir(parents=True, exist_ok=True)
    
    def upsert_chunks_batch(self, chunks: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
        """Upsert a batch of chunks with retry logic."""
        if not chunks:
            return {'success': True, 'count': 0, 'errors': []}
        
        attempt = 0
        errors = []
        
        while attempt <= self.max_retries:
            try:
                result = self.weaviate_client.upsert_chunks(chunks, collection_name)
                
                if result['success']:
                    self.logger.debug(f"Successfully upserted {result['count']} chunks to {collection_name}")
                    return result
                else:
                    errors.extend(result.get('errors', []))
                    self.logger.warning(f"Upsert attempt {attempt + 1} failed: {result['errors']}")
            
            except Exception as e:
                error_msg = str(e)
                errors.append(error_msg)
                self.logger.warning(f"Upsert attempt {attempt + 1} failed with exception: {error_msg}")
            
            attempt += 1
            
            if attempt <= self.max_retries:
                # Calculate delay with exponential backoff
                delay = min(self.retry_delay * (2 ** (attempt - 1)), self.max_retry_delay)
                self.logger.info(f"Retrying in {delay} seconds... (attempt {attempt + 1}/{self.max_retries + 1})")
                time.sleep(delay)
        
        # All retries failed, move to dead letter queue
        self._move_to_dead_letter_queue(chunks, collection_name, errors)
        
        return {
            'success': False,
            'count': 0,
            'errors': errors
        }
    
    def upsert_chunks_with_splitting(self, chunks: List[Dict[str, Any]], collection_name: str) -> Dict[str, Any]:
        """Upsert chunks with automatic batch splitting on failure."""
        if not chunks:
            return {'success': True, 'count': 0, 'errors': []}
        
        # Try to upsert the full batch first
        result = self.upsert_chunks_batch(chunks, collection_name)
        
        if result['success']:
            return result
        
        # If full batch failed, try splitting into smaller batches
        self.logger.info(f"Full batch failed, splitting {len(chunks)} chunks into smaller batches")
        
        batch_size = len(chunks) // 2
        if batch_size < 1:
            batch_size = 1
        
        total_success = 0
        all_errors = []
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_result = self.upsert_chunks_batch(batch, collection_name)
            
            if batch_result['success']:
                total_success += batch_result['count']
            else:
                all_errors.extend(batch_result.get('errors', []))
                
                # If even the smaller batch failed, try individual chunks
                if len(batch) > 1:
                    self.logger.info(f"Batch of {len(batch)} chunks failed, trying individual chunks")
                    
                    for chunk in batch:
                        individual_result = self.upsert_chunks_batch([chunk], collection_name)
                        if individual_result['success']:
                            total_success += individual_result['count']
                        else:
                            all_errors.extend(individual_result.get('errors', []))
                            self._move_to_dead_letter_queue([chunk], collection_name, individual_result.get('errors', []))
        
        return {
            'success': total_success > 0,
            'count': total_success,
            'errors': all_errors
        }
    
    def _move_to_dead_letter_queue(self, chunks: List[Dict[str, Any]], collection_name: str, errors: List[str]):
        """Move failed chunks to dead letter queue."""
        try:
            dead_letter_entry = {
                'timestamp': time.time(),
                'collection': collection_name,
                'chunk_count': len(chunks),
                'errors': errors,
                'chunks': chunks
            }
            
            with open(self.dead_letter_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(dead_letter_entry) + '\n')
            
            self.logger.warning(f"Moved {len(chunks)} failed chunks to dead letter queue: {self.dead_letter_file}")
        
        except Exception as e:
            self.logger.error(f"Error writing to dead letter queue: {e}")
    
    def retry_dead_letter_queue(self) -> Dict[str, Any]:
        """Retry processing chunks from dead letter queue."""
        if not self.dead_letter_file.exists():
            return {'success': True, 'retried': 0, 'errors': []}
        
        retried = 0
        errors = []
        
        try:
            # Read dead letter entries
            with open(self.dead_letter_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Process each entry
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    chunks = entry.get('chunks', [])
                    collection = entry.get('collection', '')
                    
                    if chunks and collection:
                        result = self.upsert_chunks_batch(chunks, collection)
                        if result['success']:
                            retried += result['count']
                        else:
                            errors.extend(result.get('errors', []))
                
                except json.JSONDecodeError as e:
                    self.logger.error(f"Error parsing dead letter entry: {e}")
                    continue
            
            # Clear dead letter queue if all retries were successful
            if not errors:
                self.dead_letter_file.unlink()
                self.logger.info("Cleared dead letter queue after successful retries")
            
            return {
                'success': len(errors) == 0,
                'retried': retried,
                'errors': errors
            }
        
        except Exception as e:
            self.logger.error(f"Error processing dead letter queue: {e}")
            return {
                'success': False,
                'retried': retried,
                'errors': [str(e)]
            }
    
    def get_upsert_statistics(self) -> Dict[str, Any]:
        """Get statistics about upsert operations."""
        stats = {
            'dead_letter_queue_size': 0,
            'dead_letter_file_exists': self.dead_letter_file.exists()
        }
        
        if self.dead_letter_file.exists():
            try:
                with open(self.dead_letter_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                stats['dead_letter_queue_size'] = len(lines)
                
                # Count chunks in dead letter queue
                total_chunks = 0
                for line in lines:
                    try:
                        entry = json.loads(line.strip())
                        total_chunks += entry.get('chunk_count', 0)
                    except json.JSONDecodeError:
                        continue
                
                stats['dead_letter_chunks'] = total_chunks
            
            except Exception as e:
                self.logger.error(f"Error reading dead letter queue statistics: {e}")
                stats['error'] = str(e)
        
        return stats
    
    def cleanup_dead_letter_queue(self, max_age_hours: int = 24):
        """Clean up old entries from dead letter queue."""
        if not self.dead_letter_file.exists():
            return
        
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            # Read all entries
            with open(self.dead_letter_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Filter out old entries
            recent_entries = []
            for line in lines:
                try:
                    entry = json.loads(line.strip())
                    entry_time = entry.get('timestamp', 0)
                    
                    if current_time - entry_time < max_age_seconds:
                        recent_entries.append(line)
                
                except json.JSONDecodeError:
                    continue
            
            # Write back recent entries
            with open(self.dead_letter_file, 'w', encoding='utf-8') as f:
                f.writelines(recent_entries)
            
            cleaned_count = len(lines) - len(recent_entries)
            if cleaned_count > 0:
                self.logger.info(f"Cleaned up {cleaned_count} old entries from dead letter queue")
        
        except Exception as e:
            self.logger.error(f"Error cleaning up dead letter queue: {e}")
