#!/usr/bin/env node

// Re-authorize Gmail OAuth — prints a URL you open in any browser.
// Usage: node scripts/gmail-reauth.mjs

import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const credDir = path.join(os.homedir(), '.gmail-mcp');
const keysPath = path.join(credDir, 'gcp-oauth.keys.json');
const tokensPath = path.join(credDir, 'credentials.json');

const keys = JSON.parse(fs.readFileSync(keysPath, 'utf-8'));
const { client_id, client_secret } = keys.installed;

const PORT = 3000;
const REDIRECT_URI = `http://localhost:${PORT}`;
const SCOPES = [
  'https://www.googleapis.com/auth/gmail.modify',
  'https://www.googleapis.com/auth/gmail.settings.basic',
];

const authUrl = new URL('https://accounts.google.com/o/oauth2/auth');
authUrl.searchParams.set('client_id', client_id);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('scope', SCOPES.join(' '));
authUrl.searchParams.set('access_type', 'offline');
authUrl.searchParams.set('prompt', 'consent'); // force new refresh token

console.log('\nOpen this URL in your browser:\n');
console.log(authUrl.toString());
console.log('\nWaiting for callback on port', PORT, '...\n');

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`);
  const code = url.searchParams.get('code');

  if (!code) {
    res.writeHead(400, { 'Content-Type': 'text/plain' });
    res.end('Missing code parameter');
    return;
  }

  try {
    const tokenRes = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        code,
        client_id,
        client_secret,
        redirect_uri: REDIRECT_URI,
        grant_type: 'authorization_code',
      }),
    });

    const tokens = await tokenRes.json();

    if (tokens.error) {
      console.error('Token exchange failed:', tokens);
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Token exchange failed: ' + tokens.error_description);
      server.close();
      process.exit(1);
    }

    fs.writeFileSync(tokensPath, JSON.stringify(tokens, null, 2));
    console.log('Tokens saved to', tokensPath);
    console.log('Done! You can restart NanoClaw now.');

    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end('<h1>Gmail re-authorized!</h1><p>You can close this tab.</p>');
    server.close();
    process.exit(0);
  } catch (err) {
    console.error('Error:', err);
    res.writeHead(500, { 'Content-Type': 'text/plain' });
    res.end('Error: ' + err.message);
    server.close();
    process.exit(1);
  }
});

server.listen(PORT);
