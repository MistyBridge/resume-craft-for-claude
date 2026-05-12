#!/usr/bin/env node
// @MistyBridge — Resume Craft
/**
 * gen-pdf.js — Convert HTML resume to PDF using Puppeteer.
 *
 * Uses Puppeteer (github.com/puppeteer/puppeteer, 88k+ stars).
 *
 * Usage:
 *   node tools/gen-pdf.js <input.html> <output.pdf>
 */

const fs = require("fs");
const path = require("path");
const puppeteer = require("puppeteer");

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node gen-pdf.js <input.html> <output.pdf>");
    process.exit(1);
  }
  const [inputPath, outputPath] = args;

  if (!fs.existsSync(inputPath)) {
    console.error(`Error: Input file not found: ${inputPath}`);
    process.exit(1);
  }

  const html = fs.readFileSync(inputPath, "utf-8");
  const outDir = path.dirname(path.resolve(outputPath));
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setContent(html, { waitUntil: "networkidle0" });
  await page.pdf({
    path: outputPath,
    format: "A4",
    margin: { top: "1.8cm", bottom: "1.5cm", left: "2cm", right: "2cm" },
    printBackground: true
  });
  await browser.close();
  console.log(`PDF exported: ${outputPath}`);
}

main().catch(err => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
