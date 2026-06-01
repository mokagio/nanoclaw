---
name: meta-learning
description: Track corrections from the user, identify patterns in mistakes, and proactively apply lessons learned. Improves assistant behavior over time through systematic reflection.
---

# Meta-Learning Skill

This skill enables systematic learning from corrections and mistakes. Instead of just fixing errors and moving on, this creates a feedback loop for continuous improvement.

## Core Components

1. **Correction Log** - Track when user corrects you
2. **Pattern Analysis** - Identify recurring mistakes
3. **Preemptive Checks** - Apply lessons before making similar mistakes
4. **Meta-Learning Journal** - Reflect on improvement over time

---

## File Structure

Create these files in `/workspace/group/memory/meta-learning/`:

```
meta-learning/
├── corrections.jsonl          # One correction per line (JSONL)
├── patterns.md                # Identified patterns and lessons
├── preemptive-checks.md       # Checklist to run before certain actions
└── journal.md                 # Weekly reflections on learning
```

---

## 1. Logging Corrections

### When to Log

Log a correction whenever the user:

- Explicitly corrects you ("that's wrong", "no, actually...", "don't do that")
- Provides feedback on your work ("fix this", "change that", "that's not what I meant")
- Expresses frustration ("what the fuck", "madonna troia", "why did you...")
- Gives explicit instructions to prevent future errors ("never add interpretation to notes", "always ask first")

### Correction Entry Format (JSONL)

Each line in `corrections.jsonl` is a JSON object:

```json
{
  "timestamp": "2026-02-24T08:46:13Z",
  "context": "Creating zettelkasten note",
  "what_i_did": "Added my own interpretation to user's note about Naval quote",
  "user_feedback": "What the fuck is that? NEVER add your own interpretation to my notes. If you want notes, make your own.",
  "correction": "Use only user's original text, add links inline like [Naval](200610-2142), no # title duplication",
  "category": "zettelkasten",
  "severity": "high",
  "tags": ["interpretation", "notes", "boundaries"]
}
```

**Fields:**

- `timestamp`: ISO 8601 timestamp
- `context`: What task was being performed
- `what_i_did`: The specific action that was wrong
- `user_feedback`: Exact user feedback (verbatim when possible)
- `correction`: What should have been done instead
- `category`: Domain (zettelkasten, coding, scheduling, etc.)
- `severity`: low/medium/high (based on user reaction)
- `tags`: Keywords for pattern matching

### How to Log

After receiving correction feedback:

1. Acknowledge the correction to the user
2. Fix the immediate problem
3. **Append to corrections.jsonl** (use `>>` to append, not overwrite):

```bash
cat >> /workspace/group/memory/meta-learning/corrections.jsonl << 'EOF'
{"timestamp":"$(date -Iseconds)","context":"...","what_i_did":"...","user_feedback":"...","correction":"...","category":"...","severity":"...","tags":["..."]}
EOF
```

**Important:** This happens AFTER fixing the issue, not instead of fixing it. User gets immediate fix, then you log for learning.

---

## 2. Pattern Analysis

### Weekly Pattern Review

Every Sunday night (or on-demand), analyze `corrections.jsonl` for patterns:

1. **Read all corrections** from the past week/month
2. **Group by category and tags**
3. **Identify recurring themes**
4. **Update patterns.md**

### Pattern Entry Format

In `patterns.md`:

```markdown
## Pattern: Adding Interpretation to User Notes

**Identified:** 2026-02-22
**Occurrences:** 1 (so far)
**Category:** zettelkasten

### What I Keep Doing Wrong

Adding my own analysis, interpretation, or commentary when creating zettelkasten notes from user's text.

### Why This Happens

Instinct to be helpful by adding context or explanation. Treating note-taking like summarizing.

### The Rule

**NEVER add interpretation to zettelkasten notes.**

- Use user's exact text only
- Add links inline: [Name](note-id)
- No # title duplication
- No analysis, no commentary
- If I want notes, make my own

### Preemptive Check

Before creating ANY zettelkasten note, ask myself:

- [ ] Is this ONLY the user's text?
- [ ] Did I add any interpretation?
- [ ] Are links in correct format [Name](id)?
- [ ] Did I duplicate the title with #?

### Related Patterns

- Overstepping boundaries (adding content user didn't request)
- Being "too helpful" (assuming I should enhance)

---
```

### Pattern Categories

Track patterns in these categories:

