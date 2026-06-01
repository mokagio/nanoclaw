# Ideas from Podcasts

This group receives daily summaries connecting Gio's podcast listening with notes from his zettelkasten.

## Daily Task (9am Melbourne)

Review yesterday's podcast listening history and connect episodes with relevant zettelkasten notes.

### Process

1. Read the most recent podcast history from `/workspace/extra/pocket-casts-history/`
2. Find yesterday's file based on current date
3. Look for episodes with `status` `completed` or with `progress_percent` > 85
4. For the main completed episode(s):
   - Note podcast title and episode title
   - Search `/workspace/extra/zettelkasten/zettelkasten/` for notes that connect to the topics
5. Send a message with format:

```
Yesterday you listened to [summary of podcasts].

Here's a note that connects with [episode]: [note title]

The connection: [explain the link]
```

### Formatting

- Use WhatsApp formatting (single asterisks for bold, underscores for italic)
- No emojis (Gio's preference for solo groups)
- Keep it concise

### Data Sources

- Podcast history: `/workspace/extra/pocket-casts-history/YYYY/MM/DD.json` (use current year)
- Zettelkasten: `/workspace/extra/zettelkasten/zettelkasten/*.md`
