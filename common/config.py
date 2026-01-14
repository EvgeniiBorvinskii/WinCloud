"""
Configuration Manager for WinCloud
"""
import os
import json
from typing import Any, Dict

class Config:
    """Configuration manager"""
    
    def __init__(self):
        self.config_file = os.path.join(
            os.path.expanduser('~'),
            '.wincloud',
            'config.json'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        # Default configuration
        default_config = {
            'server_url': 'http://5.249.160.54:8443',
            'api_version': 'v1',
            'compression_level': 9,
            'split_ratio': {
                'local': 10,
                'cloud': 90
            },
            'encryption': {
                'algorithm': 'AES-256',
                'enabled': True
            },
            'network': {
                'timeout': 30,
                'max_retries': 3,
                'chunk_size': 5242880  # 5MB
            },
            'ui': {
                'theme': 'dark',  # 'dark' or 'light'
                'language': 'en',
                'opacity': 1.0,  # Window opacity (0.0 - 1.0)
                'background_transparency': False  # Enable/disable transparent background
            }
        }
        
        # Try to load from file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception:
                pass
        else:
            # Create config directory and file
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            self._save_config(default_config)
        
        return default_config
    
    def _save_config(self, config: Dict):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception:
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, *args):
        """Set configuration value - supports both set(key, value) and set(section, key, value)"""
        if len(args) == 2:
            # set(key, value)
            key, value = args
            keys = key.split('.')
            config = self.config
            
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            config[keys[-1]] = value
        elif len(args) == 3:
            # set(section, key, value)
            section, key, value = args
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
        else:
            raise ValueError("set() takes 2 or 3 arguments")
        
        self._save_config(self.config)
    
    def save(self):
        """Save current configuration"""
        self._save_config(self.config)
