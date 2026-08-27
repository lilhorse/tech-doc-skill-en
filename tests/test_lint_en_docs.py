#!/usr/bin/env python3
"""Regression tests for lint_en_docs. Run: python3 tests/test_lint_en_docs.py"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from lint_en_docs import lint_text  # noqa: E402


def rules(text):
    return {f.rule for f in lint_text(text)}


class MaskingTests(unittest.TestCase):
    def test_fenced_code_is_ignored(self):
        text = "Intro text.\n\n```bash\nkill -9 $PID\nabort\n```\n"
        self.assertNotIn("banned-word", rules(text))

    def test_inline_code_is_ignored(self):
        self.assertNotIn("banned-word", rules("Call `terminate()` when done."))

    def test_frontmatter_is_ignored(self):
        text = "---\nname: kill-switch\ndescription: please read\n---\n\nBody text.\n"
        self.assertNotIn("banned-word", rules(text))

    def test_link_target_is_ignored(self):
        self.assertNotIn("banned-word", rules("See [the guide](https://example.com/e.g./via)."))

    def test_prose_outside_code_is_still_checked(self):
        text = "```\nkill\n```\n\nThe process is killed by the supervisor.\n"
        self.assertIn("passive-voice", rules(text))


class WordRuleTests(unittest.TestCase):
    def test_violent_metaphor(self):
        self.assertIn("banned-word", rules("Abort the running job."))

    def test_condescending(self):
        self.assertIn("condescending", rules("Simply restart the service."))

    def test_please(self):
        self.assertIn("banned-word", rules("Please click Save."))

    def test_latin_abbreviation(self):
        self.assertIn("banned-word", rules("Use a scalar type, e.g. an integer."))

    def test_the_user(self):
        self.assertIn("banned-word", rules("The user must sign in first."))


class MechanicsTests(unittest.TestCase):
    def test_en_dash(self):
        self.assertIn("en-dash", rules("Supported from 2015–2017."))

    def test_spaced_em_dash(self):
        self.assertIn("spaced-em-dash", rules("The cache — which is optional — warms slowly."))

    def test_unspaced_em_dash_is_clean(self):
        self.assertNotIn("spaced-em-dash", rules("The cache—optional—warms slowly."))

    def test_ambiguous_numeric_date(self):
        self.assertIn("numeric-date", rules("Released on 04/06/2017."))

    def test_iso_date_is_clean(self):
        self.assertNotIn("numeric-date", rules("Released on 2026-04-15."))

    def test_ordinal_numeral(self):
        self.assertIn("ordinal-numeral", rules("Open the 3rd tab."))

    def test_percent_spelled_out(self):
        self.assertIn("percent-word", rules("At least 50 percent of resources stay free."))

    def test_percent_sign_is_clean(self):
        self.assertNotIn("percent-word", rules("At least 50% of resources stay free."))

    def test_lowercase_am_pm(self):
        self.assertIn("am-pm", rules("The job runs at 3pm."))

    def test_non_descriptive_link(self):
        self.assertIn("link-text", rules("For details, [click here](https://example.com)."))


class HeadingTests(unittest.TestCase):
    def test_heading_ending_in_period(self):
        self.assertIn("heading-punctuation", rules("## Create an instance.\n"))

    def test_title_case_heading(self):
        self.assertIn("heading-case", rules("## Create An Instance Now\n"))

    def test_sentence_case_heading_is_clean(self):
        self.assertNotIn("heading-case", rules("## Create an instance\n"))

    def test_proper_nouns_in_sentence_case_heading(self):
        found = rules("## Deploy to Google Cloud\n")
        self.assertNotIn("heading-punctuation", found)


class SentenceTests(unittest.TestCase):
    def test_long_sentence_flagged(self):
        sentence = "The service " + "processes each request and " * 8 + "returns a result."
        self.assertIn("long-sentence", rules(sentence))

    def test_short_sentence_clean(self):
        self.assertNotIn("long-sentence", rules("The service returns a result."))


class PositionTests(unittest.TestCase):
    def test_line_numbers_survive_masking(self):
        text = "Line one.\n\n```\nkill\n```\n\nPlease stop.\n"
        finding = next(f for f in lint_text(text) if f.rule == "banned-word")
        self.assertEqual(finding.line, 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
