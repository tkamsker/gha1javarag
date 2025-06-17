import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(level=logging.DEBUG):
    """Configure logging for the application"""
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Create a log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"java_analysis_{timestamp}.log"
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also output to console
        ]
    )
    
    # Create logger for this application
    logger = logging.getLogger('java_analysis')
    logger.setLevel(level)
    
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger 