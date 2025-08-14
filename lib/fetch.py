"""Fetch ASCII art from OpenAI API"""

import os
import openai
from typing import Optional, Dict
from dotenv import load_dotenv

class ArtFetcher:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the ArtFetcher with configuration"""
        if config_path:
            load_dotenv(config_path)
        else:
            load_dotenv()
        
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        self.style = os.getenv('ASCII_STYLE', 'retro computer terminal')
        self.width = int(os.getenv('ASCII_WIDTH', '80'))
        self.height = int(os.getenv('ASCII_HEIGHT', '24'))
        self.theme = os.getenv('THEME', 'cyberpunk')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        openai.api_key = self.api_key
    
    def fetch_art(self, prompt: Optional[str] = None) -> Dict[str, str]:
        """Fetch ASCII art from OpenAI"""
        if not prompt:
            prompt = self._generate_prompt()
        
        try:
            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an ASCII artist. Create ASCII art that fits within the specified dimensions. Use only ASCII characters. Do not include any explanation or markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=2000
            )
            
            art = response.choices[0].message.content
            
            # Ensure art fits within dimensions
            lines = art.split('\n')
            lines = lines[:self.height]
            lines = [line[:self.width] for line in lines]
            art = '\n'.join(lines)
            
            return {
                'art': art,
                'prompt': prompt,
                'theme': self.theme,
                'style': self.style
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch art from OpenAI: {str(e)}")
    
    def _generate_prompt(self) -> str:
        """Generate a random prompt based on theme and style"""
        prompts = {
            'cyberpunk': [
                "Create ASCII art of a futuristic city skyline with neon signs",
                "Draw an ASCII robot or android face",
                "Create ASCII art of a cyberpunk hacker terminal",
                "Draw ASCII art of digital rain like in The Matrix"
            ],
            'nature': [
                "Create ASCII art of a mountain landscape",
                "Draw an ASCII tree with detailed branches",
                "Create ASCII art of ocean waves",
                "Draw ASCII art of a sunset or sunrise"
            ],
            'abstract': [
                "Create abstract geometric ASCII patterns",
                "Draw ASCII art with fractal-like patterns",
                "Create ASCII art with flowing organic shapes",
                "Draw ASCII mandala or kaleidoscope pattern"
            ],
            'retro': [
                "Create ASCII art of a retro computer terminal",
                "Draw ASCII art of an old-school arcade game screen",
                "Create ASCII art with 80s aesthetic",
                "Draw ASCII art of a vintage robot"
            ],
            'space': [
                "Create ASCII art of a spaceship",
                "Draw ASCII art of planets and stars",
                "Create ASCII art of an astronaut",
                "Draw ASCII art of a galaxy or nebula"
            ],
            'fantasy': [
                "Create ASCII art of a dragon",
                "Draw ASCII art of a castle",
                "Create ASCII art of a wizard or mage",
                "Draw ASCII art of a magical forest"
            ]
        }
        
        import random
        theme_prompts = prompts.get(self.theme, prompts['cyberpunk'])
        base_prompt = random.choice(theme_prompts)
        
        return f"{base_prompt}. Style: {self.style}. Maximum width: {self.width} characters. Maximum height: {self.height} lines. Use creative ASCII characters and ensure the art is visually interesting."