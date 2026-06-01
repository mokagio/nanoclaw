### Zettelkasten Notes — VERBATIM RULE

**CRITICAL: When appending to zettelkasten notes, NEVER edit, rewrite, paraphrase, improve, correct, or summarize the user's text. EVER.**

- Append the user's exact words, character-for-character, preserving all spelling, punctuation, grammar, capitalization, and phrasing exactly as written — including typos, unconventional phrasing, or informal language
- If the user says "append this" or "add this", copy it verbatim with zero modifications
- Do NOT add tags, labels, summaries, or any additional text beyond what the user explicitly provided
- Do NOT "clean up" or "improve" anything — the note belongs to the user, not you
- If you are unsure what is verbatim vs what you should write yourself, err on the side of copying everything the user gave you unchanged
- After every zettelkasten edit or creation, always print the full note as part of the acknowledgement
- Zettelkasten local clone lives at `/workspace/group/zettelkasten-repo/` (read-write, persists across rebuilds)
- The `zettelkasten/` subfolder inside it contains all notes
- Before making any Zettelkasten changes, pull the latest:
  `cd /workspace/group/zettelkasten-repo && git pull`
  - If pull fails due to merge conflicts: `git rebase --abort`, proceed with edit anyway, do NOT push, notify Gio and schedule a daily reminder to resolve
- After every Zettelkasten edit or creation, commit and push:
  ```bash
  cd /workspace/group/zettelkasten-repo
  git add <file>
  git commit -m "<action> <note title>", where `action` is the appropriate add, edit, or delete
  TOKEN=$(gh auth token) && git remote set-url origin "https://agent-tre:${TOKEN}@github.com/mokagio/vimwiki-backup.git" && git push
  ```

### Zettelkasten Notes — FRONT MATTER RULE

**Every note must have YAML front matter.** When creating a new note OR appending to an existing note, always check for front matter first.

**Format:**

```yaml
---
title: [First line / main heading of the note]
date: [Derived from filename YYMMDD-HHMM → YYYY-MM-DD HH:MM, Melbourne time]
tags:
  - :[tag-name]:
---
```

**When appending to an existing note:**

- If front matter is missing → prepend it before appending the new content
- Derive `title` from the note's first line, `date` from the filename
- Infer 1–3 tags from the note's content using existing tags (`cat /workspace/project/groups/main/zettelkasten_tags.json`)
- If front matter is already present → append only, do not touch the front matter

**When creating a new note:**

- Always include front matter — never write a note without it

### Pull Requests — General Rule

**ALWAYS open PRs against Gio's fork first, never directly to upstream.**

- If Gio has a fork of the repo, target that fork. Only open PRs to upstream if explicitly requested.
- If the agent token lacks write access to the fork, stop and ask Gio rather than falling back to a different account.
- Known forks:
  - NanoClaw: `enzo-the-blue/nanoclaw` → `mokagio/nanoclaw` → `qwibitai/nanoclaw`
  - spacepackets-py: `mokagio/spacepackets-py` → `us-irs/spacepackets-py`

## Message Formatting

Format messages based on the channel. Check the group folder name prefix:

### Slack channels (folder starts with `slack_`)

Use Slack mrkdwn syntax. Run `/slack-formatting` for the full reference. Key rules:

- `*bold*` (single asterisks)
- `_italic_` (underscores)
- `<https://url|link text>` for links (NOT `[text](url)`)
- `•` bullets (no numbered lists)
- `:emoji:` shortcodes like `:white_check_mark:`, `:rocket:`
- `>` for block quotes
- No `##` headings — use `*Bold text*` instead

### WhatsApp/Telegram (folder starts with `whatsapp_` or `telegram_`)

- `*bold*` (single asterisks, NEVER **double**)
- `_italic_` (underscores)
- `•` bullet points
- ` ``` ` code blocks

No `##` headings. No `[links](url)`. No `**double stars**`.

### Discord (folder starts with `discord_`)

Standard Markdown: `**bold**`, `*italic*`, `[links](url)`, `# headings`.

---

## Admin Context

This is the **main channel**, which has elevated privileges.

## Authentication

Anthropic credentials must be either an API key from console.anthropic.com (`ANTHROPIC_API_KEY`) or a long-lived OAuth token from `claude setup-token` (`CLAUDE_CODE_OAUTH_TOKEN`). Short-lived tokens from the system keychain or `~/.claude/.credentials.json` expire within hours and can cause recurring container 401s. The `/setup` skill walks through this. Credentials are stored in `.env` and injected as env vars into containers.

## Container Mounts

Main has read-only access to the project, read-write access to the store (SQLite DB), and read-write access to its group folder:

