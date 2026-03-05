#!/usr/bin/env node

/**
 * Humanizer Pro - Regression Test Suite
 * 
 * Tests both POSITIVE (human-like text should pass) and NEGATIVE (AI-tell text should flag).
 * Run: node scripts/test-regression.js
 */

const path = require('path');

// Import detection functions by requiring the main script's logic
// We re-declare core functions here for test isolation

// --- Core detection functions (mirrored from humanize.js) ---

const TIER1_WORDS = [
  'bustling', 'catalyst', 'cornerstone', 'crucial', 'comprehensive',
  'delve', 'delving', 'embark', 'empower', 'enduring', 'groundbreaking',
  'harness', 'indelible', 'invaluable', 'leverage', 'meticulous',
  'meticulously', 'multifaceted', 'myriad', 'nestled', 'paramount',
  'pivotal', 'realm', 'reimagine', 'robust', 'seamless', 'synergy',
  'tapestry', 'testament', 'transformative', 'vibrant'
];

const TIER1_PHRASES = [
  'delve into', 'embark on a journey', 'harness the power',
  'in the realm of', 'serves as a testament', 'stands as a testament',
  'marking a pivotal moment', 'plays a crucial role',
  'the evolving landscape', 'the intricate tapestry',
  'in today\'s digital age', 'in today\'s fast-paced',
  'without further ado', 'it is worth noting',
  'maintains an active social media presence',
  'maintains a strong digital presence',
  'based on available information'
];

const CHATBOT_PHRASES = [
  'i hope this helps', 'great question', 'certainly!', 'of course!',
  'you\'re absolutely right', 'would you like', 'let me know',
  'here is a', 'here are some', 'maintains an active social media presence',
  'maintains a strong digital presence', 'not widely documented',
  'based on available information'
];

const FILLER_PHRASES = [
  'in order to', 'due to the fact that', 'at this point in time',
  'in the event that', 'for the purpose of', 'in spite of the fact that',
  'with regard to', 'in light of the fact that'
];

const LLM_ARTIFACT_PATTERNS = [
  /turn0search\d+/gi,
  /oaicite:\d+/gi,
  /contentReference\[oaicite:\d+\]/gi,
  /utm_source=(chatgpt\.com|openai|copilot\.com)/gi,
  /referrer=grok\.com/gi,
  /\[attached_file:\d+\]/gi,
  /\[INSERT_[A-Z_]+\]/gi,
  /oai_citation:\d+/gi
];

const MARKDOWN_PATTERNS = [
  /\*\*[^*]+\*\*/g,
  /^#{1,6}\s+/gm,
  /\[([^\]]+)\]\(([^)]+)\)/g,
  /```[\s\S]*?```/g
];

// --- Helper functions ---

function detectTier1(text) {
  const lowerText = text.toLowerCase();
  const words = TIER1_WORDS.filter(w => new RegExp(`\\b${w}\\b`, 'i').test(text));
  const phrases = TIER1_PHRASES.filter(p => lowerText.includes(p));
  return { words, phrases };
}

function detectChatbot(text) {
  const lowerText = text.toLowerCase();
  return CHATBOT_PHRASES.filter(p => lowerText.includes(p));
}

function detectFiller(text) {
  const lowerText = text.toLowerCase();
  return FILLER_PHRASES.filter(p => lowerText.includes(p));
}

function detectLLMArtifacts(text) {
  const matches = [];
  for (const pattern of LLM_ARTIFACT_PATTERNS) {
    pattern.lastIndex = 0;
    const found = text.match(pattern);
    if (found) matches.push(...found);
  }
  return matches;
}

function detectMarkdown(text) {
  const matches = [];
  for (const pattern of MARKDOWN_PATTERNS) {
    pattern.lastIndex = 0;
    const found = text.match(pattern);
    if (found) matches.push(...found.slice(0, 5));
  }
  return matches;
}

function detectEmDashes(text) {
  return (text.match(/—/g) || []).length;
}

// --- Test framework ---

let passed = 0;
let failed = 0;
const failures = [];

function assert(condition, testName, detail) {
  if (condition) {
    passed++;
    console.log(`  ✅ ${testName}`);
  } else {
    failed++;
    failures.push({ testName, detail });
    console.log(`  ❌ ${testName}`);
    if (detail) console.log(`     → ${detail}`);
  }
}

