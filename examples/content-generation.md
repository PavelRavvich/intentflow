# Workflow: Blog Content Generation

## Meta
version: 1.0
author: Content Team
requires: Claude with web search and computer use
estimated_time: 45 minutes
tags: content, marketing, seo, writing

## Context
Generate a comprehensive blog post for the company blog. The content should be 
well-researched, SEO-optimized, and ready for publication with minimal editing.

Target audience: Technical decision-makers (CTOs, engineering managers)
Brand voice: Professional but approachable, technically credible

---

## Step 1: Topic Research

### Task
Research the assigned topic thoroughly:

**Topic**: "Microservices vs Monolith in 2025: A Practical Decision Framework"

1. **Search for recent content** (last 6 months)
   - Industry reports and surveys
   - Case studies from major companies
   - Technical blog posts from thought leaders
   - Academic or research papers if relevant

2. **Identify key themes**
   - What are the current arguments for each approach?
   - What new factors have emerged (AI, edge computing, etc.)?
   - What mistakes do companies commonly make?

3. **Find data points**
   - Statistics on adoption rates
   - Performance benchmarks
   - Cost comparisons
   - Team size correlations

4. **Competitive content analysis**
   - What do top-ranking articles cover?
   - What's missing that we could add?

### Save as
`/tmp/workflow/step1_research.json`

Structure:
```json
{
  "sources": [{"url": "", "title": "", "key_points": []}],
  "themes": [],
  "statistics": [],
  "content_gaps": [],
  "recommended_angle": ""
}
```

### Success criteria
- Minimum 10 credible sources
- At least 5 data points with citations
- Clear recommended angle identified
- Sources are from last 12 months (preferably 6)

### Flexibility [guided]
If the topic is saturated, pivot to a more specific angle. 
For example: "Microservices for AI/ML Pipelines" or "Migration Patterns from Monolith".

### If something goes wrong
- Insufficient recent sources → expand to 12-18 months
- Conflicting information → note the controversy, present both sides

---

## Step 2: Outline Creation

### Task
Create a detailed outline based on research:

**Required sections:**
1. Hook/Introduction (why this matters now)
2. The Traditional Debate (brief history for context)
3. What's Changed in 2025 (new factors)
4. Decision Framework (the core value-add)
5. Real-World Scenarios (when to choose what)
6. Common Pitfalls (what to avoid)
7. Conclusion with actionable takeaway

**For each section:**
- 2-3 sentence summary of content
- Key points to cover
- Supporting data/examples to include
- Approximate word count

**Target total:** 2,500-3,000 words

### Save as
`/tmp/workflow/step2_outline.md`

### Success criteria
- All required sections present
- Total target word count is achievable
- Each section has clear purpose (no fluff)
- Data points are mapped to relevant sections
- Logical flow from section to section

### Flexibility [guided]
Sections can be reordered or combined if it improves flow.
Additional sections allowed if they add clear value.

---

## Step 3: First Draft

### Task
Write the complete first draft following the outline.

**Writing guidelines:**
- Use clear, direct language
- One idea per paragraph
- Technical accuracy is paramount
- Include specific examples, not just theory
- Use subheadings every 300-400 words
- Write for scanning (busy readers)

**Formatting:**
- H2 for main sections
- H3 for subsections
- Bullet points for lists (max 5-7 items)
- Code blocks for any technical examples
- Bold for key terms on first use

**SEO requirements:**
- Primary keyword in title, first paragraph, and 2-3 headings
- Secondary keywords naturally distributed
- Meta description (150-160 characters)
- Suggested URL slug

### Save as
`/tmp/workflow/step3_draft.md`

### Success criteria
- Word count within 2,500-3,000 range
- All outline sections covered
- No placeholder text ("[TODO]", "insert example")
- Proper markdown formatting
- Includes meta description and slug

### Constraints
- No AI-generated clichés ("In today's fast-paced world...")
- No unsupported claims (cite or remove)
- No competitor bashing (compare objectively)

### Flexibility [autonomous]
Writing style within brand guidelines is up to you. 
Be creative with examples and analogies.

---

## Step 4: Fact-Check and Edit

### Task
Review and improve the draft:

1. **Fact verification**
   - Verify all statistics are accurate and current
   - Check all company/product names are spelled correctly
   - Ensure technical claims are accurate
   - Verify links/sources are still accessible

2. **Readability pass**
   - Simplify complex sentences
   - Remove jargon or explain it
   - Check paragraph length (max 4-5 sentences)
   - Ensure transitions between sections

3. **SEO optimization**
   - Check keyword density (1-2% for primary)
   - Verify meta description length
   - Add internal link suggestions (placeholders)
   - Add alt-text suggestions for potential images

4. **Grammar and style**
   - Fix grammatical errors
   - Ensure consistent tense
   - Check for passive voice overuse
   - Verify consistent terminology

### Save as
- `/tmp/workflow/step4_edited.md` (clean version)
- `/tmp/workflow/step4_changes.md` (track changes summary)

### Success criteria
- All facts verified or flagged for human review
- Readability score: Grade 10 or lower (Flesch-Kincaid)
- No grammatical errors
- Changes documented

### If something goes wrong
- Cannot verify a statistic → flag it clearly with "[VERIFY]"
- Source no longer accessible → find alternative or remove claim

---

## Step 5: Visual Assets Specification

### Task
Create specifications for visual assets to accompany the article:

1. **Hero image concept**
   - Description for designer or stock photo search
   - Recommended dimensions
   - Alt text

2. **Diagrams needed**
   - Decision flowchart for the framework
   - Architecture comparison (monolith vs microservices)
   - Any data visualizations

3. **Pull quotes**
   - Select 2-3 compelling quotes from the text
   - These become shareable graphics

4. **Social media snippets**
   - Twitter/X post (280 chars)
   - LinkedIn post (100-150 words)
   - Key takeaway for Instagram/threads

### Save as
`/tmp/workflow/step5_assets.json`

### Success criteria
- Hero image concept is clear and actionable
- All diagrams have clear specifications
- Social snippets are engaging and accurate
- Alt text is descriptive and accessible

### Flexibility [autonomous]
If you can generate any of the diagrams yourself (mermaid, ASCII), do so.
Otherwise, provide detailed specs for a designer.

---

## Step 6: Final Package

### Task
Compile all deliverables into a final package:

1. **final_article.md** — publication-ready article
2. **meta.json** — SEO metadata, social snippets, keywords
3. **assets/** — folder with any generated diagrams
4. **brief.md** — instructions for designer (images needed)
5. **review_notes.md** — anything requiring human decision

### Save as
`/tmp/workflow/final_package/` (directory with all files)

### Success criteria
- All files present and properly formatted
- Article requires no further editing (except human preference)
- Clear handoff documentation

---

## Finalization

### After completion
1. Compress final package: `final_package.zip`
2. Move to `/home/user/content/blog/`
3. Clean up temp files

### Notification
Summary should include:
- Article title and word count
- Primary keyword and SEO readiness
- Number of sources cited
- Items flagged for human review
- Location of final package

### If any step failed
- Deliver partial package with clear indication of what's missing
- Prioritize: draft > outline > research (descending value)
