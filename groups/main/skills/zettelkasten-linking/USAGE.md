# How to Use Zettelkasten Smart Linking

## Quick Start

When user is creating a new note or wants to find related notes:

```bash
python3 /workspace/group/skills/zettelkasten-linking/suggest_links.py \
  --title "Note Title" \
  --tags ":tag1: :tag2:" \
  --content "Note content here..."
```

## Usage Patterns

### Pattern 1: Before Creating Note

**User:** "I want to create a note about Popperian epistemology in software development"

**Enzo:**

1. Ask user for key details (title, tags, main content)
2. Run suggest_links.py with those details
3. Present suggestions
4. User decides which links to include
5. Create note with inline links

### Pattern 2: After Creating Note

**User:** "Find notes related to 260222-2207"

**Enzo:**

1. Read the existing note
2. Extract title, tags, content
3. Run suggest_links.py
4. Present suggestions
5. User decides whether to edit note to add links

### Pattern 3: Batch Linking

**User:** "Check my recent notes and suggest links for them"

**Enzo:**

1. Find recently created notes (last week)
2. For each note, run suggest_links.py
3. Present all suggestions in a summary
4. User picks which ones to act on

## Example Interactions

### Example 1: Creating TDD Note

**User:** "Create a note: TDD is error correction through rapid feedback. Each test is a conjecture."

**Enzo:** "Before I create that note, let me find related notes you might want to link..."

_[Runs suggest_links.py]_

**Enzo:** "Found these related notes:

**Medium relevance:**

- [Antifragility as error-correction](250502-1446)
- [Error correction is simple to understand but hard to implement](230815-0925)
- [Product Iterations are Error Corrections](240826-0819)

Would you like me to include any of these as links in your new note?"

**User:** "Yes, link the first two"

**Enzo:** _[Creates note with inline links]_

### Example 2: Finding Links for Existing Note

**User:** "What notes should I link from my Podcastistan note?"

**Enzo:** _[Reads 260222-2207.md, runs suggest_links.py]_

**Enzo:** "Here are related notes to consider:

**Medium relevance:**

- [The Dawn of the Post-Literal Society - A critique](251002-0726)
- [You must not fool yourself — and you are the easiest one to fool](210406-0528)

The first one discusses media critique similar to your podcast analysis. The second is about self-deception which relates to your point about engagement over substance."

## Command Line Options

```
--title          Note title
--tags           Tags in format ":tag1: :tag2:"
--content        Note content (body text)
--file           Path to draft note file (alternative to --title/tags/content)
--top-n          Number of suggestions (default: 5)
--zettelkasten-dir  Path to zettelkasten (default: /workspace/extra/zettelkasten/zettelkasten)
```

## Output Format

```
**High relevance:**  (score >= 10)
- [Note Title](note-id) (tags: :shared: :tags:; title words: shared, words)

**Medium relevance:** (score 5-10)
- [Note Title](note-id) (tags: :shared:)

**Lower relevance:**  (score 2-5)
- [Note Title](note-id)
```

## Scoring System

- Shared title words: 3 points each
- Shared tags: 2 points each
- Shared content words: 1 point each

Minimum threshold: 2 points (filters out very weak matches)

## Tips for Good Results

1. **Use descriptive titles** - More keywords = better matching
2. **Tag consistently** - Reuse existing tags when possible
3. **Include key concepts in content** - Not just in title
4. **Don't over-filter** - Review medium relevance suggestions too
5. **It's a suggestion tool** - You decide which links make sense

## Integration with Note Creation

When creating a note, Enzo should:

1. Get user's note content
2. Run suggest_links.py
3. Present top 3-5 suggestions
4. Ask which to include
5. Create note with links in format: `[Title](note-id)`

Example generated note:

```markdown
---
title: TDD as Error Correction
date: 2026-02-25 10:30
tags: :tdd: :testing: :epistemology:
---

Test-driven development is a form of [error correction](250502-1446) through rapid feedback cycles.

Each test is a conjecture that can be falsified. This connects to the broader principle that [error correction is simple to understand but hard to implement](230815-0925).
```

## Performance Notes

- Scans ~3800 notes in < 5 seconds
- No external dependencies (pure Python 3)
- Uses simple keyword matching (fast, good enough for v1)

## Known Limitations

- Only matches exact words (no semantic understanding)
- Doesn't consider existing link graph
- Can't detect conceptual relationships without keyword overlap
- Stop words might filter out some meaningful short words

See SKILL.md for future enhancements.

---

_Created: 2026-02-25_
_Status: Working prototype_