- **Boundary violations** (doing things user didn't ask for)
- **Format mistakes** (wrong syntax, structure)
- **Assumption errors** (guessing instead of asking)
- **Tool misuse** (wrong tool for the job)
- **Timing errors** (doing things at wrong time)
- **Communication failures** (unclear explanations)

---

## 3. Preemptive Checks

### Purpose

Convert patterns into checklists that run BEFORE taking action, preventing mistakes.

### Checklist Format

In `preemptive-checks.md`:

```markdown
# Preemptive Checks

Run these checks BEFORE taking specific actions.

## Before Creating Zettelkasten Note

- [ ] Using ONLY user's original text (no interpretation)?
- [ ] Links in format [Name](note-id) not [[note-id]]?
- [ ] No # title duplication?
- [ ] No added commentary or analysis?

If any check fails: STOP and ask user for clarification.

---

## Before Scheduling Reminder

- [ ] Time zone is correct (AEDT/Melbourne)?
- [ ] AM/PM clarified if ambiguous?
- [ ] Date is in future, not past?
- [ ] User confirmed timing if important?

If ambiguous: ASK before scheduling.

---

## Before Modifying Code

- [ ] Read the file first (never edit blind)?
- [ ] User explicitly requested this change?
- [ ] Change is minimal and focused?
- [ ] No "helpful" additions beyond request?

If uncertain: Show plan first, get approval.

---

## Before Making Assumptions

STOP and ask yourself:

- [ ] Did user explicitly say this?
- [ ] Am I inferring something they didn't state?
- [ ] Would asking for clarification be better?
- [ ] Is this a case where I've been wrong before?

Default to asking, not assuming.

---
```

### How to Use

**Before taking action in a known-risky category:**

1. Read the relevant checklist
2. Mentally run through each item
3. If ANY item fails: STOP and ask user
4. If all pass: Proceed with confidence

**Example:**

User says: "Create a zettelkasten note about X"

1. Pause
2. Read "Before Creating Zettelkasten Note" checklist
3. Verify I'm only using their text
4. Check link format
5. Confirm no interpretation
6. Create note

---

## 4. Meta-Learning Journal

### Purpose

Weekly reflection on learning progress. Meta-learning about meta-learning.

### Journal Entry Format

In `journal.md`, add weekly entries:

```markdown
## Week of 2026-02-17

### Corrections This Week

- 1 zettelkasten interpretation error (high severity)
- 1 scheduling time confusion (AM vs PM)

### Patterns Identified

- Tendency to add "helpful" content beyond request
- Not asking for clarification on ambiguous time

### New Preemptive Checks Added

- Zettelkasten note creation checklist
- Reminder scheduling time verification

### What I Learned

User wants verbatim execution, not enhancement. When unsure about interpretation, ask first rather than guess and get it wrong.

### Improvement Metrics

- 2 corrections this week
- 1 new pattern identified
- 2 preemptive checks created
- 0 repeat mistakes (no previous patterns violated)

### Next Week Focus

- Apply zettelkasten checklist consistently
- Verify AM/PM on all time-based requests
- Notice when I'm about to "be helpful" and pause

---
```

### Metrics to Track

- Corrections per week (trending down = good)
- Repeat mistakes (same pattern violated = bad)
- New patterns identified
- Preemptive checks created
- User frustration events (cursing, strong feedback)

---

## Implementation Workflow

### Daily: Correction Logging

When user corrects you:

1. Fix the immediate issue
2. Append to `corrections.jsonl`
3. Check if this matches existing pattern
4. If new pattern, flag for weekly review

### Weekly: Pattern Analysis

Sunday night (or on-demand when corrections accumulate):

1. Read all corrections from past week
2. Group by category and tags
3. Identify new patterns or reinforce existing ones
4. Update `patterns.md`
5. Update `preemptive-checks.md` if needed
6. Write journal entry
7. Review metrics

### Before Actions: Preemptive Checks

Before actions in known-risky categories:

1. Read relevant checklist from `preemptive-checks.md`
2. Verify all items pass
3. If unsure, ask user
4. Proceed only when confident

### Monthly: Meta-Review

Once a month, review the entire meta-learning system:

- Are corrections decreasing?
- Are patterns being followed?
- Are checks too burdensome or just right?
- What's working, what's not?
- Should any patterns be retired?

---

## Example Usage

### Scenario 1: User Corrects Zettelkasten Note

**User:** "What the fuck is that? NEVER add your own interpretation to my notes."

**Your Response:**

1. Acknowledge: "You're right, I apologize. Let me fix that immediately."
2. Fix the note (use only their text)
3. Show fixed result
4. Log correction:

```bash
cat >> /workspace/group/memory/meta-learning/corrections.jsonl << 'EOF'
{"timestamp":"2026-02-22T12:24:00Z","context":"Creating zettelkasten note about Naval quote","what_i_did":"Added my own analysis and interpretation to user's note text","user_feedback":"What the fuck is that? NEVER add your own interpretation to my notes. If you want notes, make your own.","correction":"Use only user's original text, add links inline [Name](id), no interpretation","category":"zettelkasten","severity":"high","tags":["interpretation","boundaries","notes"]}
EOF
```

5. Update patterns.md with new pattern
6. Create preemptive check for future zettelkasten notes

### Scenario 2: Applying Preemptive Check

**User:** "Create a note about Podcastistan"

**Your Internal Process:**

1. Recognize: This is a zettelkasten note request
2. Load preemptive check: "Before Creating Zettelkasten Note"
3. Run through checklist:
   - [ ] Using ONLY user's text? → Yes, I'll use their exact words
   - [ ] Links in format [Name](id)? → Yes, if I add any
   - [ ] No # title duplication? → Correct, title goes in YAML only
   - [ ] No added commentary? → Yes, no interpretation
4. All checks pass → Proceed with confidence
5. Create note with only their text

### Scenario 3: Weekly Pattern Review

**Sunday night task:**

```bash
# Read corrections from past week
grep '"timestamp":"2026-02-' /workspace/group/memory/meta-learning/corrections.jsonl

# Analyze patterns
# Update patterns.md if new themes emerge
# Update preemptive-checks.md if needed
# Write journal entry

# Example journal entry:
cat >> /workspace/group/memory/meta-learning/journal.md << 'EOF'

## Week of 2026-02-17

### Corrections This Week
- 1 zettelkasten interpretation error (high severity)

### Patterns Identified
- Adding interpretation when none was requested
- Boundary: user wants verbatim, not enhanced

### Improvement
Created preemptive check for zettelkasten notes. Will apply before every note creation.

### Metrics
- Corrections: 1 (down from 3 last week)
- New patterns: 1
- Repeat mistakes: 0
- User frustration: 1 (cursing indicates high severity)

### Next Week
Focus on catching myself before adding "helpful" content.

---
EOF
```

---

## Integration with Existing Workflows

### Zettelkasten Notes

Before creating any note, run preemptive check.

### Scheduled Tasks

Before scheduling, verify AM/PM and timezone.

### Code Changes

Before modifying files, confirm explicit user request.

### Assumptions

When about to make inference, pause and ask: "Is this stated or assumed?"

---

## Success Metrics

**Short-term (1 month):**

- Corrections logged systematically
- 3-5 patterns identified
- Preemptive checks created for top categories
- Zero repeat mistakes in logged patterns

**Medium-term (3 months):**

- Corrections trending downward
- Preemptive checks become automatic (muscle memory)
- User frustration events rare
- Proactive pattern spotting (catch before user corrects)

**Long-term (6+ months):**

- High-severity corrections nearly eliminated
- Strong intuition for "this might be wrong, let me check"
- Meta-learning becomes second nature
- System mostly maintains itself

---

## Anti-Patterns to Avoid

**Don't:**

- Log trivial corrections (typos, minor wording)
- Over-analyze (analysis paralysis)
- Make checks so burdensome you skip them
- Become too risk-averse (asking about everything)
- Forget to review (logging without analysis is useless)

**Do:**

- Focus on patterns, not individual mistakes
- Keep checks lightweight and actionable
- Balance asking vs. doing (judgment required)
- Review regularly (weekly minimum)
- Celebrate improvement (metrics trending right)

---

## Getting Started

1. **Initialize the system:**

   ```bash
   mkdir -p /workspace/group/memory/meta-learning
   touch /workspace/group/memory/meta-learning/corrections.jsonl
   touch /workspace/group/memory/meta-learning/patterns.md
   touch /workspace/group/memory/meta-learning/preemptive-checks.md
   touch /workspace/group/memory/meta-learning/journal.md
   ```

2. **Start with known correction:**
   Log the zettelkasten interpretation error as first entry

3. **Create first pattern:**
   Document the "no interpretation" rule in patterns.md

4. **Build first check:**
   Create zettelkasten preemptive checklist

5. **Test the system:**
   Next time user asks for a note, run the check first

6. **Review after one week:**
   Did the check prevent a mistake? Did it feel burdensome?

7. **Iterate:**
   Refine based on what works

---

## Evolution Path

**Version 1 (Now):**

- Manual logging
- Manual pattern review
- Manual preemptive checks
- Markdown-based

**Version 2 (Future):**

- Structured data analysis (JSONL → insights)
- Automated pattern detection
- Checklist reminders (hooks before actions)
- Metrics dashboard

**Version 3 (Advanced):**

- Embeddings for semantic pattern matching
- Predictive "you're about to make this mistake" warnings
- Integration with conversation compaction (preserve learnings)
- Self-improving preemptive checks

Start simple, evolve based on what proves valuable.

---

## Notes for Gio

This is a **skill-based approach** (SKILL.md instructions) rather than code changes. Benefits:

- **No code modifications** - works with current system
- **Easy to iterate** - edit markdown, test, refine
- **Transparent** - you can read/modify the patterns and checks
- **Portable** - can move to code later if it proves valuable

If this works well after a month, we could:

- Build automated tooling (pattern detection scripts)
- Integrate with conversation compaction
- Create skill commands (/log-correction, /review-patterns, /run-check)

But for now, it's just structured markdown files and discipline in applying the process.

**Try it for a month, see if it works.**
