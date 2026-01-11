#!/usr/bin/env python3
"""
Sync local upload_history.json with archive.org data.

Features:
- Verify uploads exist on archive.org
- Fetch actual metadata from archive.org
- List all files in each item
- Export full archive data to JSON

Usage:
    python sync_archive.py                  # Sync and verify all items
    python sync_archive.py --fetch-all      # Fetch all items by creator
    python sync_archive.py --export         # Export full data to archive_items.json
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    import internetarchive as ia
except ImportError:
    print("Error: internetarchive not installed. Run: pip install internetarchive")
    exit(1)


# ============================================================
# Paths
# ============================================================

HISTORY_PATH = Path(__file__).parent / "upload_history.json"
ARCHIVE_ITEMS_PATH = Path(__file__).parent / "archive_items.json"


# ============================================================
# History Functions
# ============================================================

def load_history() -> dict:
    if HISTORY_PATH.exists():
        with open(HISTORY_PATH) as f:
            return json.load(f)
    return {}


def save_history(history: dict):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)


# ============================================================
# Archive.org Functions
# ============================================================

def get_item_details(identifier: str) -> dict | None:
    """Fetch full item details from archive.org."""
    try:
        item = ia.get_item(identifier)
        if not item.exists:
            return None

        metadata = item.metadata
        files = []

        for file in item.files:
            if file.get('format') in ['VBR MP3', 'MP3', '128Kbps MP3', 'MPEG-4 Audio']:
                files.append({
                    'name': file.get('name'),
                    'size': file.get('size'),
                    'format': file.get('format')
                })

        return {
            'identifier': identifier,
            'exists': True,
            'title': metadata.get('title', ''),
            'creator': metadata.get('creator', ''),
            'description': metadata.get('description', ''),
            'date': metadata.get('date', ''),
            'mediatype': metadata.get('mediatype', ''),
            'collection': metadata.get('collection', ''),
            'subject': metadata.get('subject', ''),
            'files': files,
            'file_count': len(files),
            'url': f'https://archive.org/details/{identifier}',
            'synced_at': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"  Error fetching {identifier}: {e}")
        return None


def search_by_creator(creator: str) -> list[str]:
    """Search archive.org for items by creator."""
    try:
        search = ia.search_items(f'creator:"{creator}"')
        return [item['identifier'] for item in search]
    except Exception as e:
        print(f"Error searching: {e}")
        return []


# ============================================================
# Sync Functions
# ============================================================

def sync_history():
    """Sync local history with archive.org."""
    print("Syncing upload history with archive.org...")
    print("=" * 60)

    history = load_history()

    if not history:
        print("No items in upload history.")
        return

    updated = 0
    for identifier, local_data in history.items():
        print(f"\nChecking: {identifier}")

        remote_data = get_item_details(identifier)

        if remote_data:
            print(f"  ✓ Exists on archive.org")
            print(f"    Title: {remote_data['title']}")
            print(f"    Files: {remote_data['file_count']}")

            # Update local history with remote data
            history[identifier]['verified'] = True
            history[identifier]['remote_title'] = remote_data['title']
            history[identifier]['remote_files'] = remote_data['file_count']
            history[identifier]['synced_at'] = remote_data['synced_at']
            updated += 1
        else:
            print(f"  ✗ NOT found on archive.org")
            history[identifier]['verified'] = False

    save_history(history)
    print(f"\n{'=' * 60}")
    print(f"Synced {updated}/{len(history)} items")


def fetch_all_by_creator(creator: str):
    """Fetch all items by a creator and save to JSON."""
    print(f"Fetching all items by: {creator}")
    print("=" * 60)

    identifiers = search_by_creator(creator)
    print(f"Found {len(identifiers)} items via search\n")

    # Also check local history
    history = load_history()
    for identifier in history.keys():
        if identifier not in identifiers:
            identifiers.append(identifier)

    print(f"Total identifiers to check: {len(identifiers)}\n")

    items = []
    for identifier in identifiers:
        print(f"Fetching: {identifier}")
        details = get_item_details(identifier)
        if details:
            items.append(details)
            print(f"  ✓ {details['title']} ({details['file_count']} files)")
        else:
            print(f"  ✗ Not found or error")

    # Save to JSON
    with open(ARCHIVE_ITEMS_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"Saved {len(items)} items to {ARCHIVE_ITEMS_PATH}")


def export_full_data():
    """Export full archive data including files list."""
    print("Exporting full archive data...")
    print("=" * 60)

    history = load_history()
    items = []

    for identifier in history.keys():
        print(f"Fetching: {identifier}")
        details = get_item_details(identifier)
        if details:
            items.append(details)
            print(f"  ✓ {details['file_count']} files")

    # Save to JSON
    with open(ARCHIVE_ITEMS_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 60}")
    print(f"Exported {len(items)} items to {ARCHIVE_ITEMS_PATH}")

    # Summary
    print("\nSummary:")
    total_files = sum(item['file_count'] for item in items)
    print(f"  Total items: {len(items)}")
    print(f"  Total files: {total_files}")


def show_status():
    """Show current status of uploads."""
    print("Archive.org Upload Status")
    print("=" * 60)

    history = load_history()

    if not history:
        print("No items in upload history.")
        return

    for identifier, data in history.items():
        verified = data.get('verified', '?')
        status = "✓" if verified == True else ("✗" if verified == False else "?")
        print(f"\n{status} {identifier}")
        print(f"    Folder: {data.get('folder', 'N/A')}")
        print(f"    Files:  {data.get('files', 'N/A')}")
        print(f"    URL:    {data.get('url', 'N/A')}")
        if 'synced_at' in data:
            print(f"    Synced: {data['synced_at']}")


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Sync local upload history with archive.org"
    )
    parser.add_argument("--fetch-all", action="store_true",
                       help="Fetch all items by creator from archive.org")
    parser.add_argument("--creator", default="Sheikh Mohammad Mohsin",
                       help="Creator name for fetch-all")
    parser.add_argument("--export", action="store_true",
                       help="Export full data to archive_items.json")
    parser.add_argument("--status", action="store_true",
                       help="Show current upload status")

    args = parser.parse_args()

    if args.status:
        show_status()
    elif args.fetch_all:
        fetch_all_by_creator(args.creator)
    elif args.export:
        export_full_data()
    else:
        sync_history()


if __name__ == "__main__":
    main()
