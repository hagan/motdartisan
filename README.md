# MOTD Artisan

Message of the Day Artisan - A shell module that displays beautiful ASCII and Unicode art on terminal login using OpenAI's API.

## Features

- Generates ASCII and Unicode art using OpenAI API
- Supports traditional ASCII, Japanese characters, Braille patterns, and emoji art
- Caches art locally to minimize API calls
- Rotates through cached art on each login
- Configurable themes and styles (cyberpunk, fantasy, nature, etc.)
- ZSH and Bash compatible
- Easy integration with shell startup

## Installation

### As a Git Submodule

```bash
cd ~/.config
git submodule add https://github.com/hagan/motdartisan.git
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
  - Use `-p "custom prompt"` for specific requests
- `motd-show` - Display random cached art
  - Use `-i ID` to show specific art
  - Use `-b` for bordered display
  - Use `-c` for centered display
- `motd-import FILE` - Import custom ASCII art from file
  - Use `-i ID` to set custom ID (default: auto-generated)
  - Use `-d "description"` to add description
  - Use `-t theme` to set theme (default: custom)
  - Use `-s style` to set style (default: ASCII art)
- `motd-delete ID` - Delete specific art by ID
  - Shows preview before deletion
  - Use `-f` to skip confirmation
- `motd-clear` - Clear ALL art from cache (requires confirmation)
- `motd-list` - List cached art pieces with metadata

## Configuration Options

Edit the `.env` file to customize:

### Required Settings
- `OPENAI_API_KEY` - Your OpenAI API key (required)
  - Get one from https://platform.openai.com/api-keys

### Art Generation Settings
- `OPENAI_MODEL` - Model to use (default: `"gpt-4"`)
  - Options: `"gpt-4"`, `"gpt-3.5-turbo"`
  
- `ASCII_STYLE` - Art style descriptor (default: `"detailed ASCII art"`)
  - **Traditional ASCII styles:**
    - `"detailed ASCII art"` - High-quality ASCII art
    - `"block ASCII art"` - Uses block characters (█ ▀ ▄)
    - `"line art ASCII"` - Uses line characters (─ │ ┌ ┐)
    - `"shaded ASCII art"` - Uses shading (░ ▒ ▓)
    - `"classic ASCII art"` - Traditional ASCII
    - `"minimalist ASCII"` - Simple, clean designs
  - **Unicode styles (more detailed, photo-like):**
    - `"unicode art"` - Mixed Unicode characters for detail
    - `"japanese unicode art"` - Uses Japanese characters (あ漢字カナ) for texture
    - `"dense unicode patterns"` - Complex Unicode symbols
    - `"braille art"` - Braille patterns for grayscale effects (⠿⡿⣿)
    - `"emoji art"` - Creative emoji combinations 🎨
  - **To avoid text/fonts:**
    - `"pictorial ASCII art, no text or fonts"`
    - `"visual art scene, avoid letters"`
  
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

## Examples

### Using Different Art Styles

```bash
# Traditional ASCII art
ASCII_STYLE="detailed ASCII art"

# Japanese characters for texture (creates photo-like effects)
ASCII_STYLE="japanese unicode art"

# Braille patterns for grayscale-like images
ASCII_STYLE="braille art"

# Emoji art for colorful representations
ASCII_STYLE="emoji art"

# Block characters for solid shapes
ASCII_STYLE="block ASCII art"
```

### Custom Fetching

```bash
# Fetch with specific style request
motd-fetch -p "Create a cyberpunk city using dense Unicode patterns"

# Fetch Japanese-style art
motd-fetch -p "Create art using Japanese kanji 龍火山水風 and hiragana あいうえお"

# Fetch emoji art
motd-fetch -p "Create a sunset scene using only emoji characters 🌅🌊🏖️"
```

### Display and Management

```bash
# Show specific art by ID
motd-show -i 392c621a

# Show with decorative border
motd-show -b

# Center the art on screen
motd-show -c

# List all cached art with IDs
motd-list

# Delete specific art by ID (with confirmation)
motd-delete 392c621a

# Delete without confirmation
motd-delete -f 392c621a

# Clear entire cache (with confirmation)
motd-clear
```

## Adding Custom ASCII Art

### Easy Method: Using Import Command

```bash
# Import with auto-generated ID
motd-import myart.txt

# Import with custom ID and description
motd-import myart.txt -i company_logo -d "Company ASCII logo"

# Import with full metadata
motd-import myart.txt -i mylogo -d "Custom logo" -t corporate -s "ANSI color art"
```

### Manual Method

You can also add art files directly to the cache:

1. **Create your ASCII art file** in `cache/` directory:
   ```bash
   vim ~/.config/motdartisan/cache/myart.txt
   ```

2. **Create a metadata JSON file** with the same ID:
   ```json
   {
     "id": "myart",
     "created": "2025-08-13T20:48:00.000000",
     "prompt": "Description of your art",
     "theme": "custom",
     "style": "ASCII art"
   }
   ```

3. **Update cache/metadata.json** - add your entry to the "items" array

Your custom art will now appear in `motd-list` and can be displayed with `motd-show -i myart`.

**Supported formats:**
- Plain ASCII text
- ANSI color codes (for colored art)
- Unicode characters
- Emoji art

## Directory Structure

```
motdartisan/
├── README.md
├── config.example      # Example configuration
├── .env               # Your config (gitignored)
├── requirements.txt   # Python dependencies
├── motdartisan.sh     # Shell wrapper script (ZSH/Bash compatible)
├── cache/             # Cached ASCII art (gitignored)
├── lib/
│   ├── __init__.py
│   ├── fetch.py       # OpenAI API interaction with Unicode support
│   ├── display.py     # Display logic with color themes
│   └── cache.py       # Cache management
└── main.py            # Main CLI entry point
```

## License

MIT