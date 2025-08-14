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

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `OPENAI_MODEL` - Model to use (default: "gpt-4")
- `ASCII_STYLE` - Art style (default: "retro computer terminal")
- `ASCII_WIDTH` - Max width in characters (default: 80)
- `ASCII_HEIGHT` - Max height in lines (default: 24)
- `CACHE_SIZE` - Number of art pieces to cache (default: 10)
- `AUTO_FETCH` - Fetch new art if cache is empty (default: true)
- `THEME` - Theme for art generation (default: "cyberpunk")

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