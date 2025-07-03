import os
import yaml
from typing import Dict, Any
try:
    from rate_limiter import RateLimitConfig
except ImportError:
    from .rate_limiter import RateLimitConfig

def load_rate_limit_config(environment: str = None) -> RateLimitConfig:
    """Load rate limiting configuration from YAML file"""
    
    # Default to production if no environment specified
    if environment is None:
        environment = os.getenv('RATE_LIMIT_ENV', 'production')
    
    config_file = os.path.join('config', 'rate_limiting.yaml')
    
    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if environment not in config_data:
            raise ValueError(f"Environment '{environment}' not found in config file")
        
        env_config = config_data[environment]
        
        return RateLimitConfig(
            requests_per_minute=env_config.get('requests_per_minute', 15),
            requests_per_hour=env_config.get('requests_per_hour', 800),
            delay_between_requests=env_config.get('delay_between_requests', 4.0),
            exponential_backoff_base=env_config.get('exponential_backoff_base', 2.0),
            max_retries=env_config.get('max_retries', 5),
            quota_exceeded_wait_time=env_config.get('quota_exceeded_wait_time', 3600)
        )
        
    except FileNotFoundError:
        print(f"Warning: Config file {config_file} not found. Using default settings.")
        return RateLimitConfig()
    except Exception as e:
        print(f"Warning: Error loading config: {e}. Using default settings.")
        return RateLimitConfig()

def get_ollama_config(environment: str = None) -> Dict[str, Any]:
    """Get Ollama-specific configuration from YAML file"""
    
    # Default to production if no environment specified
    if environment is None:
        environment = os.getenv('RATE_LIMIT_ENV', 'production')
    
    config_file = os.path.join('config', 'rate_limiting.yaml')
    
    try:
        with open(config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        
        if environment not in config_data:
            raise ValueError(f"Environment '{environment}' not found in config file")
        
        env_config = config_data[environment]
        
        return {
            'timeout': env_config.get('ollama_timeout', 120),
            'environment': environment
        }
        
    except FileNotFoundError:
        print(f"Warning: Config file {config_file} not found. Using default Ollama settings.")
        return {'timeout': 120, 'environment': 'default'}
    except Exception as e:
        print(f"Warning: Error loading Ollama config: {e}. Using default settings.")
        return {'timeout': 120, 'environment': 'default'}

def get_environment_config() -> Dict[str, Any]:
    """Get current environment configuration"""
    environment = os.getenv('RATE_LIMIT_ENV', 'production')
    
    configs = {
        'production': {
            'description': 'Conservative settings for production use',
            'requests_per_minute': 15,
            'requests_per_hour': 800,
            'delay_between_requests': 4.0,
            'ollama_timeout': 120
        },
        'test': {
            'description': 'Very conservative settings for testing',
            'requests_per_minute': 10,
            'requests_per_hour': 500,
            'delay_between_requests': 8.0,
            'ollama_timeout': 60
        },
        'development': {
            'description': 'More aggressive settings for development',
            'requests_per_minute': 20,
            'requests_per_hour': 1000,
            'delay_between_requests': 2.0,
            'ollama_timeout': 90
        },
        'emergency': {
            'description': 'Very restrictive settings for emergency situations',
            'requests_per_minute': 5,
            'requests_per_hour': 200,
            'delay_between_requests': 10.0,
            'ollama_timeout': 30
        }
    }
    
    return {
        'environment': environment,
        'config': configs.get(environment, configs['production'])
    } 