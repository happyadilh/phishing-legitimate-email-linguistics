import csv
import math
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from phishing_language.features import extract,mattr,read_emolex
from phishing_language.analysis import holm_adjust,cohens_d
from phishing_language.cli import run_extract

class FeatureTests(unittest.TestCase):
    def test_second_person(self):
        result=extract('You should check your notes. I will review the email.')
        self.assertGreater(result['second_person'],result['first_person_singular'])
    def test_urgency_multiword(self):
        self.assertGreater(extract('Act now! The last chance to respond is today.')['urgency_markers'],0)
    def test_mattr_under_window(self):
        self.assertAlmostEqual(mattr(['one','two','one'],20),2/3)
    def test_no_text(self):
        with self.assertRaises(ValueError):extract('1234 %%%')
    def test_emotion_optional(self):
        self.assertNotIn('positive_emotion',extract('I read the message.'))
    def test_holm(self):
        self.assertEqual([round(x,2) for x in holm_adjust([.01,.04,.03])],[.03,.06,.06])
    def test_cohens_d_direction(self):
        self.assertGreater(cohens_d([3,5,7],[1,2,3]),0)
    def test_holm_preserves_undefined_tests(self):
        result = holm_adjust([float('nan'), .01, .04, .03])
        self.assertTrue(math.isnan(result[0]))
        for actual, expected in zip(result[1:], [.04, .09, .09]):
            self.assertAlmostEqual(actual, expected)
        self.assertTrue(math.isnan(holm_adjust([float('nan')])[0]))
    def test_holm_rejects_invalid_probabilities(self):
        for invalid in (-.1, 1.1, float('inf')):
            with self.assertRaises(ValueError):
                holm_adjust([.01, invalid])
    def test_demo_rows(self):
        with (ROOT/'data/demo_emails.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),8)
        self.assertEqual(sum(r['label']=='phishing' for r in rows),4)
    def test_reported_rows(self):
        with (ROOT/'data/reported_feature_results.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual((len(rows),sum(r['significant_reported']=='yes' for r in rows)),(19,16))
        self.assertEqual(max(rows,key=lambda r:float(r['cohens_d_reported']))['feature'],'Second-person pronouns')
    def test_emo_lex_parser(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'lex.tsv'
            path.write_text('happy\tpositive\t1\nsad\tnegative\t1\nafraid\tfear\t1\n',encoding='utf-8')
            lex=read_emolex(path)
            self.assertEqual(lex['fear'],{'afraid'})

if __name__=='__main__':unittest.main()
