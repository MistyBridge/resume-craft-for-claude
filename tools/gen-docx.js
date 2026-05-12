#!/usr/bin/env node
/**
 * gen-docx.js — Generate a professional .docx resume from profile JSON.
 *
 * Uses the 'docx' npm package (github.com/dolanmedia/docx, 4k+ stars).
 *
 * Usage:
 *   node tools/gen-docx.js <profile.json> <output.docx>
 */

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel,
  AlignmentType, TabStopPosition, TabStopType,
  BorderStyle, convertInchesToTwip
} = require("docx");

// ── Helpers ──────────────────────────────────────────────────────────────

function blankLine() {
  return new Paragraph({ spacing: { after: 0, before: 0 } });
}

function sectionTitle(text) {
  return new Paragraph({
    text,
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 280, after: 120 },
    border: {
      bottom: { color: "333333", size: 2, style: BorderStyle.SINGLE, space: 4 }
    }
  });
}

function bullet(text) {
  return new Paragraph({
    text,
    bullet: { level: 0 },
    spacing: { after: 60, line: 276 }
  });
}

function tag(text) {
  return new TextRun({ text, font: "Microsoft YaHei", size: 19, color: "555555" });
}

// ── Header ───────────────────────────────────────────────────────────────

function buildHeader(basics) {
  const children = [
    new Paragraph({
      text: basics.name || "",
      heading: HeadingLevel.TITLE,
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 }
    })
  ];
  if (basics.title) {
    children.push(new Paragraph({
      text: basics.title,
      alignment: AlignmentType.CENTER,
      spacing: { after: 60 },
      style: "Subtitle"
    }));
  }
  const contact = [basics.email, basics.phone, basics.location, basics.github, basics.website]
    .filter(Boolean).join("  ·  ");
  if (contact) {
    children.push(new Paragraph({
      text: contact,
      alignment: AlignmentType.CENTER,
      spacing: { after: 200 }
    }));
  }
  children.push(blankLine());
  return children;
}

// ── Summary ───────────────────────────────────────────────────────────────

function buildSummary(summary) {
  const text = summary?.polished || summary?.raw;
  if (!text) return [];
  return [
    sectionTitle("个人总结"),
    new Paragraph({ text, spacing: { after: 120 } })
  ];
}

// ── Experience ────────────────────────────────────────────────────────────

function buildExperience(experience) {
  if (!experience?.length) return [];
  const result = [sectionTitle("工作经历")];
  for (const exp of experience) {
    result.push(new Paragraph({
      children: [
        new TextRun({ text: exp.company || "", bold: true, size: 22 }),
        new TextRun({ text: exp.title ? `  ·  ${exp.title}` : "", size: 22 }),
        new TextRun({ text: exp.start_date ? `    ${exp.start_date} — ${exp.end_date || "至今"}` : "", size: 19, color: "888888" })
      ],
      tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      spacing: { before: 160, after: 40 }
    }));
    if (exp.bullets) {
      for (const b of exp.bullets) {
        result.push(bullet(b.polished || b.raw));
      }
    }
    if (exp.technologies?.length) {
      result.push(new Paragraph({
        children: [new TextRun({ text: "技术栈：", bold: true, size: 19 })].concat(
          exp.technologies.map(t => tag(` ${t} `))
        ),
        spacing: { before: 80, after: 40 }
      }));
    }
  }
  return result;
}

// ── Projects ──────────────────────────────────────────────────────────────

function buildProjects(projects) {
  if (!projects?.length) return [];
  const result = [sectionTitle("项目作品")];
  for (const p of projects) {
    result.push(new Paragraph({
      children: [
        new TextRun({ text: p.name || "", bold: true, size: 22 }),
        new TextRun({ text: p.role ? `  ·  ${p.role}` : "", size: 19, color: "888888" })
      ],
      spacing: { before: 140, after: 40 }
    }));
    if (p.description) {
      result.push(new Paragraph({ text: p.description, spacing: { after: 60 } }));
    }
    if (p.technologies?.length) {
      result.push(new Paragraph({
        children: p.technologies.map(t => tag(` ${t} `)),
        spacing: { after: 40 }
      }));
    }
  }
  return result;
}

