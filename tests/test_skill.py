"""Tests for the reel-hook-caption-skill: frontmatter, the fixed
output shape (3 hooks, 1 caption, 5 slides) in the three worked
examples, the counts the skill prints (hook and slide lengths,
caption length, first 125 characters), the no-invention rule
(every number in an output is a number from the input, every
hashtag is a word from the input), one ask only, no reach
promises, .gitignore, CI, and the install step. Standard
library only — no third-party imports (a clean CI runner
does not have them)."""
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "reel-hook-caption-skill" / "SKILL.md"
README = ROOT / "README.md"
GITIGNORE = ROOT / ".gitignore"
CI = ROOT / ".github" / "workflows" / "ci.yml"
EX1_IN = ROOT / "examples" / "editing-time-input.md"
EX1_OUT = ROOT / "examples" / "editing-time-output.md"
EX2_IN = ROOT / "examples" / "used-phone-input.md"
EX2_OUT = ROOT / "examples" / "used-phone-output.md"
FEW_IN = ROOT / "examples" / "too-few-points-input.md"
FEW_OUT = ROOT / "examples" / "too-few-points-output.md"
WALK_IN = ROOT / "examples" / "walkthrough-input.md"
WALK_OUT = ROOT / "examples" / "walkthrough-output.md"
BANNED = ["TODO", "FIXME", "lorem", "coming soon"]
GROWTH = ["viral", "guaranteed"]
ASK_WORDS = ["comment", "save", "share", "follow"]


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        sys.exit(1)


def parse_output(text):
    """Split a fixed-shape output into its parts.

    Returns a dict: topic, hooks (3 texts), opens (hook number
    the caption opens with), caption_lines, stated_len,
    first125 (quoted string), first125_count, slides (5 texts)."""
    lines = text.splitlines()
    hooks_at = next(i for i, l in enumerate(lines)
                    if l.startswith("Hooks (3):"))
    cap_at = next(i for i, l in enumerate(lines)
                  if l.startswith("Caption (opens with hook"))
    len_at = next(i for i, l in enumerate(lines)
                  if l.startswith("Caption length:"))
    slides_at = next(i for i, l in enumerate(lines)
                     if l.startswith("Slides (5):"))
    hooks = []
    for line in lines[hooks_at + 1:cap_at]:
        m = re.match(r"^[123]\. (.*)$", line)
        if m:
            hooks.append(m.group(1))
    opens = int(re.search(r"hook (\d+)", lines[cap_at]).group(1))
    caption_lines = lines[cap_at + 1:len_at]
    stated_len = int(re.search(r"Caption length: (\d+) / 2200",
                               lines[len_at]).group(1))
    m = re.search(r'First 125 characters: "(.*?)" \((\d+) characters\)',
                  text, re.S)
    first125, first125_count = m.group(1), int(m.group(2))
    slides = []
    for line in lines[slides_at + 1:]:
        m = re.match(r"^[1-5]\. (?:Cover — |Payoff — )?(.*)$", line)
        if m:
            slides.append(m.group(1))
    return {"topic": lines[0].split("Topic: ", 1)[1],
            "hooks": hooks, "opens": opens,
            "caption_lines": caption_lines,
            "stated_len": stated_len,
            "first125": first125, "first125_count": first125_count,
            "slides": slides}


def parse_input(text):
    """Return (topic, [point texts]) from an input file."""
    lines = text.splitlines()
    topic = lines[0].split("Topic: ", 1)[1]
    points = []
    for line in lines:
        m = re.match(r"^\d+\. (.*)$", line)
        if m:
            points.append(m.group(1))
    return topic, points


def numbers(s):
    return set(re.findall(r"\d+", s))


def words(s):
    return set(re.findall(r"[a-z]+", s.lower()))


def check_full_output(name, in_path, out_path):
    """Mechanical checks on one complete example."""
    topic, points = parse_input(in_path.read_text())
    out = parse_output(out_path.read_text())
    check("test_" + name + "_topic", out["topic"] == topic)
    check("test_" + name + "_three_hooks", len(out["hooks"]) == 3)
    check("test_" + name + "_hooks_under_100",
          all(len(h) < 100 for h in out["hooks"]))
    check("test_" + name + "_caption_opens_with_hook",
          out["caption_lines"][0] == out["hooks"][out["opens"] - 1])
    caption = "\n".join(out["caption_lines"])
    check("test_" + name + "_caption_length",
          len(caption) == out["stated_len"]
          and out["stated_len"] <= 2200)
    check("test_" + name + "_first125",
          caption[:125] == out["first125"]
          and out["first125_count"] == 125)
    check("test_" + name + "_five_slides", len(out["slides"]) == 5)
    check("test_" + name + "_slides_under_120",
          all(len(s) < 120 for s in out["slides"]))
    check("test_" + name + "_cover_is_hook",
          out["slides"][0] == out["hooks"][out["opens"] - 1])
    # No invented numbers: every digit in a hook, in the caption
    # body, or in a slide must be a digit from the topic or points.
    allowed = numbers(topic) | numbers(" ".join(points))
    used = (numbers(" ".join(out["hooks"]))
            | numbers(caption) | numbers(" ".join(out["slides"])))
    check("test_" + name + "_no_invented_numbers", used <= allowed)
    # Hashtags: at most 5, each a word from the topic or points.
    tags = re.findall(r"#([A-Za-z]+)", caption)
    check("test_" + name + "_hashtags_max_5", len(tags) <= 5)
    check("test_" + name + "_hashtags_from_input",
          all(t.lower() in words(topic) | words(" ".join(points))
              for t in tags))
    # One ask only, the same ask in the caption and slide 5.
    found = [w for w in ASK_WORDS
             if re.search(r"\b" + w + r"\b", caption, re.I)]
    check("test_" + name + "_one_ask", len(found) == 1)
    check("test_" + name + "_same_ask_slide5",
          re.search(r"\b" + found[0] + r"\b",
                    out["slides"][4], re.I) is not None)
    # No reach promises anywhere in the output.
    check("test_" + name + "_no_growth_words",
          not any(g in out_path.read_text().lower() for g in GROWTH))
    return out


