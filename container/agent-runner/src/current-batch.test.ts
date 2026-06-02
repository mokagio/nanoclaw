import { describe, it, expect } from 'bun:test';

import {
  setCurrentInReplyTo,
  clearCurrentInReplyTo,
  recordSentContent,
  wasSentThisTurn,
} from './current-batch.js';

describe('sent-this-turn dedup tracking', () => {
  it('matches content recorded this turn (trimmed)', () => {
    setCurrentInReplyTo('m1');
    recordSentContent('  PDF done — here it is  ');
    expect(wasSentThisTurn('PDF done — here it is')).toBe(true);
  });

  it('does not match content not sent', () => {
    setCurrentInReplyTo('m1');
    recordSentContent('On it');
    expect(wasSentThisTurn('the actual answer')).toBe(false);
  });

  it('resets at turn start so prior-turn content does not leak', () => {
    setCurrentInReplyTo('m1');
    recordSentContent('answer A');
    expect(wasSentThisTurn('answer A')).toBe(true);

    setCurrentInReplyTo('m2'); // next turn begins
    expect(wasSentThisTurn('answer A')).toBe(false);

    clearCurrentInReplyTo();
  });
});
