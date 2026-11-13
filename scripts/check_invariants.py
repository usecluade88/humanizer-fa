"""Check explicit output constraints, never prose quality or full semantic fidelity."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def word_count(text: str) -> int:
    """Whitespace-delimited tokens; ZWNJ remains within a token."""
    return len(text.split())


def check_outputs(corpus: dict, outputs: dict) -> list[str]:
    cases = corpus.get('cases')
    if not isinstance(cases, list) or not cases:
        raise ValueError('corpus.cases must be a nonempty list')
    ids = [case['id'] for case in cases]
    if len(set(ids)) != len(ids):
        raise ValueError('case ids must be unique')
    if not isinstance(outputs, dict):
        raise ValueError('outputs must map case ids to output strings')
    errors = [f'missing case: {key}' for key in ids if key not in outputs]
    errors += [f'unknown case: {key}' for key in outputs if key not in ids]
    for case in cases:
        key = case['id']
        if key not in outputs:
            continue
        text = outputs[key]
        if not isinstance(text, str) or not text.strip():
            errors.append(f'{key}: output must be a nonempty string')
            continue
        count = word_count(text)
        if 'exact_words' in case and count != case['exact_words']:
            errors.append(f'{key}: expected {case["exact_words"]} words, got {count}')
        if 'max_words' in case and count > case['max_words']:
            errors.append(f'{key}: exceeds {case["max_words"]} words (got {count})')
        for part in case.get('verbatim', []) + case.get('must_contain', []):
            if part not in text:
                errors.append(f'{key}: missing required fragment {part!r}')
        if 'equals' in case and text.strip() != case['equals']:
            errors.append(f'{key}: expected exact unchanged text')
        if 'json_keys' in case:
            try:
                obj = json.loads(text)
            except json.JSONDecodeError:
                errors.append(f'{key}: not valid raw JSON')
            else:
                if not isinstance(obj, dict) or set(obj) != set(case['json_keys']):
                    errors.append(f'{key}: JSON keys changed')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('corpus', type=Path)
    parser.add_argument('outputs', type=Path)
    args = parser.parse_args()
    try:
        corpus = json.loads(args.corpus.read_text(encoding='utf-8-sig'))
        outputs = json.loads(args.outputs.read_text(encoding='utf-8-sig'))
        errors = check_outputs(corpus, outputs)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'Invalid input: {exc}')
        return 2
    if errors:
        for error in errors:
            print(error)
        return 1
    print(f'Explicit machine-checkable constraints passed for {len(corpus["cases"])} cases.')
    print('Tone, engagement, empathy and full meaning preservation still need review.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
