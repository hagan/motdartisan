"""Display ASCII art with optional colors and effects"""

import os
import sys
import random
from typing import Optional

class ArtDisplay:
    def __init__(self):
        """Initialize the ArtDisplay with configuration"""
        self.use_color = os.getenv('DISPLAY_COLOR', 'true').lower() == 'true'
        self.random_color = os.getenv('RANDOM_COLOR', 'false').lower() == 'true'
        
        # ANSI color codes
        self.colors = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'magenta': '\033[35m',
            'cyan': '\033[36m',
            'white': '\033[37m',
            'bright_black': '\033[90m',
            'bright_red': '\033[91m',
            'bright_green': '\033[92m',
            'bright_yellow': '\033[93m',
            'bright_blue': '\033[94m',
            'bright_magenta': '\033[95m',
            'bright_cyan': '\033[96m',
            'bright_white': '\033[97m',
            'reset': '\033[0m'
        }
        
        # Theme color schemes
        self.themes = {
            'cyberpunk': ['cyan', 'magenta', 'bright_blue', 'bright_magenta'],
            'nature': ['green', 'bright_green', 'yellow', 'bright_yellow'],
            'retro': ['bright_cyan', 'bright_magenta', 'bright_yellow', 'white'],
            'space': ['blue', 'bright_blue', 'white', 'bright_white'],
            'abstract': ['red', 'yellow', 'blue', 'green', 'magenta', 'cyan'],
            'fantasy': ['bright_magenta', 'bright_cyan', 'bright_yellow', 'bright_blue'],
            'monochrome': ['white', 'bright_white', 'bright_black']
        }
    
    def display(self, art: str, theme: Optional[str] = None, clear_screen: bool = False):
        """Display ASCII art with optional colors"""
        if clear_screen:
            self._clear_screen()
        
        if not self.use_color:
            print(art)
            return
        
        # Choose color scheme
        if self.random_color:
            color = random.choice(list(self.colors.keys())[:-1])  # Exclude 'reset'
            colored_art = f"{self.colors[color]}{art}{self.colors['reset']}"
        elif theme and theme in self.themes:
            colored_art = self._apply_theme_colors(art, theme)
        else:
            # Default cyan color for terminal aesthetic
            colored_art = f"{self.colors['cyan']}{art}{self.colors['reset']}"
        
        print(colored_art)
    
    def _apply_theme_colors(self, art: str, theme: str) -> str:
        """Apply theme-based gradient colors to art"""
        lines = art.split('\n')
        theme_colors = self.themes[theme]
        colored_lines = []
        
        # Apply gradient effect
        for i, line in enumerate(lines):
            if line.strip():  # Only color non-empty lines
                # Cycle through theme colors
                color_index = i % len(theme_colors)
                color_name = theme_colors[color_index]
                colored_line = f"{self.colors[color_name]}{line}{self.colors['reset']}"
                colored_lines.append(colored_line)
            else:
                colored_lines.append(line)
        
        return '\n'.join(colored_lines)
    
    def display_with_border(self, art: str, border_char: str = '='):
        """Display ASCII art with a border"""
        lines = art.split('\n')
        max_width = max(len(line) for line in lines) if lines else 0
        
        border = border_char * (max_width + 4)
        
        print(border)
        for line in lines:
            print(f"{border_char} {line.ljust(max_width)} {border_char}")
        print(border)
    
    def _clear_screen(self):
        """Clear the terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def print_centered(self, art: str):
        """Print ASCII art centered in terminal"""
        try:
            # Get terminal size
            columns = os.get_terminal_size().columns
            
            lines = art.split('\n')
            for line in lines:
                padding = (columns - len(line)) // 2
                print(' ' * padding + line)
        except:
            # Fallback to normal print if terminal size can't be determined
            print(art)