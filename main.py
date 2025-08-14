#!/usr/bin/env python3
"""Main entry point for MOTD Artisan"""

import click
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

from lib import ArtFetcher, ArtCache, ArtDisplay

# Load environment variables
env_file = Path(__file__).parent / '.env'
if env_file.exists():
    load_dotenv(env_file)

@click.group()
def cli():
    """MOTD Artisan - Display beautiful ASCII art as Message of the Day"""
    pass

@cli.command()
@click.option('--prompt', '-p', help='Custom prompt for art generation')
def fetch(prompt):
    """Fetch new ASCII art from OpenAI"""
    try:
        fetcher = ArtFetcher()
        cache = ArtCache()
        
        click.echo("Fetching new ASCII art from OpenAI...")
        art_data = fetcher.fetch_art(prompt)
        
        art_id = cache.save_art(art_data)
        click.echo(f"Art saved with ID: {art_id}")
        
        # Display the fetched art
        display = ArtDisplay()
        display.display(art_data['art'], theme=art_data.get('theme'))
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.option('--id', '-i', help='Display specific art by ID')
@click.option('--border', '-b', is_flag=True, help='Display with border')
@click.option('--center', '-c', is_flag=True, help='Center the art')
def show(id, border, center):
    """Display random cached ASCII art"""
    try:
        cache = ArtCache()
        display = ArtDisplay()
        
        # Check if cache is empty and auto-fetch if configured
        if cache.is_empty() and os.getenv('AUTO_FETCH', 'true').lower() == 'true':
            click.echo("Cache is empty, fetching new art...", err=True)
            fetcher = ArtFetcher()
            art_data = fetcher.fetch_art()
            cache.save_art(art_data)
        
        # Get art from cache
        if id:
            art = cache.get_art_by_id(id)
            if not art:
                click.echo(f"Art with ID {id} not found", err=True)
                sys.exit(1)
        else:
            art = cache.get_random_art()
            if not art:
                click.echo("No art in cache. Run 'fetch' to get some!", err=True)
                sys.exit(1)
        
        # Display the art
        theme = os.getenv('THEME', 'cyberpunk')
        
        if border:
            display.display_with_border(art)
        elif center:
            display.print_centered(art)
        else:
            display.display(art, theme=theme)
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
def list():
    """List all cached ASCII art"""
    try:
        cache = ArtCache()
        items = cache.list_cached_art()
        
        if not items:
            click.echo("No art in cache")
            return
        
        click.echo(f"Cached ASCII Art ({len(items)} items):")
        click.echo("-" * 50)
        
        for item in items:
            click.echo(f"ID: {item['id']}")
            click.echo(f"  Created: {item['created']}")
            click.echo(f"  Theme: {item.get('theme', 'N/A')}")
            click.echo(f"  Style: {item.get('style', 'N/A')}")
            if item.get('prompt'):
                click.echo(f"  Prompt: {item['prompt'][:50]}...")
            click.echo()
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
@click.confirmation_option(prompt='Are you sure you want to clear the cache?')
def clear():
    """Clear all cached ASCII art"""
    try:
        cache = ArtCache()
        cache.clear_cache()
        click.echo("Cache cleared successfully")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

@cli.command()
def login():
    """Display art for login (used by shell integration)"""
    try:
        cache = ArtCache()
        display = ArtDisplay()
        
        # Silent mode - only output art, no messages
        art = cache.get_random_art()
        
        if art:
            theme = os.getenv('THEME', 'cyberpunk')
            display.display(art, theme=theme)
        # If no art, fail silently for login
        
    except:
        # Fail silently on login to not disrupt shell startup
        pass

if __name__ == '__main__':
    cli()