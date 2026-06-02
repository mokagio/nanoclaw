/**
 * Per-batch context the poll loop publishes for downstream consumers
 * (MCP tools, etc.) that don't sit on the poll-loop's call stack.
 *
 * Today the only field is `inReplyTo` — the id of the first inbound
 * message in the batch the agent is currently processing. MCP tools like
 * `send_message` and `send_file` read this and stamp it onto the outbound
 * row so the host's a2a return-path routing can correlate replies back to
 * the originating session.
 *
 * This is module-level state on purpose: the agent-runner is single-process
 * and processes one batch at a time. Poll-loop calls `setCurrentInReplyTo`
 * before invoking the provider and `clearCurrentInReplyTo` after the batch
 * completes (or errors out).
 */
let currentInReplyTo: string | null = null;

// Contents already delivered this turn via send_message. Used to drop a
// final-output <message> block that exactly repeats a mid-turn send_message —
// the agent sometimes pushes its final result through both paths, which lands
// as a duplicate reply. Keyed by trimmed text; reset at each turn start.
const sentThisTurn = new Set<string>();

export function setCurrentInReplyTo(id: string | null): void {
  currentInReplyTo = id;
  sentThisTurn.clear();
}

export function clearCurrentInReplyTo(): void {
  currentInReplyTo = null;
}

export function getCurrentInReplyTo(): string | null {
  return currentInReplyTo;
}

export function recordSentContent(text: string): void {
  sentThisTurn.add(text.trim());
}

export function wasSentThisTurn(text: string): boolean {
  return sentThisTurn.has(text.trim());
}

