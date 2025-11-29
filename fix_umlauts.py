#!/usr/bin/env python3
"""
Script to fix umlauts in image filenames for Vercel deployment
"""
import os
import json
import shutil

# Mapping of umlauts to ASCII equivalents
UMLAUT_MAP = {
    'ä': 'ae',
    'ö': 'oe',
    'ü': 'ue',
    'Ä': 'Ae',
    'Ö': 'Oe',
    'Ü': 'Ue',
    'ß': 'ss'
}

def replace_umlauts(text):
    """Replace umlauts in text with ASCII equivalents"""
    for umlaut, replacement in UMLAUT_MAP.items():
        text = text.replace(umlaut, replacement)
    return text

def rename_files_in_directory(directory):
    """Rename all files with umlauts in the given directory"""
    renamed_files = {}

    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist, skipping...")
        return renamed_files

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if any(char in filename for char in UMLAUT_MAP.keys()):
                old_path = os.path.join(root, filename)
                new_filename = replace_umlauts(filename)
                new_path = os.path.join(root, new_filename)

                print(f"Renaming: {old_path} -> {new_path}")
                shutil.move(old_path, new_path)

                # Store the mapping relative to the directory
                rel_old = os.path.relpath(old_path, directory)
                rel_new = os.path.relpath(new_path, directory)
                renamed_files[rel_old] = rel_new

    return renamed_files

def update_activities_json(json_file, renamed_files):
    """Update activities.json to reflect renamed files"""
    with open(json_file, 'r', encoding='utf-8') as f:
        activities = json.load(f)

    updated = False

    for activity in activities:
        # Check main image_filename
        if 'image_filename' in activity and activity['image_filename'].startswith('activities/'):
            old_filename = activity['image_filename'].replace('activities/', '')
            new_filename = replace_umlauts(old_filename)
            if old_filename != new_filename:
                activity['image_filename'] = f'activities/{new_filename}'
                print(f"Updated activity {activity['id']}: {old_filename} -> {new_filename}")
                updated = True

        # Check sub_items
        if 'sub_items' in activity:
            for sub_item in activity['sub_items']:
                if 'image_filename' in sub_item and sub_item['image_filename'].startswith('activities/'):
                    old_filename = sub_item['image_filename'].replace('activities/', '')
                    new_filename = replace_umlauts(old_filename)
                    if old_filename != new_filename:
                        sub_item['image_filename'] = f'activities/{new_filename}'
                        print(f"Updated sub_item {sub_item['id']}: {old_filename} -> {new_filename}")
                        updated = True

    if updated:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(activities, f, ensure_ascii=False, indent=2)
        print(f"\nUpdated {json_file}")
    else:
        print(f"\nNo updates needed in {json_file}")

if __name__ == '__main__':
    print("=" * 60)
    print("Fixing umlauts in image filenames for Vercel deployment")
    print("=" * 60)

    # Rename files in app/static/images
    print("\n1. Renaming files in app/static/images...")
    renamed_files = rename_files_in_directory('app/static/images')

    # Update activities.json
    print("\n2. Updating data/activities.json...")
    update_activities_json('data/activities.json', renamed_files)

    print("\n" + "=" * 60)
    print("Done! All umlauts have been replaced.")
    print("=" * 60)
