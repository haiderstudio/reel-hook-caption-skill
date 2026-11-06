# Contributing

Small, focused improvements are welcome.

- Open an issue first for anything larger than a typo or a clearer example, so the scope can be agreed before work starts.
- Never weaken the safety rules: the skill must stay text-only — it must never post, schedule, or publish anything — it must never invent a fact or a number, and it must never promise reach, views, or followers. The output shape is fixed: 3 hooks, 1 caption, 5 slides.
- Do not add a 4th hook or a 6th slide, and do not drop one. The shape is fixed. A new output needs its own issue and a reason why this shape is not enough.
- Every claim in a proposed change must be verifiable: a command must be runnable, a hook length must be countable, a caption length must match the number printed under it, a number in an output must be a number from the input.
- Run `python3 tests/test_skill.py` before opening a pull request. It must pass.
- Do not add placeholder text, invented features, or copied content without attribution.
- Python standard library only — no new dependency without a reason in the issue.
- Never put a real person's account, a real post, or a real result in an example, a test, or an output.
