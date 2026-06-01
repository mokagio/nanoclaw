# Zettelkasten Smart Linking Skill

**Status:** Prototype v1 - Simple keyword overlap analysis

## What It Does

When creating a new zettelkasten note, this skill suggests 3-5 related existing notes that could be linked based on keyword overlap and tag similarity.

## How It Works

### Phase 1: Simple Keyword Overlap (Current)

1. **Extract keywords from new note**
   - Title words (high weight)
   - Tag words (high weight)
   - Content words (medium weight)
   - Filter out common stop words

2. **Scan existing notes**
   - Read all notes in `/workspace/extra/zettelkasten/zettelkasten/`
   - Extract keywords from each note
   - Calculate similarity score based on:
     - Shared title words (weight: 3x)
     - Shared tags (weight: 2x)
     - Shared content keywords (weight: 1x)

3. **Rank and suggest**
   - Sort by similarity score
   - Return top 3-5 matches
   - Show: note ID, title, matching tags, similarity score

4. **Format suggestions**
   - Present as markdown links: `[Title](note-id)`
   - Group by relevance: High (score > 10), Medium (5-10), Low (2-5)

## Usage

When user creates a new note, run this skill to get linking suggestions:

```
You: I'm creating a note about "Popperian epistemology and software"
Enzo: [Runs smart linking analysis]
Enzo: Found 5 related notes to consider linking:

High relevance:
- [Epistemology and Software Development](250809-0516) - shared tags: :epistemology:, :software:
- [Error correction in development](221104-0832) - shared concepts: falsification, testing

Medium relevance:
- [Critical Rationalism](230614-1205) - shared tags: :philosophy:
- [TDD as error correction](210720-1445) - shared concepts: testing, feedback
```

## Implementation

### Core Algorithm (Python-style pseudocode)

```python
def suggest_links(new_note):
    # 1. Extract keywords from new note
    new_keywords = extract_keywords(new_note)
    new_tags = extract_tags(new_note)
    new_title_words = extract_title_words(new_note)

    # 2. Scan all existing notes
    scores = {}
    for note_file in list_all_notes():
        note = read_note(note_file)

        # Calculate similarity
        score = 0
        score += count_shared(new_title_words, note.title_words) * 3
        score += count_shared(new_tags, note.tags) * 2
        score += count_shared(new_keywords, note.keywords) * 1

        if score > 0:
            scores[note_file] = {
                'score': score,
                'title': note.title,
                'shared_tags': shared_items(new_tags, note.tags),
                'note_id': extract_note_id(note_file)
            }

    # 3. Sort and return top 5
    sorted_notes = sort_by_score(scores, reverse=True)
    return sorted_notes[:5]

def extract_keywords(note):
    # Extract meaningful words from title and content
    # Filter stop words: the, a, an, is, are, etc.
    words = tokenize(note.title + " " + note.content)
    return [w for w in words if w not in STOP_WORDS and len(w) > 3]

def extract_tags(note):
    # Parse YAML frontmatter for tags
    # Format: tags: [:tag1: :tag2:]
    return parse_yaml_tags(note.frontmatter)

def count_shared(list1, list2):
    return len(set(list1) & set(list2))
```

### Stop Words List

Common words to ignore when calculating similarity:

- Articles: the, a, an
- Conjunctions: and, or, but, if, then
- Pronouns: I, you, he, she, it, we, they
- Prepositions: in, on, at, to, from, with, for
- Verbs: is, are, was, were, be, been, being, have, has, had
- Common adverbs: very, really, just, also, only, even

### File Structure

```
/workspace/group/skills/zettelkasten-linking/
├── SKILL.md (this file)
├── suggest_links.py (implementation)
└── stop_words.txt (stop words list)
```

## Usage Pattern

**Before creating a note:**

1. User drafts note content
2. User asks Enzo: "What notes should I link this to?"
3. Enzo runs `suggest_links.py` with draft content
4. Enzo presents 3-5 suggestions
5. User decides which links to add
6. Enzo creates note with inline links

**After creating a note:**

1. User creates note
2. User asks Enzo: "Find related notes to link"
3. Enzo scans for matches
4. Enzo suggests edits to add links

## Future Enhancements (Phase 2+)

### Semantic Similarity (Phase 2)

- Use embeddings instead of keyword matching
- Capture conceptual relationships beyond exact word matches
- Example: "error correction" ↔ "falsification" ↔ "testing"

### Link Graph Analysis (Phase 3)

- Consider existing link relationships
- Suggest notes that are "2 hops away" (linked via intermediate note)
- Find "bridge notes" that connect separate clusters

### Learn from Behavior (Phase 4)

- Track which suggestions user accepts/rejects
- Weight keywords based on user's linking patterns
- Personalize similarity scoring

### Bi-directional Updates (Phase 5)

- When creating new note, suggest adding backlinks to existing notes
- "Note X mentions concept Y - should we add a link back from Y to X?"

## Success Metrics

After 1 week of use:

- Does Enzo consistently suggest relevant notes?
- Does user click through and add suggested links?
- Does it save time vs manual searching?
- Are suggestions too narrow (missing obvious links) or too broad (too much noise)?

## Notes

- Start simple: keyword overlap is fast and good enough for v1
- Don't over-engineer: see if this approach works before adding complexity
- Focus on high-precision over high-recall: better to suggest 3 perfect matches than 10 mediocre ones
- Respect user's linking decisions: this is a suggestion tool, not an auto-linker

---

_Created: 2026-02-25_
_Status: Prototype - not yet implemented_