def main():
    skill = SKILL.read_text()
    m = re.match(r"---\n(.*?)\n---\n", skill, re.S)
    check("test_skill_frontmatter",
          bool(m) and "name: reel-hook-caption-skill" in m.group(1)
          and "description:" in m.group(1))
    for section in ["When to use this skill", "When NOT to use it",
                    "What you need before you start", "Workflow",
                    "Good examples", "Bad examples", "Output rules",
                    "Limits and safety rules"]:
        check("test_skill_sections_" + section.split()[0],
              section in skill)
    check("test_skill_shape",
          "Hooks (3):" in skill and "Slides (5):" in skill
          and "Caption (opens with hook" in skill)
    check("test_skill_no_yaml_import", "import yaml" not in skill)
    check("test_gitignore_env_first",
          GITIGNORE.read_text().splitlines()[0] == ".env")
    for f in [SKILL, README, EX1_IN, EX1_OUT, EX2_IN, EX2_OUT,
              FEW_IN, FEW_OUT, WALK_IN, WALK_OUT]:
        check("test_no_placeholders_" + f.name,
              not any(b in f.read_text() for b in BANNED))
        check("test_no_growth_words_" + f.name,
              not any(g in f.read_text().lower() for g in GROWTH))

    # The three complete examples, checked mechanically.
    check_full_output("ex1", EX1_IN, EX1_OUT)
    check_full_output("ex2", EX2_IN, EX2_OUT)
    check_full_output("walkthrough", WALK_IN, WALK_OUT)

    # Too few points: the skill stops and asks, writes nothing.
    _, few_points = parse_input(FEW_IN.read_text())
    check("test_few_points_count", len(few_points) == 2)
    few = FEW_OUT.read_text()
    check("test_few_points_asks",
          "I need one more key point" in few
          and "you gave 2" in few)
    check("test_few_points_no_output",
          "Hooks (3):" not in few and "Slides (5):" not in few
          and "Caption (opens" not in few)

    # The outputs quoted in the README and SKILL.md are the real files.
    readme = README.read_text()
    for name, path in [("ex1", EX1_OUT), ("ex2", EX2_OUT)]:
        text = path.read_text()
        check("test_" + name + "_output_in_readme",
              text.strip() in readme)
        check("test_" + name + "_output_in_skill",
              text.strip() in skill)
    check("test_few_output_in_readme", few.strip() in readme)
    check("test_walkthrough_output_in_skill",
          WALK_OUT.read_text().strip() not in skill)  # walkthrough
    # (lives in examples/ only; the skill quotes ex1 and ex2)

    # CI is valid plain YAML shape and runs only stdlib tests.
    ci = CI.read_text()
    check("test_ci_valid",
          "python3 tests/test_skill.py" in ci
          and "actions/checkout@v4" in ci
          and "runs-on: ubuntu-latest" in ci)
    check("test_ci_no_pip_install", "pip install" not in ci)

    # No third-party imports anywhere in the repo's Python, and
    # no absolute local paths or .env file anywhere. (Match real
    # import lines only — the literal "import yaml" also appears
    # inside this check itself.)
    for path in ROOT.rglob("*.py"):
        text = path.read_text()
        check("test_stdlib_only_" + path.name,
              not re.search(r"(?m)^(import|from) (yaml|requests|pytest)\b",
                            text))
        check("test_no_abs_path_" + path.name,
              not re.search(r"/(home|Users)/[A-Za-z]", text))
    check("test_no_env_file", not (ROOT / ".env").exists())
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".yml"):
            check("test_no_abs_path_" + path.name,
                  "/home/" not in path.read_text(errors="ignore"))

    # Install step from the README works on a clean folder.
    # (If this environment cannot create a temp dir at all —
    # some sandboxes block file writes from a shell — the check
    # says SKIP out loud instead of passing silently. It still
    # runs for real on the CI runner.)
    try:
        tmpdir = tempfile.TemporaryDirectory()
    except OSError:
        print("SKIP test_install_copies_skill "
              "(no writable temp dir in this environment)")
    else:
        with tmpdir as tmp:
            dest = Path(tmp) / ".agents" / "skills"
            dest.mkdir(parents=True)
            shutil.copytree(ROOT / "skills" / "reel-hook-caption-skill",
                            dest / "reel-hook-caption-skill")
            check("test_install_copies_skill",
                  (dest / "reel-hook-caption-skill" / "SKILL.md").exists())
    print("All tests passed.")


if __name__ == "__main__":
    main()
