"""Dependency-free package checks; not a general YAML or language-quality validator."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    required = ['SKILL.md', 'LICENSE', 'README.md', 'README.en.md',
                'agents/openai.yaml', 'references/tones.md', 'references/editorial.md',
                'references/web-copy.md', 'references/sources.md',
                'evals/cases.json', 'evals/holdout.json', 'evals/rubric.md', 'THIRD_PARTY_NOTICES.md',
                'third_party/humanizer-LICENSE.txt', 'third_party/persian-writing-LICENSE.txt']
    for relative in required:
        if not (root / relative).is_file():
            errors.append(f'missing file: {relative}')
    manifest = root / 'SKILL.md'
    if manifest.is_file():
        content = manifest.read_text(encoding='utf-8')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', content, re.S)
        if not match:
            errors.append('SKILL.md: missing frontmatter')
        else:
            front = match.group(1)
            for field in ['name', 'description', 'license']:
                if not re.search(rf'^{field}:\s*\S', front, re.M):
                    errors.append(f'SKILL.md: missing {field}')
            if not re.search(r'^name: humanizer-fa\s*$', front, re.M):
                errors.append('SKILL.md: incorrect skill name')
    for doc in root.rglob('*.md'):
        text = doc.read_text(encoding='utf-8')
        for link in re.findall(r'\]\(([^)]+)\)', text):
            if '://' in link or link.startswith('#'):
                continue
            target = (doc.parent / link.split('#', 1)[0]).resolve()
            if not target.is_relative_to(root):
                errors.append(f'{doc.relative_to(root)}: link escapes package: {link}')
            elif not target.is_file():
                errors.append(f'{doc.relative_to(root)}: missing link target: {link}')
        if re.search(r'[A-Z]:[\\/]Users[\\/]\w+', text):
            errors.append(f'{doc.relative_to(root)}: device-specific user path')
    for relative in ['evals/cases.json', 'evals/holdout.json']:
        corpus_path = root / relative
        if not corpus_path.is_file():
            continue
        try:
            corpus = json.loads(corpus_path.read_text(encoding='utf-8'))
            cases = corpus['cases']
            if not isinstance(cases, list) or not cases:
                raise ValueError('cases must be a nonempty list')
            ids = [case['id'] for case in cases]
            if len(set(ids)) != len(ids):
                raise ValueError('duplicate case ids')
            for case in cases:
                if not isinstance(case['id'], str) or not case['id']:
                    raise ValueError('invalid case id')
                if not isinstance(case['request'], str) or not case['request'].strip():
                    raise ValueError('empty case request')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{relative}: {exc}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate(args.root)
    except (OSError, UnicodeError) as exc:
        print(f'Cannot read package: {exc}')
        return 2
    if errors:
        print('\n'.join(errors))
        return 1
    print('Package structure, local links and evaluation corpus passed basic checks.')
    print('This does not validate full YAML syntax or writing quality.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