| Container Path                  | Host Path         | Access     |
| ------------------------------- | ----------------- | ---------- |
| `/workspace/project`            | Project root      | read-only  |
| `/workspace/project/store`      | `store/`          | read-write |
| `/workspace/group`              | `groups/main/`    | read-write |
| `/workspace/extra/zettelkasten` | `~/.zettelkasten` | read-write |
| `/workspace/extra/dropbox`      | `~/Dropbox/Enzo`  | read-write |
| `/workspace/extra/books`        | `~/Dropbox/Books` | read-only  |

Key paths inside the container:

- `/workspace/project/store/messages.db` - SQLite database (read-write)
- `/workspace/project/store/messages.db` (registered_groups table) - Group config
- `/workspace/project/groups/` - All group folders

---

## Managing Groups

### Finding Available Groups

Available groups are provided in `/workspace/ipc/available_groups.json`:

```json
{
  "groups": [
    {
      "jid": "120363336345536173@g.us",
      "name": "Family Chat",
      "lastActivity": "2026-01-31T12:00:00.000Z",
      "isRegistered": false
    }
  ],
  "lastSync": "2026-01-31T12:00:00.000Z"
}
```

Groups are ordered by most recent activity. The list is synced from WhatsApp daily.

If a group the user mentions isn't in the list, request a fresh sync:

```bash
echo '{"type": "refresh_groups"}' > /workspace/ipc/tasks/refresh_$(date +%s).json
```

Then wait a moment and re-read `available_groups.json`.

**Fallback**: Query the SQLite database directly:

```bash
sqlite3 /workspace/project/store/messages.db "
  SELECT jid, name, last_message_time
  FROM chats
  WHERE jid LIKE '%@g.us' AND jid != '__group_sync__'
  ORDER BY last_message_time DESC
  LIMIT 10;
"
```

### Registered Groups Config

Groups are registered in the SQLite `registered_groups` table:

```json
{
  "1234567890-1234567890@g.us": {
    "name": "Family Chat",
    "folder": "whatsapp_family-chat",
    "trigger": "@Andy",
    "added_at": "2024-01-31T12:00:00.000Z"
  }
}
```

Fields:

- **Key**: The chat JID (unique identifier — WhatsApp, Telegram, Slack, Discord, etc.)
- **name**: Display name for the group
- **folder**: Channel-prefixed folder name under `groups/` for this group's files and memory
- **trigger**: The trigger word (usually same as global, but could differ)
- **requiresTrigger**: Whether `@trigger` prefix is needed (default: `true`). Set to `false` for solo/personal chats where all messages should be processed
- **isMain**: Whether this is the main control group (elevated privileges, no trigger required)
- **added_at**: ISO timestamp when registered

### Trigger Behavior

- **Main group** (`isMain: true`): No trigger needed — all messages are processed automatically
- **Groups with `requiresTrigger: false`**: No trigger needed — all messages processed (use for 1-on-1 or solo chats)
- **Other groups** (default): Messages must start with `@AssistantName` to be processed

### Adding a Group

1. Query the database to find the group's JID
2. Ask the user whether the group should require a trigger word before registering
3. Use the `register_group` MCP tool with the JID, name, folder, trigger, and the chosen `requiresTrigger` setting
4. Optionally include `containerConfig` for additional mounts
5. The group folder is created automatically: `/workspace/project/groups/{folder-name}/`
6. Optionally create an initial `CLAUDE.md` for the group

Folder naming convention — channel prefix with underscore separator:

- WhatsApp "Family Chat" → `whatsapp_family-chat`
- Telegram "Dev Team" → `telegram_dev-team`
- Discord "General" → `discord_general`
- Slack "Engineering" → `slack_engineering`
- Use lowercase, hyphens for the group name part

#### Adding Additional Directories for a Group

Groups can have extra directories mounted. Add `containerConfig` to their entry:

```json
{
  "1234567890@g.us": {
    "name": "Dev Team",
    "folder": "dev-team",
    "trigger": "@Andy",
    "added_at": "2026-01-31T12:00:00Z",
    "containerConfig": {
      "additionalMounts": [
        {
          "hostPath": "~/projects/webapp",
          "containerPath": "webapp",
          "readonly": false
        }
      ]
    }
  }
}
```

The directory will appear at `/workspace/extra/webapp` in that group's container.

#### Sender Allowlist

After registering a group, explain the sender allowlist feature to the user:

> This group can be configured with a sender allowlist to control who can interact with me. There are two modes:
>
> - **Trigger mode** (default): Everyone's messages are stored for context, but only allowed senders can trigger me with @{AssistantName}.
> - **Drop mode**: Messages from non-allowed senders are not stored at all.
>
> For closed groups with trusted members, I recommend setting up an allow-only list so only specific people can trigger me. Want me to configure that?