// ========================================
// NEGATIVE TESTS (should detect AI tells)
// ========================================

console.log('\n=== NEGATIVE TESTS (AI text → should flag) ===\n');

// Tier 1 vocabulary detection
console.log('--- Tier 1 Vocabulary ---');
assert(
  detectTier1('This serves as a testament to the vibrant tapestry of innovation.').words.length >= 3,
  'Detects multiple Tier 1 words (testament, vibrant, tapestry)',
  `Found: ${detectTier1('This serves as a testament to the vibrant tapestry of innovation.').words.join(', ')}`
);

assert(
  detectTier1('We must delve into the robust framework to leverage synergy.').words.length >= 4,
  'Detects delve, robust, leverage, synergy'
);

assert(
  detectTier1('The meticulous approach was meticulously planned.').words.length >= 1,
  'Detects meticulous/meticulously'
);

// Tier 1 phrase detection
console.log('\n--- Tier 1 Phrases ---');
assert(
  detectTier1('This stands as a testament to their vision.').phrases.length >= 1,
  'Detects "stands as a testament"'
);

assert(
  detectTier1('In today\'s digital age, we must adapt.').phrases.length >= 1,
  'Detects "in today\'s digital age"'
);

assert(
  detectTier1('She maintains an active social media presence with 500K followers.').phrases.length >= 1,
  'Detects "maintains an active social media presence" (new)'
);

// Chatbot artifacts
console.log('\n--- Chatbot Artifacts ---');
assert(
  detectChatbot('Great question! I hope this helps! Let me know if you need more.').length >= 3,
  'Detects chatbot triple-tap (Great question + I hope this helps + Let me know)'
);

assert(
  detectChatbot('Details about his personal life are not widely documented.').length >= 1,
  'Detects "not widely documented" (new cutoff disclaimer pattern)'
);

assert(
  detectChatbot('Based on available information, the company was founded in 1995.').length >= 1,
  'Detects "based on available information" (new cutoff disclaimer)'
);

// Filler phrases
console.log('\n--- Filler Phrases ---');
assert(
  detectFiller('In order to achieve this goal, due to the fact that resources are limited...').length >= 2,
  'Detects "in order to" and "due to the fact that"'
);

// LLM reference artifacts (Pattern 27 - NEW)
console.log('\n--- LLM Reference Artifacts (Pattern 27) ---');
assert(
  detectLLMArtifacts('The school was established in 1990. turn0search0 It offers various programs. turn0search1').length >= 2,
  'Detects turn0search artifacts'
);

assert(
  detectLLMArtifacts('contentReference[oaicite:0]{index=0} This is a test.').length >= 1,
  'Detects oaicite artifacts'
);

assert(
  detectLLMArtifacts('Source: https://example.com?utm_source=chatgpt.com').length >= 1,
  'Detects utm_source=chatgpt.com in URLs'
);

assert(
  detectLLMArtifacts('Source: https://example.com?utm_source=copilot.com').length >= 1,
  'Detects utm_source=copilot.com in URLs'
);

assert(
  detectLLMArtifacts('More information can be found here.[attached_file:1]').length >= 1,
  'Detects [attached_file:1] Perplexity artifacts'
);

assert(
  detectLLMArtifacts('Please fill in [INSERT_SOURCE_URL] and [INSERT_DATE_HERE].').length >= 2,
  'Detects [INSERT_X_HERE] placeholder templates'
);

assert(
  detectLLMArtifacts('See: https://example.com?referrer=grok.com for details.').length >= 1,
  'Detects referrer=grok.com in URLs'
);

// Markdown leakage (Pattern 26 - NEW)
console.log('\n--- Markdown Leakage (Pattern 26) ---');
assert(
  detectMarkdown('The **important** thing is that **bold text** appears often.').length >= 2,
  'Detects **bold** markdown syntax'
);

assert(
  detectMarkdown('## Section Header\nSome content here.\n## Another Section').length >= 2,
  'Detects ## header markdown syntax'
);

assert(
  detectMarkdown('Read more at [our blog](https://example.com/blog).').length >= 1,
  'Detects [text](url) markdown links'
);

