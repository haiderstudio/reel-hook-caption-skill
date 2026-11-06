# reel-hook-caption-skill

Write hooks, a caption, and a carousel outline for one reel.

[![CI](https://github.com/haiderstudio/reel-hook-caption-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/haiderstudio/reel-hook-caption-skill/actions/workflows/ci.yml) [![Licence: MIT](https://img.shields.io/badge/Licence-MIT-yellow.svg)](LICENSE)

## What it does

When an AI coding agent loads this skill, it writes
the words for one reel — and nothing else — in this
fixed shape:

- **3 hooks**, one line each, under 100 characters,
  each a different angle: a claim with a number, a
  question or a command, and a mistake or a skipped
  step.
- **1 caption**: the first line is one of the three
  hooks, the body is the key points in plain words,
  one ask only, at most 5 hashtags — each a word
  from the topic or the points. At most 2,200
  characters, with the count printed and the first
  125 characters shown, so the creator can see
  where the feed cuts it off.
- **A 5-slide carousel outline**: cover, one point
  per slide, payoff with the same one ask.

It works from two things the creator gives it: a
topic, and at least 3 key points in the creator's
own words. Every number in the output must be a
number from the topic or the points. Every hashtag
must be a word from the topic or the points. If
fewer than 3 points are given, the skill stops and
asks for the missing ones instead of inventing a
third point.

## What it does NOT do

- It does not post, schedule, or publish anything.
  It writes text. The creator posts it, in their
  own name, when they choose.
- It does not promise reach, views, or followers.
  No hook or caption can promise that, and this
  skill never writes a promise about what the text
  will do.
- It does not invent facts, numbers, or results.
  A number that is not in the topic or the points
  is never written. A vague point is never
  sharpened into a number.
- It does not edit or render video. Hooks,
  captions, and slide text are the whole output.
  Cutting, on-screen captions, music, and
  rendering are different jobs.
- It does not write a second version, a week of
  reels, or a full account plan. One reel is the
  whole job.
- It does not add a 4th hook or a 6th slide. The
  shape is fixed: 3 hooks, 1 caption, 5 slides.

## Who it is for

Creators who use an AI coding agent and want the
words for one reel written from their own points —
three hooks to choose from, one caption, and a
five-slide outline — without handing the agent the
posting, and without a promise about what the reel
will do.

## How this differs from similar tools

Hooks and captions for short video are a crowded
field, and the wide versions of it are packs that
run a whole account. This skill is the narrow one
— one skill, one reel, text only:

- Jakeschincariol/instagram-agent-skill is a pack
  of 13 skills. Its `/ig-reel` writes 3 hooks from
  26 formulas, scores them, and writes the script
  and a timed beat sheet; its `/ig-caption` lints
  the caption and shows the first ~125 characters.
  This skill does not score hooks, does not write
  a script or a beat sheet, and does not split the
  job across skills — hooks, caption, and the
  5-slide outline come out together, in one fixed
  shape.
- sergebulaev/instagram-skills is a bundle of 9
  skills (752 stars, per SkillsLLM, checked Nov 6,
  2026): a caption writer, a carousel planner, a
  hook extractor, and more, with a publish flow
  through Publora. This skill is one skill, writes
  text only, and never touches posting or
  publishing.
- motion-team/creative-strategy-skills
  hook-voice-patterns is a swipe file of hook
  templates to browse. This skill is not a library
  to browse — it writes one reel's hooks, caption,
  and slides from the creator's own points.
- harper-carroll/reel-studio-skill is a full reel
  pipeline that renders video: AI B-roll, Remotion
  captions, editing. This skill renders nothing —
  it writes words only.
- A GitHub search for the exact name
  "reel-hook-caption-skill" returns 0 results
  (checked Nov 6, 2026). No repo owns that exact
  name or that exact one-skill shape.

None of those were copied. The fixed output shape,
the three hook angles, the 125-character check, the
no-invention rule, and all three worked examples
here are original.

## Install

This skill follows the open Agent Skills format: a folder with a
`SKILL.md` file.

**Claude Code / Codex / Gemini CLI (project level):**

```bash
mkdir -p .agents/skills
cp -r skills/reel-hook-caption-skill .agents/skills/reel-hook-caption-skill
```

## Usage

Give the agent a topic and at least 3 key points,
and tell it to use this skill. The agent follows
`skills/reel-hook-caption-skill/SKILL.md`: it reads
the points, writes 3 hooks, one caption, and the
5-slide outline, and stops. With fewer than 3
points it asks for the missing ones and writes
nothing.

## Example 1 — a full reel, 4 points

The input (from `examples/editing-time-input.md`) is
a topic and four points about cutting editing time.
The output (full output in
`examples/editing-time-output.md`):

```markdown
Topic: How I cut my editing time from 6 hours to 47 minutes
Hooks (3):
1. I cut my editing time from 6 hours to 47 minutes.
2. Stop editing your video in the wrong order.
3. The first cut I make has nothing to do with colour.
Caption (opens with hook 1):
I cut my editing time from 6 hours to 47 minutes.
I edit in watch order: hook first, then the middle, then the ending.
First, cut pauses and dead air before colour or music.
One caption style for the whole video — I never re-decide it.
Export a draft, watch it once on my phone, fix only what I notice.
Save this for your next edit.
#editing #video #caption
Caption length: 357 / 2200 characters
First 125 characters: "I cut my editing time from 6 hours to 47 minutes.
I edit in watch order: hook first, then the middle, then the ending.
First," (125 characters)
Slides (5):
1. Cover — I cut my editing time from 6 hours to 47 minutes.
2. Edit in watch order: hook first, then the middle, then the ending.
3. Cut pauses and dead air before colour or music.
4. One caption style for the whole video.
5. Payoff — Export a draft, watch it once on my phone, fix only what you notice. Save this for your next edit.
```

Three hooks, three different angles. The only
numbers in the output — 6 and 47 — are the numbers
from the input. The hashtags are words from the
topic and points. One ask: save. The first 125
characters end at a word end, and the first line
ends cleanly at 49 characters, well before the
feed cut.

## Example 2 — a second reel, 3 points

The input (from `examples/used-phone-input.md`) is
a topic and three points about buying a used phone.
The output (full output in
`examples/used-phone-output.md`):

```markdown
Topic: Three things I check before I buy a used phone
Hooks (3):
1. Three checks before you buy a used phone.
2. Battery under 80%? I walk away.
3. The screen test most buyers skip.
Caption (opens with hook 1):
Three checks before you buy a used phone.
Battery health under 80% and I just walk away.
Test call and a voice note — mic and speaker checked.
Screen in full sunlight: dead pixels and a dim patch.
Comment CHECK and I will send you the list.
#phone #battery #screen
Caption length: 264 / 2200 characters
First 125 characters: "Three checks before you buy a used phone.
Battery health under 80% and I just walk away.
Test call and a voice note — mic and" (125 characters)
Slides (5):
1. Cover — Three checks before you buy a used phone.
2. Battery health under 80%? Walk away.
3. Test call and a voice note: mic and speaker.
4. Screen in full sunlight: dead pixels and dim patches.
5. Payoff — Three checks, no surprises. Comment CHECK for the list.
```

The same shape, a different topic. The caption ask
is "comment", and slide 5 carries the same ask.
The only number in the output — 80 — is the number
from the input.

## Example 3 — too few points, the skill stops

The input (from `examples/too-few-points-input.md`)
gives a topic and only 2 key points. The skill
writes no hooks, no caption, and no slides. The
whole output (in `examples/too-few-points-output.md`):

```markdown
I need one more key point before I write anything — you gave 2, I need at least 3. What is the third point?
```

Two points is not enough to fill three hooks and
five slides without inventing a third point, so the
skill writes nothing instead. A third worked
example — a fresh topic walked through by hand,
following the skill step by step — is in
`examples/walkthrough-input.md` and
`examples/walkthrough-output.md`: packing a
carry-on for 3 days, 3 points, 3 hooks, one
caption of 245 characters, 5 slides.

## How it is tested

```bash
python3 tests/test_skill.py
```

The tests check that `SKILL.md` has valid `name` and
`description` frontmatter and the required workflow
sections; that the three complete examples each
have exactly 3 hooks under 100 characters, 1
caption that opens with one of the hooks, a caption
length that matches the number printed under it
and stays under 2,200 characters, a first-125
characters line that matches the caption, exactly 5
slides under 120 characters, a cover slide that is
the chosen hook, no number in any output that is
not in the input, at most 5 hashtags and each one a
word from the input, exactly one ask and the same
ask in slide 5, and no reach-promise words anywhere;
that the too-few-points example asks for the third
point and writes nothing else; that the outputs
quoted in this README and in the skill are the real
files; that `.gitignore` starts with `.env`; that
the install step copies the skill to a clean folder;
and that no file uses a third-party import. Standard
library only — no third-party imports, so the same
command runs on a clean CI runner. No placeholder
text anywhere in the repo.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and pull requests
are welcome; please keep examples real and checkable, and
never put a real person's account, a real post, or a real
result in an example, a test, or an output.

## Licence

MIT — see [LICENSE](LICENSE). This is original work. The
related tools named above are listed as related work, not
sources — nothing here was copied from them.
