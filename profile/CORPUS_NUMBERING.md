Proposed corpus ID standard
000–009: Canonical baselines (maintainer-owned)

These are the “reference corpora” you use in the matrix and talk about publicly.

000 = neutral baseline (flat)

001 = structured animals baseline (hills)

002–009 reserved for future canonical baselines

This keeps your matrix stable forever.

010–049: Instructor-curated “teaching packs”

These are officially blessed corpora that are not “baseline controls” but are still part of the main curriculum/story.

Suggested mapping (your idea, slightly tightened):

010 = llm_glossary

020 = repo_tour

030 = analytics_micro_lessons

040 = (future) tokenization_demo / morphology / long_words

041–049 reserved for future instructor packs

Why this is good:

IDs encode “this is a standard teaching corpus”

you keep lots of room

050–099: Experimental / optional (instructor-owned)

Corpora you might include later, but not part of the canonical narrative.

050 = adversarial/no-signal (perfectly flat transitions)

060 = ambiguity/disambiguation challenge

etc.

These can come and go without threatening the “main spine.”

100–799: Student contributions (team-allocated blocks)

This is the key part for your “20 students” scenario.

You allocate each student (or team) a small block, and they choose within it.

Example allocation:

Student 01: 100–109

Student 02: 110–119

Student 03: 120–129

...

Student 20: 290–299

Then:

no collisions

no coordination overhead

IDs remain meaningful and bounded

800–999: Reserved for future / external / published corpora

If later you want:

corpora from public domain texts,

corpora with licensing constraints,

corpora tied to a publication artifact,

you have room without renumbering anything.