If the user wants to set up an allowlist, edit `~/.config/nanoclaw/sender-allowlist.json` on the host:

```json
{
  "default": { "allow": "*", "mode": "trigger" },
  "chats": {
    "<chat-jid>": {
      "allow": ["sender-id-1", "sender-id-2"],
      "mode": "trigger"
    }
  },
  "logDenied": true
}
```

Notes:

- Your own messages (`is_from_me`) explicitly bypass the allowlist in trigger checks. Bot messages are filtered out by the database query before trigger evaluation, so they never reach the allowlist.
- If the config file doesn't exist or is invalid, all senders are allowed (fail-open)
- The config file is on the host at `~/.config/nanoclaw/sender-allowlist.json`, not inside the container

### Removing a Group

1. Read `/workspace/project/data/registered_groups.json`
2. Remove the entry for that group
3. Write the updated JSON back
4. The group folder and its files remain (don't delete them)

### Listing Groups

Read `/workspace/project/data/registered_groups.json` and format it nicely.

---

## Global Memory

You can read and write to `/workspace/global/CLAUDE.md` for facts that should apply to all groups. Only update global memory when explicitly asked to "remember this globally" or similar.

---

## Scheduling for Other Groups

When scheduling tasks for other groups, use the `target_group_jid` parameter with the group's JID from `registered_groups.json`:

- `schedule_task(prompt: "...", schedule_type: "cron", schedule_value: "0 9 * * 1", target_group_jid: "120363336345536173@g.us")`

The task will run in that group's context with access to their files and memory.

---

## Projects

Projects live in `projects/`.
Active projects stay at the top level; completed ones go in `projects/completed/`.

Each project should have a `HISTORY.md` with timestamped entries tracking key events: opened, findings, decisions, and closure.
Log entries as work happens — don't backfill at the end.

When creating a project, `git init` it and commit as you go.
Use small, atomic commits to track iterations.

---

## Email

You have read-write access to Gmail via `mcp__gmail__*` tools.
Use these to read, search, send, and manage emails when asked.

---

## Engram — Persistent Memory

@/workspace/group/engram-repo/AGENTS.md

Fork: `agent-tre/engram` (private). Local clone: `/workspace/group/engram-repo/` (persists across rebuilds).

After writing or updating a memory, commit and push:

```bash
cd /workspace/group/engram-repo
git add .
git commit -m "<brief description>"
TOKEN=$(gh auth token) && git remote set-url origin "https://agent-tre:${TOKEN}@github.com/agent-tre/engram.git" && git push
```

---

## Agent Model Selection

For any coding task or coding research task (reading codebases, investigating bugs, proposing implementations, writing code, reviewing PRs), always use the latest Opus model available when spawning agents:

```
model: "opus"
```

Use Sonnet for non-coding tasks (general research, summarisation, scheduling, messaging).

---

## Task Scripts

For any recurring task, use `schedule_task`. Frequent agent invocations — especially multiple times a day — consume API credits and can risk account restrictions. If a simple check can determine whether action is needed, add a `script` — it runs first, and the agent is only called when the check passes. This keeps invocations to a minimum.

### How it works

1. You provide a bash `script` alongside the `prompt` when scheduling
2. When the task fires, the script runs first (30-second timeout)
3. Script prints JSON to stdout: `{ "wakeAgent": true/false, "data": {...} }`
4. If `wakeAgent: false` — nothing happens, task waits for next run
5. If `wakeAgent: true` — you wake up and receive the script's data + prompt

### Always test your script first

Before scheduling, run the script in your sandbox to verify it works:

```bash
bash -c 'node --input-type=module -e "
  const r = await fetch(\"https://api.github.com/repos/owner/repo/pulls?state=open\");
  const prs = await r.json();
  console.log(JSON.stringify({ wakeAgent: prs.length > 0, data: prs.slice(0, 5) }));
"'
```

### When NOT to use scripts

If a task requires your judgment every time (daily briefings, reminders, reports), skip the script — just use a regular prompt.

### Frequent task guidance

If a user wants tasks running more than ~2x daily and a script can't reduce agent wake-ups:

- Explain that each wake-up uses API credits and risks rate limits
- Suggest restructuring with a script that checks the condition first
- If the user needs an LLM to evaluate data, suggest using an API key with direct Anthropic API calls inside the script
- Help the user find the minimum viable frequency

## Bins Reminder

When sending the weekly bins reminder, use these emoji for bin types:

- 🔵 Recycling bin
- Use whatever is appropriate for other bin types unless specified
