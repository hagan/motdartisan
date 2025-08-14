#!/usr/bin/env python3
"""Import custom ASCII art into MOTD Artisan cache"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime
import click

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--id', '-i', help='Custom ID for the art (default: auto-generated)')
@click.option('--description', '-d', default='Manually imported art', help='Description of the art')
@click.option('--theme', '-t', default='custom', help='Theme category')
@click.option('--style', '-s', default='ASCII art', help='Art style')
def import_art(file_path, id, description, theme, style):
    """Import a custom ASCII art file into the MOTD Artisan cache.
    
    Example:
        python import_art.py myart.txt --id mylogo --description "Company logo"
    """
    # Setup paths
    script_dir = Path(__file__).parent
    cache_dir = script_dir / 'cache'
    cache_dir.mkdir(exist_ok=True)
    
    # Read the art file
    with open(file_path, 'r') as f:
        art_content = f.read()
    
    # Generate ID if not provided
    if not id:
        # Use first 8 chars of MD5 hash
        id = hashlib.md5(art_content.encode()).hexdigest()[:8]
    
    # Validate ID (alphanumeric and underscores only)
    if not id.replace('_', '').isalnum():
        click.echo("Error: ID must be alphanumeric (underscores allowed)", err=True)
        sys.exit(1)
    
    # Check if ID already exists
    art_file = cache_dir / f"{id}.txt"
    if art_file.exists():
        click.echo(f"Error: Art with ID '{id}' already exists", err=True)
        sys.exit(1)
    
    # Save art file
    with open(art_file, 'w') as f:
        f.write(art_content)
    
    # Create metadata JSON
    metadata = {
        'id': id,
        'created': datetime.now().isoformat(),
        'prompt': description,
        'theme': theme,
        'style': style
    }
    
    meta_file = cache_dir / f"{id}.json"
    with open(meta_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Update main metadata file
    metadata_file = cache_dir / 'metadata.json'
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            main_metadata = json.load(f)
    else:
        main_metadata = {'items': [], 'last_updated': None}
    
    # Add new entry
    main_metadata['items'].append({
        'id': id,
        'created': metadata['created']
    })
    main_metadata['last_updated'] = datetime.now().isoformat()
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(main_metadata, f, indent=2)
    
    click.echo(f"✓ Successfully imported art with ID: {id}")
    click.echo(f"  File: {art_file}")
    click.echo(f"  Theme: {theme}")
    click.echo(f"  Style: {style}")
    click.echo(f"  Description: {description}")
    click.echo(f"\nYou can now use:")
    click.echo(f"  motd-show -i {id}")
    click.echo(f"  motd-delete {id}")

if __name__ == '__main__':
    import_art()