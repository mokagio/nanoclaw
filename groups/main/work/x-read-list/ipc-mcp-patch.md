# ipc-mcp-stdio.ts patch

In `container/agent-runner/src/ipc-mcp-stdio.ts`, add this BEFORE the line
`// Start the stdio transport`:

```typescript
server.tool(
  'x_read_list',
  'Read the latest tweets from an X (Twitter) list. Main group only. Returns tweet text, author, handle, URL and timestamp.',
  {
    list_url: z
      .string()
      .describe('The X list URL (e.g., https://x.com/i/lists/123456789)'),
    count: z
      .number()
      .int()
      .min(1)
      .max(50)
      .default(10)
      .describe('Number of tweets to return (default: 10, max: 50)'),
  },
  async (args) => {
    if (!isMain) {
      return {
        content: [
          {
            type: 'text' as const,
            text: 'Only the main group can interact with X.',
          },
        ],
        isError: true,
      };
    }

    const requestId = `xreadlist-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    writeXIpcFile({
      type: 'x_read_list',
      requestId,
      listUrl: args.list_url,
      count: args.count,
      groupFolder,
      timestamp: new Date().toISOString(),
    });

    const result = await waitForXResult(requestId);
    if (!result.success) {
      return {
        content: [{ type: 'text' as const, text: result.message }],
        isError: true,
      };
    }

    // Format tweets as readable text
    const data = result.data as {
      tweets: Array<{
        author: string;
        handle: string;
        text: string;
        url: string;
        timeAgo: string;
      }>;
      listName: string | null;
      count: number;
    };
    const lines: string[] = [];
    if (data.listName) lines.push(`List: ${data.listName}\n`);
    data.tweets.forEach((t, i) => {
      lines.push(`${i + 1}. ${t.author} (${t.handle}) · ${t.timeAgo}`);
      if (t.text) lines.push(`   ${t.text}`);
      lines.push(`   ${t.url}`);
      lines.push('');
    });

    return {
      content: [{ type: 'text' as const, text: lines.join('\n') }],
    };
  },
);
```
