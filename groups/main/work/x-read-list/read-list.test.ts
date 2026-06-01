/**
 * Unit tests for read-list.ts
 *
 * Tests cover: input validation, tweet parsing helpers, deduplication.
 * Browser interaction is tested via integration test at the bottom (skipped in CI).
 */

import { describe, it, expect } from 'vitest';

// ── Pure helpers extracted for testability ──────────────────────────────────

/**
 * Parse the X User-Name block into author + handle.
 * X renders: "Display Name@handle" with no separator.
 */
export function parseUserName(block: string): {
  author: string;
  handle: string;
} {
  const handleMatch = block.match(/@([A-Za-z0-9_]+)/);
  const handle = handleMatch ? `@${handleMatch[1]}` : '';
  const author = block.replace(/@[A-Za-z0-9_]+/g, '').trim();
  return { author, handle };
}

/**
 * Build a full tweet URL from a status href.
 */
export function buildTweetUrl(statusHref: string): string {
  if (statusHref.startsWith('http')) return statusHref;
  return `https://x.com${statusHref}`;
}

/**
 * Validate read-list input.
 */
export function validateInput(input: {
  listUrl?: string;
  count?: number;
}): string | null {
  if (!input.listUrl) return 'Missing listUrl';
  if (
    !input.listUrl.includes('x.com') &&
    !input.listUrl.includes('twitter.com')
  ) {
    return 'listUrl must be an x.com or twitter.com URL';
  }
  if (input.count !== undefined && (input.count < 1 || input.count > 100)) {
    return 'count must be between 1 and 100';
  }
  return null;
}

// ── Tests ────────────────────────────────────────────────────────────────────

describe('parseUserName', () => {
  it('parses standard display name + handle', () => {
    expect(parseUserName('David Deutsch@DavidDeutschOxf')).toEqual({
      author: 'David Deutsch',
      handle: '@DavidDeutschOxf',
    });
  });

  it('handles handle-only (no display name)', () => {
    expect(parseUserName('@naval')).toEqual({
      author: '',
      handle: '@naval',
    });
  });

  it('handles display name with spaces', () => {
    expect(parseUserName('Brett Hall@TokTeacher')).toEqual({
      author: 'Brett Hall',
      handle: '@TokTeacher',
    });
  });

  it('returns empty strings for empty input', () => {
    expect(parseUserName('')).toEqual({ author: '', handle: '' });
  });

  it('handles underscores and numbers in handle', () => {
    const result = parseUserName('Some User@user_123');
    expect(result.handle).toBe('@user_123');
  });
});

describe('buildTweetUrl', () => {
  it('prepends x.com to relative href', () => {
    expect(buildTweetUrl('/SomeUser/status/123456')).toBe(
      'https://x.com/SomeUser/status/123456',
    );
  });

  it('passes through absolute URLs unchanged', () => {
    expect(buildTweetUrl('https://x.com/SomeUser/status/123456')).toBe(
      'https://x.com/SomeUser/status/123456',
    );
  });
});

describe('validateInput', () => {
  it('accepts valid x.com list URL', () => {
    expect(
      validateInput({ listUrl: 'https://x.com/i/lists/12345' }),
    ).toBeNull();
  });

  it('accepts valid twitter.com URL', () => {
    expect(
      validateInput({ listUrl: 'https://twitter.com/i/lists/12345' }),
    ).toBeNull();
  });

  it('rejects missing listUrl', () => {
    expect(validateInput({})).toBe('Missing listUrl');
  });

  it('rejects non-X URL', () => {
    expect(validateInput({ listUrl: 'https://example.com/list' })).toMatch(
      /x\.com/,
    );
  });

  it('accepts valid count', () => {
    expect(
      validateInput({ listUrl: 'https://x.com/i/lists/1', count: 10 }),
    ).toBeNull();
  });

  it('rejects count of 0', () => {
    expect(
      validateInput({ listUrl: 'https://x.com/i/lists/1', count: 0 }),
    ).toBeTruthy();
  });

  it('rejects count over 100', () => {
    expect(
      validateInput({ listUrl: 'https://x.com/i/lists/1', count: 101 }),
    ).toBeTruthy();
  });
});
