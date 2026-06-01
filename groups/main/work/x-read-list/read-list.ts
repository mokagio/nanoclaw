#!/usr/bin/env npx tsx
/**
 * X Integration - Read List
 * Reads the latest tweets from an X (Twitter) list.
 * Usage: echo '{"listUrl":"https://x.com/i/lists/123456","count":10}' | npx tsx read-list.ts
 */

import {
  getBrowserContext,
  runScript,
  config,
  ScriptResult,
} from '../lib/browser.js';

export interface Tweet {
  author: string;
  handle: string;
  text: string;
  url: string;
  datetime: string; // ISO timestamp from <time datetime="...">
  timeAgo: string; // Human label e.g. "2h"
}

interface ReadListInput {
  listUrl: string;
  count?: number; // How many tweets to return. Default: 10
}

interface ReadListResult extends ScriptResult {
  data?: {
    tweets: Tweet[];
    listName: string | null;
    count: number;
  };
}

export async function readList(input: ReadListInput): Promise<ReadListResult> {
  const { listUrl, count = 10 } = input;

  if (!listUrl) {
    return { success: false, message: 'Missing listUrl' };
  }

  let context = null;
  try {
    context = await getBrowserContext();
    const page = context.pages()[0] || (await context.newPage());

    await page.goto(listUrl, {
      timeout: config.timeouts.navigation,
      waitUntil: 'domcontentloaded',
    });
    await page.waitForTimeout(config.timeouts.pageLoad);

    // Check if logged in
    const isLoggedIn = await page
      .locator('[data-testid="SideNav_AccountSwitcher_Button"]')
      .isVisible()
      .catch(() => false);
    if (!isLoggedIn) {
      return {
        success: false,
        message: 'X login expired. Run setup to re-authenticate.',
      };
    }

    // Get list name from heading
    const listName = await page
      .locator('[data-testid="primaryColumn"] h2')
      .first()
      .textContent()
      .catch(() => null);

    // Wait for at least one tweet to appear
    await page
      .waitForSelector('article[data-testid="tweet"]', {
        timeout: config.timeouts.elementWait * 3,
      })
      .catch(() => null);

    const tweets: Tweet[] = [];
    const seen = new Set<string>();
    let scrollAttempts = 0;
    const maxScrolls = 8;

    while (tweets.length < count && scrollAttempts < maxScrolls) {
      const articles = page.locator('article[data-testid="tweet"]');
      const total = await articles.count();

      for (let i = 0; i < total; i++) {
        if (tweets.length >= count) break;

        const article = articles.nth(i);

        // Use status link as stable dedup key
        const statusHref = await article
          .locator('a[href*="/status/"]')
          .first()
          .getAttribute('href')
          .catch(() => null);
        if (!statusHref || seen.has(statusHref)) continue;
        seen.add(statusHref);

        // Tweet text (may be empty for media-only tweets)
        const text =
          (await article
            .locator('[data-testid="tweetText"]')
            .first()
            .textContent()
            .catch(() => '')) ?? '';

        // Author block — X renders it as "Display Name@handle"
        const userNameBlock =
          (await article
            .locator('[data-testid="User-Name"]')
            .first()
            .textContent()
            .catch(() => '')) ?? '';
        const handleMatch = userNameBlock.match(/@([A-Za-z0-9_]+)/);
        const handle = handleMatch ? `@${handleMatch[1]}` : '';
        const author = userNameBlock.replace(/@[A-Za-z0-9_]+/g, '').trim();

        // Timestamp
        const timeEl = article.locator('time').first();
        const datetime =
          (await timeEl.getAttribute('datetime').catch(() => '')) ?? '';
        const timeAgo = (await timeEl.textContent().catch(() => '')) ?? '';

        const url = `https://x.com${statusHref}`;

        tweets.push({
          author,
          handle,
          text: text.trim(),
          url,
          datetime,
          timeAgo: timeAgo.trim(),
        });
      }

      if (tweets.length < count) {
        await page.evaluate(() => window.scrollBy(0, 1000));
        await page.waitForTimeout(2000);
        scrollAttempts++;
      }
    }

    if (tweets.length === 0) {
      return {
        success: false,
        message:
          'No tweets found. List may be empty or selectors may need updating.',
      };
    }

    return {
      success: true,
      message: `Read ${tweets.length} tweet${tweets.length !== 1 ? 's' : ''} from list`,
      data: {
        tweets,
        listName: listName?.trim() ?? null,
        count: tweets.length,
      },
    };
  } finally {
    if (context) await context.close();
  }
}

runScript<ReadListInput>(readList);