// Em dash overuse
console.log('\n--- Em Dash Overuse ---');
assert(
  detectEmDashes('This is the point — and it matters — because without it — everything falls apart — including the argument — and the conclusion — period.') > 5,
  'Detects excessive em dash usage (>5)'
);

// ========================================
// POSITIVE TESTS (human text → should NOT flag)
// ========================================

console.log('\n\n=== POSITIVE TESTS (Human text → should pass clean) ===\n');

// Clean human-like text
console.log('--- Clean Human Writing ---');

const humanText1 = 'Solar panel costs dropped 90% between 2010 and 2023. That single fact explains why adoption took off. It stopped being an ideological choice and became an economic one.';
assert(
  detectTier1(humanText1).words.length === 0,
  'Human text has zero Tier 1 words'
);
assert(
  detectChatbot(humanText1).length === 0,
  'Human text has zero chatbot artifacts'
);
assert(
  detectFiller(humanText1).length === 0,
  'Human text has zero filler phrases'
);

const humanText2 = 'I tried the recipe last night. Burned the garlic, obviously. But the rest turned out okay. My kids even asked for seconds, which never happens with anything green.';
assert(
  detectTier1(humanText2).words.length === 0,
  'Casual human text has zero Tier 1 words'
);
assert(
  detectLLMArtifacts(humanText2).length === 0,
  'Casual human text has zero LLM artifacts'
);

const humanText3 = 'The company was founded in 1994, according to its registration documents. Revenue hit $12M last year, mostly from the European market.';
assert(
  detectTier1(humanText3).words.length === 0,
  'Factual human text has zero Tier 1 words'
);

// Ensure legitimate uses don't false-positive
console.log('\n--- False Positive Guard ---');
assert(
  detectTier1('The building is robust enough to withstand earthquakes.').words.length >= 1,
  'Note: "robust" flags even in legitimate structural context (expected - Tier 1 is strict)',
  'This is by design. Tier 1 words always flag; context is for human review.'
);

assert(
  detectMarkdown('Use **bold** in your CSS for emphasis.').length >= 1,
  'Note: Technical markdown discussion flags (expected in non-code contexts)'
);

assert(
  detectLLMArtifacts('Normal URL: https://example.com?ref=newsletter&source=email').length === 0,
  'Normal UTM params (non-AI) do NOT flag'
);

assert(
  detectEmDashes('She arrived — finally.') <= 1,
  'Single em dash is fine (human-normal usage)'
);

// ========================================
// COMBINED SCORING TESTS
// ========================================

console.log('\n\n=== COMBINED SCORING TESTS ===\n');

const aiHeavy = 'Great question! In today\'s rapidly evolving digital landscape, we must delve into the intricate tapestry of innovation. This transformative approach leverages robust synergies and serves as a testament to our commitment. Additionally, the groundbreaking framework harnesses the power of multifaceted solutions. I hope this helps!';
const aiDetection = detectTier1(aiHeavy);
const aiChatbot = detectChatbot(aiHeavy);
assert(
  aiDetection.words.length >= 7,
  `Heavy AI text flags 7+ Tier 1 words (found ${aiDetection.words.length}: ${aiDetection.words.join(', ')})`
);
assert(
  aiChatbot.length >= 2,
  `Heavy AI text flags 2+ chatbot phrases (found ${aiChatbot.length})`
);

const humanNatural = 'I kept thinking about what she said. Not because it was profound or anything — just because it stuck. Sometimes the obvious stuff is the hardest to hear. Anyway, I made coffee and moved on.';
const humanDetection = detectTier1(humanNatural);
assert(
  humanDetection.words.length === 0,
  'Natural human text flags zero Tier 1 words'
);
assert(
  detectChatbot(humanNatural).length === 0,
  'Natural human text flags zero chatbot phrases'
);

// ========================================
// SUMMARY
// ========================================

console.log('\n' + '='.repeat(50));
console.log(`\nResults: ${passed} passed, ${failed} failed, ${passed + failed} total`);

if (failures.length > 0) {
  console.log('\nFailed tests:');
  failures.forEach(f => {
    console.log(`  ❌ ${f.testName}`);
    if (f.detail) console.log(`     → ${f.detail}`);
  });
}

console.log('');
process.exit(failed > 0 ? 1 : 0);