// ── Skills ────────────────────────────────────────────────────────────────

function buildSkills(skills) {
  if (!skills) return [];
  const result = [sectionTitle("专业技能")];
  if (skills.hard_skills?.length) {
    const items = skills.hard_skills.map(s =>
      s.proficiency ? `${s.name} · ${s.proficiency}` : s.name
    );
    result.push(new Paragraph({
      children: items.map(t => tag(` ${t} `)),
      spacing: { after: 80 }
    }));
  }
  if (skills.tools?.length) {
    result.push(new Paragraph({
      children: [new TextRun({ text: "工具：", bold: true, size: 19 })].concat(
        skills.tools.map(t => tag(` ${t} `))
      ),
      spacing: { after: 80 }
    }));
  }
  if (skills.languages?.length) {
    const langs = skills.languages.map(l => `${l.name} (${l.level})`).join(" · ");
    result.push(new Paragraph({
      children: [new TextRun({ text: `语言：${langs}`, size: 19 })],
      spacing: { after: 80 }
    }));
  }
  return result;
}

// ── Education ─────────────────────────────────────────────────────────────

function buildEducation(education) {
  if (!education?.length) return [];
  const result = [sectionTitle("教育背景")];
  for (const edu of education) {
    const parts = [edu.school, edu.degree, edu.major].filter(Boolean).join(" · ");
    result.push(new Paragraph({
      children: [
        new TextRun({ text: parts, bold: true, size: 22 }),
        new TextRun({ text: edu.start_date ? `    ${edu.start_date} — ${edu.end_date || "至今"}` : "", size: 19, color: "888888" })
      ],
      spacing: { after: 60 }
    }));
    if (edu.honors?.length) {
      result.push(new Paragraph({
        children: [new TextRun({ text: "荣誉：" + edu.honors.join(" · "), size: 19, color: "555555" })],
        spacing: { after: 40 }
      }));
    }
  }
  return result;
}

// ── Additional ────────────────────────────────────────────────────────────

function buildAdditional(additional) {
  if (!additional) return [];
  const items = [];
  if (additional.certifications?.length)
    items.push("证书：" + additional.certifications.join(" · "));
  if (additional.publications?.length)
    items.push("发表：" + additional.publications.join(" · "));
  if (additional.interests?.length)
    items.push("兴趣：" + additional.interests.join(" · "));
  if (!items.length) return [];
  return [
    sectionTitle("其他信息"),
    new Paragraph({ text: items.join("    "), spacing: { after: 120 } })
  ];
}

// ── Main ──────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: node gen-docx.js <profile.json> <output.docx>");
    process.exit(1);
  }
  const [inputPath, outputPath] = args;

  if (!fs.existsSync(inputPath)) {
    console.error(`Error: Profile not found: ${inputPath}`);
    process.exit(1);
  }

  const profile = JSON.parse(fs.readFileSync(inputPath, "utf-8"));
  const { basics, summary, experience, projects, skills, education, additional } = profile;

  const doc = new Document({
    sections: [{
      properties: {
        page: {
          margin: {
            top: convertInchesToTwip(0.7),
            bottom: convertInchesToTwip(0.6),
            left: convertInchesToTwip(0.8),
            right: convertInchesToTwip(0.8)
          }
        }
      },
      children: [
        ...buildHeader(basics),
        ...buildSummary(summary),
        ...buildExperience(experience),
        ...buildProjects(projects),
        ...buildSkills(skills),
        ...buildEducation(education),
        ...buildAdditional(additional)
      ]
    }]
  });

  fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  console.log(`DOCX exported: ${outputPath}`);
}

main().catch(err => {
  console.error("Fatal:", err.message);
  process.exit(1);
});
