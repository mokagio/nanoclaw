#!/usr/bin/env python3
import os
import json
import re
from collections import Counter

ZK_PATH = '/workspace/extra/zettelkasten/zettelkasten/'
OUTPUT_DIR = '/workspace/group/'

def build_title_index(zk_path):
    """Build a mapping of note titles to note IDs."""
    title_index = {}

    try:
        entries = os.listdir(zk_path)
    except FileNotFoundError:
        return title_index

    for filename in entries:
        if not filename.endswith('.md'):
            continue

        note_id = filename[:-3]
        filepath = os.path.join(zk_path, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Match: title: <title>
            match = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
            if match:
                title = match.group(1).strip()
                title_index[title] = note_id
        except Exception as err:
            print(f"Error reading {filename}: {err}")

    return title_index

def build_tag_index(zk_path):
    """Build a list of the top 100 tags by frequency."""
    tag_counts = Counter()

    try:
        entries = os.listdir(zk_path)
    except FileNotFoundError:
        return []

    for filename in entries:
        if not filename.endswith('.md'):
            continue

        filepath = os.path.join(zk_path, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Match: tags:\n  - tag1\n  - tag2\n...
            tags_match = re.search(r'^tags:\n((?:\s+-\s+.+\n)*)', content, re.MULTILINE)
            if not tags_match:
                continue

            tag_lines = tags_match.group(1).split('\n')
            for line in tag_lines:
                tag_match = re.match(r'^\s+-\s+(.+)', line)
                if tag_match:
                    tag = tag_match.group(1).strip()
                    tag_counts[tag] += 1
        except Exception as err:
            print(f"Error reading {filename}: {err}")

    # Return top 100 tags sorted by frequency
    top_tags = [
        {"tag": tag, "count": count}
        for tag, count in tag_counts.most_common(100)
    ]
    return top_tags

if __name__ == '__main__':
    print('Rebuilding zettelkasten indexes...')

    # Build and save title index
    title_index = build_title_index(ZK_PATH)
    title_output = os.path.join(OUTPUT_DIR, 'zettelkasten_title_index.json')
    with open(title_output, 'w', encoding='utf-8') as f:
        json.dump(title_index, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'Saved {len(title_index)} note titles to {title_output}')

    # Build and save tag index
    tags = build_tag_index(ZK_PATH)
    tag_output = os.path.join(OUTPUT_DIR, 'zettelkasten_tags.json')
    with open(tag_output, 'w', encoding='utf-8') as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f'Saved {len(tags)} tags to {tag_output}')

    print('Done!')
