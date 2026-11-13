import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checks = load_module('check_invariants')
package = load_module('validate_package')


class InvariantsTest(unittest.TestCase):
    def test_zwnj_does_not_split_words(self):
        self.assertEqual(checks.word_count('می‌توانیم\tکمک کنیم.\n'), 3)

    def test_detects_lost_technical_fragments(self):
        corpus = {'cases': [{'id': 'a', 'verbatim': ['{filename}', '?v=2.5']}]}
        errors = checks.check_outputs(corpus, {'a': 'فایل filename را ببینید؛ ?v=۲٫۵'})
        self.assertEqual(len(errors), 2)

    def test_missing_and_unknown_are_not_success(self):
        errors = checks.check_outputs({'cases': [{'id': 'a'}]}, {'b': 'متن'})
        self.assertEqual(len(errors), 2)

    def test_exact_count_runs_on_final_text(self):
        corpus = {'cases': [{'id': 'a', 'exact_words': 3}]}
        self.assertEqual(checks.check_outputs(corpus, {'a': 'متن نهایی اینجاست.'}), [])
        self.assertTrue(checks.check_outputs(corpus, {'a': 'متن اینجاست.'}))

    def test_json_is_not_a_fenced_or_corrupt_approximation(self):
        corpus = {'cases': [{'id': 'a', 'json_keys': ['message'], 'verbatim': ['{n}']}]}
        self.assertEqual(checks.check_outputs(corpus, {'a': '{"message":"تعداد {n}"}'}), [])
        self.assertTrue(checks.check_outputs(corpus, {'a': '```json\n{"message":"{n}"}\n```'}))
        self.assertTrue(checks.check_outputs(corpus, {'a': '{"other":"{n}"}'}))

    def test_empty_or_invalid_outputs_fail(self):
        corpus = {'cases': [{'id': 'a'}]}
        self.assertTrue(checks.check_outputs(corpus, {'a': ''}))
        self.assertTrue(checks.check_outputs(corpus, {'a': 3}))

    def test_duplicates_are_invalid_input(self):
        with self.assertRaises(ValueError):
            checks.check_outputs({'cases': [{'id': 'a'}, {'id': 'a'}]}, {'a': 'متن'})

    def test_semantic_check_is_not_claimed(self):
        # A valid string with an altered claim passes when no explicit invariant
        # was supplied. This limitation is intentional and documented.
        self.assertEqual(checks.check_outputs({'cases': [{'id': 'a'}]}, {'a': 'همه چیز تضمین می‌شود.'}), [])


class PackageTest(unittest.TestCase):
    def test_real_package_links(self):
        self.assertEqual(package.validate(ROOT), [])

    def test_broken_and_escaping_links_are_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'README.md').write_text('[missing](absent.md) [outside](../secret.md)', encoding='utf-8')
            errors = package.validate(root)
            self.assertTrue(any('missing link target' in error for error in errors))
            self.assertTrue(any('escapes package' in error for error in errors))

    def test_corpus_missing_request_is_reported(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / 'evals').mkdir()
            (root / 'evals/cases.json').write_text(json.dumps({'cases': [{'id': 'x'}]}), encoding='utf-8')
            self.assertTrue(any('cases.json' in error for error in package.validate(root)))


if __name__ == '__main__':
    unittest.main()
