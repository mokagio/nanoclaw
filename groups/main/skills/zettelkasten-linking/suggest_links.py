#!/usr/bin/env python3
"""
Zettelkasten Smart Linking - Suggest related notes based on keyword overlap

Usage:
    python suggest_links.py --title "Note Title" --tags ":tag1: :tag2:" --content "Note content..."
    python suggest_links.py --file path/to/draft-note.md
"""

import os
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass

# Stop words to ignore in similarity calculation
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else',
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may', 'might',
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'them', 'their', 'this', 'that',
    'in', 'on', 'at', 'to', 'from', 'with', 'for', 'by', 'of', 'as',
    'very', 'really', 'just', 'also', 'only', 'even', 'so', 'more', 'most',
    'some', 'any', 'all', 'both', 'each', 'few', 'many', 'much', 'own', 'same',
    'than', 'too', 'very', 'can', 'about', 'into', 'through', 'during', 'before',
    'after', 'above', 'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again'
}

@dataclass
class Note:
    """Represents a zettelkasten note"""
    file_path: str
    note_id: str
    title: str
    tags: Set[str]
    content: str
    title_words: Set[str]
    content_words: Set[str]

@dataclass
class LinkSuggestion:
    """A suggested link to another note"""
    note_id: str
    title: str
    score: float
    shared_tags: Set[str]
    shared_title_words: Set[str]
    shared_content_words: Set[str]

def extract_note_id(file_path: str) -> str:
    """Extract note ID from filename (e.g., '260222-1224' from '260222-1224.md')"""
    return Path(file_path).stem

def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter from markdown content"""
    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    # Simple YAML parser for our needs (title, tags, date, url)
    frontmatter_text = match.group(1)
    body = match.group(2)
    frontmatter = {}

    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if not line or ':' not in line:
            continue

        # Handle "key: value" format
        key, _, value = line.partition(':')
        key = key.strip()
        value = value.strip()

        if key == 'tags':
            # Tags might be on multiple lines or inline
            # For now, just grab the current line
            frontmatter[key] = value
        elif key.startswith('-'):
            # This is a list item under tags
            if 'tags' in frontmatter and isinstance(frontmatter['tags'], str):
                frontmatter['tags'] += ' ' + key.strip('-').strip()
        else:
            frontmatter[key] = value

    return frontmatter, body

def extract_tags(frontmatter: Dict) -> Set[str]:
    """Extract tags from frontmatter"""
    tags = frontmatter.get('tags', [])
    if isinstance(tags, str):
        # Handle format like ":tag1: :tag2:"
        tags = re.findall(r':([^:]+):', tags)
    elif isinstance(tags, list):
        # Handle list format, strip colons
        tags = [tag.strip(':') for tag in tags]
    return set(tags)

def tokenize(text: str) -> Set[str]:
    """Extract words from text, filtering stop words and short words"""
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-z]{4,}\b', text.lower())
    # Filter stop words
    return {w for w in words if w not in STOP_WORDS}

def read_note(file_path: str) -> Note:
    """Read and parse a zettelkasten note"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    frontmatter, body = parse_frontmatter(content)

    note_id = extract_note_id(file_path)
    title = frontmatter.get('title', '')
    tags = extract_tags(frontmatter)

    title_words = tokenize(title)
    content_words = tokenize(body)

    return Note(
        file_path=file_path,
        note_id=note_id,
        title=title,
        tags=tags,
        content=body,
        title_words=title_words,
        content_words=content_words
    )

def calculate_similarity(new_note: Note, existing_note: Note) -> float:
    """Calculate similarity score between two notes"""
    score = 0.0

    # Shared title words (weight: 3x)
    shared_title = new_note.title_words & existing_note.title_words
    score += len(shared_title) * 3

    # Shared tags (weight: 2x)
    shared_tags = new_note.tags & existing_note.tags
    score += len(shared_tags) * 2

    # Shared content words (weight: 1x)
    shared_content = new_note.content_words & existing_note.content_words
    score += len(shared_content) * 1

    return score

def suggest_links(
    zettelkasten_dir: str,
    new_note: Note,
    top_n: int = 5
) -> List[LinkSuggestion]:
    """Suggest related notes to link"""
    suggestions = []

    # Scan all existing notes
    for file_path in Path(zettelkasten_dir).glob('*.md'):
        # Skip index and special files
        if file_path.stem in ['index', 'README']:
            continue

        try:
            existing_note = read_note(str(file_path))

            # Calculate similarity
            score = calculate_similarity(new_note, existing_note)

            if score > 0:
                suggestions.append(LinkSuggestion(
                    note_id=existing_note.note_id,
                    title=existing_note.title,
                    score=score,
                    shared_tags=new_note.tags & existing_note.tags,
                    shared_title_words=new_note.title_words & existing_note.title_words,
                    shared_content_words=new_note.content_words & existing_note.content_words
                ))
        except Exception as e:
            # Skip notes that can't be parsed
            pass

    # Sort by score and return top N
    suggestions.sort(key=lambda x: x.score, reverse=True)
    return suggestions[:top_n]

def format_suggestions(suggestions: List[LinkSuggestion]) -> str:
    """Format suggestions as markdown"""
    if not suggestions:
        return "No related notes found."

    output = []

    # Group by relevance
    high = [s for s in suggestions if s.score >= 10]
    medium = [s for s in suggestions if 5 <= s.score < 10]
    low = [s for s in suggestions if 2 <= s.score < 5]

    if high:
        output.append("**High relevance:**")
        for s in high:
            details = []
            if s.shared_tags:
                details.append(f"tags: {', '.join(':' + t + ':' for t in s.shared_tags)}")
            if s.shared_title_words:
                details.append(f"title words: {', '.join(s.shared_title_words)}")

            detail_str = f" ({'; '.join(details)})" if details else ""
            output.append(f"- [{s.title}]({s.note_id}){detail_str}")
        output.append("")

    if medium:
        output.append("**Medium relevance:**")
        for s in medium:
            details = []
            if s.shared_tags:
                details.append(f"tags: {', '.join(':' + t + ':' for t in s.shared_tags)}")

            detail_str = f" ({'; '.join(details)})" if details else ""
            output.append(f"- [{s.title}]({s.note_id}){detail_str}")
        output.append("")

    if low:
        output.append("**Lower relevance:**")
        for s in low:
            output.append(f"- [{s.title}]({s.note_id})")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Suggest related zettelkasten notes to link'
    )
    parser.add_argument('--title', help='Note title')
    parser.add_argument('--tags', help='Note tags (format: ":tag1: :tag2:")')
    parser.add_argument('--content', help='Note content')
    parser.add_argument('--file', help='Path to draft note file')
    parser.add_argument('--zettelkasten-dir',
                       default='/workspace/extra/zettelkasten/zettelkasten',
                       help='Path to zettelkasten directory')
    parser.add_argument('--top-n', type=int, default=5,
                       help='Number of suggestions to return')

    args = parser.parse_args()

    # Read new note
    if args.file:
        new_note = read_note(args.file)
    else:
        # Create note from arguments
        frontmatter = {
            'title': args.title or '',
            'tags': args.tags or ''
        }
        content = args.content or ''

        new_note = Note(
            file_path='',
            note_id='new',
            title=frontmatter['title'],
            tags=extract_tags(frontmatter),
            content=content,
            title_words=tokenize(frontmatter['title']),
            content_words=tokenize(content)
        )

    # Get suggestions
    suggestions = suggest_links(args.zettelkasten_dir, new_note, args.top_n)

    # Print results
    print(format_suggestions(suggestions))

if __name__ == '__main__':
    main()
