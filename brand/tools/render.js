// HTML document → PDF (and an optional full-page PNG preview), with the brand fonts embedded.
// Usage: NODE_PATH=$(npm root -g) node brand/tools/render.js <input.html> <output.pdf> [preview.png]
// Needs Playwright with Chromium (`npm i -g playwright`, then `npx playwright install chromium`).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [, , input, outPdf, outPng] = process.argv;
  if (!input || !outPdf) {
    console.error('usage: node render.js <input.html> <output.pdf> [preview.png]');
    process.exit(1);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1000, height: 1400 }, deviceScaleFactor: 1.5 });
  await page.goto('file://' + path.resolve(input));
  await page.evaluate(() => document.fonts.ready);
  if (outPng) await page.screenshot({ path: outPng, fullPage: true });
  await page.pdf({ path: outPdf, preferCSSPageSize: true, printBackground: true });
  await browser.close();
  console.log('wrote', outPdf, outPng || '');
})();
