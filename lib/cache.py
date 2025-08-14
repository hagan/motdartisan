"""Cache management for ASCII art"""

import os
import json
import random
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class ArtCache:
    def __init__(self, cache_dir: str = None):
        """Initialize the ArtCache with a cache directory"""
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path(__file__).parent.parent / 'cache'
        
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_size = int(os.getenv('CACHE_SIZE', '10'))
        self.metadata_file = self.cache_dir / 'metadata.json'
        self._load_metadata()
    
    def _load_metadata(self):
        """Load cache metadata"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {
                'items': [],
                'last_updated': None
            }
    
    def _save_metadata(self):
        """Save cache metadata"""
        self.metadata['last_updated'] = datetime.now().isoformat()
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
    
    def save_art(self, art_data: Dict[str, str]) -> str:
        """Save ASCII art to cache"""
        # Generate unique ID for the art
        art_id = hashlib.md5(art_data['art'].encode()).hexdigest()[:8]
        
        # Save art file
        art_file = self.cache_dir / f"{art_id}.txt"
        with open(art_file, 'w') as f:
            f.write(art_data['art'])
        
        # Save art metadata
        meta_file = self.cache_dir / f"{art_id}.json"
        metadata = {
            'id': art_id,
            'created': datetime.now().isoformat(),
            'prompt': art_data.get('prompt', ''),
            'theme': art_data.get('theme', ''),
            'style': art_data.get('style', '')
        }
        with open(meta_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        # Update cache metadata
        self.metadata['items'].append({
            'id': art_id,
            'created': metadata['created']
        })
        
        # Maintain cache size limit
        while len(self.metadata['items']) > self.cache_size:
            oldest = self.metadata['items'].pop(0)
            self._remove_art(oldest['id'])
        
        self._save_metadata()
        return art_id
    
    def get_random_art(self) -> Optional[str]:
        """Get a random ASCII art from cache"""
        if not self.metadata['items']:
            return None
        
        item = random.choice(self.metadata['items'])
        art_file = self.cache_dir / f"{item['id']}.txt"
        
        if art_file.exists():
            with open(art_file, 'r') as f:
                return f.read()
        return None
    
    def get_art_by_id(self, art_id: str) -> Optional[str]:
        """Get specific ASCII art by ID"""
        art_file = self.cache_dir / f"{art_id}.txt"
        if art_file.exists():
            with open(art_file, 'r') as f:
                return f.read()
        return None
    
    def list_cached_art(self) -> List[Dict]:
        """List all cached art with metadata"""
        result = []
        for item in self.metadata['items']:
            meta_file = self.cache_dir / f"{item['id']}.json"
            if meta_file.exists():
                with open(meta_file, 'r') as f:
                    result.append(json.load(f))
        return result
    
    def _remove_art(self, art_id: str):
        """Remove art from cache"""
        art_file = self.cache_dir / f"{art_id}.txt"
        meta_file = self.cache_dir / f"{art_id}.json"
        
        if art_file.exists():
            art_file.unlink()
        if meta_file.exists():
            meta_file.unlink()
    
    def clear_cache(self):
        """Clear all cached art"""
        for item in self.metadata['items']:
            self._remove_art(item['id'])
        
        self.metadata = {
            'items': [],
            'last_updated': None
        }
        self._save_metadata()
    
    def is_empty(self) -> bool:
        """Check if cache is empty"""
        return len(self.metadata['items']) == 0
    
    def size(self) -> int:
        """Get number of items in cache"""
        return len(self.metadata['items'])