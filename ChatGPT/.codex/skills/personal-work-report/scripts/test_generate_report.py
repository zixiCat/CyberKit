import copy
import json
import tempfile
import unittest
from pathlib import Path

from generate_report import localized, markdown, validate


class ReportContractTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).parent.parent / 'references' / 'intake.json').read_text(encoding='utf-8-sig'))
        self.data['date'] = '2026-01-01'
        self.data['commits'] = [{'id': 'abc12345', 'at': '2026-01-01 10:00 +08:00', 'author': 'Example author', 'title': 'Restore saved replies', 'status': 'Current checkout'}]

    def check(self, data):
        with tempfile.TemporaryDirectory() as folder:
            return validate(data, Path(folder))

    def test_old_reports_remain_valid(self):
        del self.data['summary']
        del self.data['commits']
        self.check(self.data)
        self.assertIn(self.data['conclusion'], markdown(self.data))

    def test_summary_cannot_invent_an_evidence_reference(self):
        self.data['summary'][0]['evidence_ids'] = ['E99']
        with self.assertRaisesRegex(ValueError, 'unknown evidence'):
            self.check(self.data)

    def test_translated_commits_keep_attribution_and_timestamp(self):
        self.data['translations'] = {'zh': {'summary': [{'label': '改了什么', 'text': '修复回复丢失。', 'evidence_ids': []}], 'commits': [{'id': 'abc12345', 'title': '修复回复丢失', 'status': '当前分支'}]}}
        self.check(self.data)
        translated = localized(self.data, 'zh')
        self.assertEqual(translated['commits'][0]['author'], self.data['commits'][0]['author'])
        self.assertEqual(translated['commits'][0]['at'], self.data['commits'][0]['at'])
        altered = copy.deepcopy(self.data)
        altered['translations']['zh']['commits'][0]['author'] = 'Different author'
        with self.assertRaisesRegex(ValueError, 'attribution'):
            self.check(altered)

    def test_commit_manifest_does_not_drop_or_duplicate_changes(self):
        self.data['commits'].append(copy.deepcopy(self.data['commits'][0]))
        with self.assertRaisesRegex(ValueError, 'unique'):
            self.check(self.data)

    def test_long_image_and_markdown_preserve_content(self):
        self.data['imageLayout'] = 'long'
        self.data['summary'][0]['text'] = 'Restore A | B replies'
        self.check(self.data)
        output = markdown(self.data)
        self.assertIn('A \\| B', output)
        self.assertIn('abc12345', output)
        self.assertIn('Example author', output)
        self.data['imageLayout'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'imageLayout'):
            self.check(self.data)


if __name__ == '__main__':
    unittest.main()
