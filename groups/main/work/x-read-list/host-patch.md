# host.ts patch

In `.claude/skills/x-integration/host.ts`, add this case to the switch statement
(after the `x_quote` case, before `default: return false`):

```typescript
    case 'x_read_list':
      if (!data.listUrl) {
        result = { success: false, message: 'Missing listUrl' };
        break;
      }
      result = await runScript('read-list', {
        listUrl: data.listUrl,
        count: data.count ?? 10,
      });
      break;
```
