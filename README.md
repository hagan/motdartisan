# MOTD Artisan

Message of the Day Artisan - A shell module that displays beautiful ASCII art on terminal login using OpenAI's API.

## Features

- Generates ASCII art using OpenAI API
- Caches art locally to minimize API calls
- Rotates through cached art on each login
- Configurable themes and styles
- Easy integration with shell startup

## Installation

### As a Git Submodule

```bash
cd ~/.config
git submodule add https://github.com/yourusername/motdartisan.git
git submodule init
git submodule update
```

### Dependencies

```bash
pip install openai requests python-dotenv
```

### Configuration

1. Copy `config.example` to `.env` and add your OpenAI API key:
```bash
cp config.example .env
# Edit .env and add your API key
```

2. Add to your shell startup (~/.config/zsh/.zshrc):
```bash
# MOTD Artisan
if [[ -f "$HOME/.config/motdartisan/motdartisan.sh" ]]; then
    source "$HOME/.config/motdartisan/motdartisan.sh"
fi
```

## Usage

The module will automatically display ASCII art on login. 

### Manual Commands

- `motd-fetch` - Fetch new ASCII art from OpenAI
- `motd-show` - Display random cached art
- `motd-clear` - Clear the art cache
- `motd-list` - List cached art pieces

## Configuration Options

Edit the `.env` file to customize:

### Required Settings
- `OPENAI_API_KEY` - Your OpenAI API key (required)
  - Get one from https://platform.openai.com/api-keys

### Art Generation Settings
- `OPENAI_MODEL` - Model to use (default: `"gpt-4"`)
  - Options: `"gpt-4"`, `"gpt-3.5-turbo"`
  
- `ASCII_STYLE` - Art style descriptor (default: `"detailed ASCII art"`)
  - **Recommended for actual art:**
    - `"detailed ASCII art"` - High-quality ASCII art
    - `"block ASCII art"` - Uses block characters (█ ▀ ▄)
    - `"line art ASCII"` - Uses line characters (─ │ ┌ ┐)
    - `"shaded ASCII art"` - Uses shading (░ ▒ ▓)
    - `"classic ASCII art"` - Traditional ASCII
    - `"minimalist ASCII"` - Simple, clean designs
  - **To avoid text/fonts:**
    - `"pictorial ASCII art, no text or fonts"`
    - `"visual ASCII art scene, avoid letters"`
  
- `THEME` - Content theme (default: `"cyberpunk"`)
  - Options: `"cyberpunk"`, `"nature"`, `"abstract"`, `"retro"`, `"space"`, `"fantasy"`
  - Each theme has different prompt variations

### Display Settings  
- `ASCII_WIDTH` - Max width in characters (default: `80`)
  - Standard terminal width, adjust for your terminal
  
- `ASCII_HEIGHT` - Max height in lines (default: `24`)  
  - Adjust based on terminal size and preference

- `DISPLAY_COLOR` - Enable colored output (default: `true`)
  - Set to `false` for monochrome terminals
  
- `RANDOM_COLOR` - Use random colors each time (default: `false`)
  - When `true`, ignores theme colors

### Cache Settings
- `CACHE_SIZE` - Number of art pieces to cache (default: `10`)
  - Higher values = more variety, more disk space
  
- `AUTO_FETCH` - Fetch new art if cache empty (default: `true`)
  - Set to `false` to prevent automatic API calls

## Directory Structure

```
ascii-login/
├── README.md
├── config.example      # Example configuration
├── .env               # Your config (gitignored)
├── requirements.txt   # Python dependencies
├── ascii-login.sh     # Shell wrapper script
├── cache/             # Cached ASCII art (gitignored)
├── lib/
│   ├── __init__.py
│   ├── fetch.py       # OpenAI API interaction
│   ├── display.py     # Display logic
│   └── cache.py       # Cache management
└── main.py            # Main entry point
```

## License

MIT