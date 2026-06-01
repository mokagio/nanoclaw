# How to apply

1. Copy script:
   cp /workspace/group/work/x-read-list/read-list.ts .claude/skills/x-integration/scripts/read-list.ts

2. Copy tests:
   cp /workspace/group/work/x-read-list/read-list.test.ts .claude/skills/x-integration/scripts/read-list.test.ts

3. Apply host patch (see host-patch.md) to .claude/skills/x-integration/host.ts

4. Apply IPC tool patch (see ipc-mcp-patch.md) to container/agent-runner/src/ipc-mcp-stdio.ts

5. Rebuild + restart:
   ./container/build.sh && npm run build && launchctl kickstart -k gui/$(id -u)/com.nanoclaw

Then tell Enzo "applied, test it".
