# Humanizer FA

Natural Persian writing with selectable tone and meaning-preservation checks.

[فارسی](README.md) · [Tone guide](references/tones.md) · [Examples](examples/before-after.md) · [Evaluation](evals/rubric.md)

A standalone prompt skill for writing, rewriting and reviewing Persian prose. Choose a conversational, warm-professional, formal, administrative, academic, persuasive, literary or custom voice. Keep facts, qualifications, speaker roles and technical fragments intact while improving how the text reads.

## Quick start

[Download the repository ZIP](https://github.com/usecluade88/humanizer-fa/archive/refs/heads/main.zip), or clone it:

```text
git clone https://github.com/usecluade88/humanizer-fa.git
```

Copy the folder containing `SKILL.md` into your agent installation's configured skill directory, name it `humanizer-fa`, and retain its `references` directory. For a Codex installation that discovers personal skills under `~/.codex/skills`, the destination is `~/.codex/skills/humanizer-fa`. Locations vary; confirm discovery in your own environment rather than assuming installation from a copied folder alone.

Once available in Codex, an example request is:

```text
$humanizer-fa
این متن را خودمونی ولی با خطاب شما بازنویسی کن؛ کوتاه و فقط متن نهایی:
«لازم به ذکر است که درخواست شما دریافت گردید.»
```

Illustrative output: «درخواستتون رو دریافت کردیم.» Exact model wording will vary.

This is an instruction bundle, not a trained model, web service, browser extension or executable rewriting engine. Invocation syntax depends on the host agent; cross-agent behavior has not been comprehensively tested. Optional validation utilities require Python 3.10+. The writing skill itself needs no API key, network service, font or Python execution.

## Controls

Natural-language instructions are sufficient. Optional textual controls provide an explicit contract:

```text
task=edit tone=samimi address=shoma strength=balanced length=short output=final
متن: ...
```

These are prompt hints, not flags accepted by a CLI or API. See [SKILL.md](SKILL.md) for supported values. Persian names such as «خودمونی» and «رسمی» are accepted as natural-language equivalents.

Tone and relationship are separate: conversational Persian need not address an unfamiliar customer with «تو». Empathy means responding to the person's specific problem and a useful next step, not inserting an emotional stock phrase. An already-good sentence may remain unchanged.

Use `light`, `balanced` or `deep` editing without silently deleting information. Use `length=exact:40` for whitespace-delimited word counts; ZWNJ does not split a token. When factual fidelity and a length request cannot coexist, the skill must surface the conflict rather than fabricate details or remove critical conditions.

## Scope and limitations

Suitable for website copy, UI messages, support replies, professional correspondence, articles and social writing in Persian. English text should use a suitable English editing workflow. A website orchestrator may select this skill for Persian and a different one for English; neither is a required dependency of this package.

No AI-detector evasion, human-origin certification, search ranking or universal quality guarantee is offered. Results depend on the model, brief and source text. The skill does not validate a business policy, issue refunds or send messages. Review important outputs, especially legal, scientific and contractual text.

## Validation and evaluation

```text
python scripts/validate_package.py
python -m unittest discover -s tests -v
python scripts/check_invariants.py evals/cases.json path/to/outputs.json
```

The first two commands need no model or network. The third checks outputs you actually generated against explicit string/count constraints. It cannot establish full semantic fidelity or naturalness. The [evaluation rubric](evals/rubric.md) describes semantic gates and qualitative review; [recorded results](evals/RESULTS.md) disclose the scope and limitations of the available run.

Version 2.0.1 also includes [five long-form before/after examples](evals/long-form.md), with each source and final text above 200 whitespace-delimited words. This is explicitly author self-review, not blinded or independent evaluation.

See [CONTRIBUTING.md](CONTRIBUTING.md) for reporting reproducible issues without private data. Documentation is bilingual; detailed editorial references and evaluation prompts are Persian because the target task is Persian writing.

## License and credits

[MIT](LICENSE). Editorial ideas were informed by Humanizer and Persian Writing and independently redesigned. This is not their official release or translation. [Third-party notices](THIRD_PARTY_NOTICES.md) preserve attribution and upstream license notices; see [source notes](references/sources.md). No upstream font, dictionary or cleanup implementation is bundled.
