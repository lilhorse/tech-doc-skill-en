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
        self.assertNotIn("please", rules(text))

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
        self.assertIn("please", rules("Please click Save."))

    def test_latin_abbreviation(self):
        self.assertIn("banned-word", rules("Use a scalar type, e.g. an integer."))

    def test_the_user(self):
        self.assertIn("the-user", rules("The user must sign in first."))


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
        self.assertIn("heading-case", rules("## Create An Instance Right Now\n"))

    def test_short_title_case_heading_is_a_known_miss(self):
        """Two capitalized words is under the threshold that spares
        'Deploy to Google Cloud'. Documented tradeoff, not a regression."""
        self.assertNotIn("heading-case", rules("## Create An Instance Now\n"))

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
        finding = next(f for f in lint_text(text) if f.rule == "please")
        self.assertEqual(finding.line, 7)


class AuditRegressionTests(unittest.TestCase):
    """Every case here is a defect found by the 2026-08-27 adversarial audit.
    The false positives all contradicted rules the skill itself teaches."""

    def test_recommended_time_format_is_not_flagged(self):
        self.assertNotIn("am-pm", rules("The job runs at 3 PM daily."))

    def test_lowercase_meridiem_is_flagged(self):
        self.assertIn("am-pm", rules("The job runs at 3pm."))

    def test_missing_space_before_meridiem_is_flagged(self):
        self.assertIn("am-pm", rules("The job runs at 3PM."))

    def test_thematic_breaks_are_not_treated_as_front_matter(self):
        text = "Intro.\n\n---\n\nSection one says please kill the job.\n\n---\n\nEnd.\n"
        self.assertIn("banned-word", rules(text))

    def test_real_front_matter_is_still_skipped(self):
        text = "---\nname: kill-switch\ndescription: please read\n---\n\nBody.\n"
        self.assertNotIn("banned-word", rules(text))

    def test_nested_list_items_are_checked(self):
        self.assertIn("banned-word", rules("- Top item\n    - Nested says please kill it.\n"))

    def test_inline_code_does_not_fake_a_double_space(self):
        self.assertNotIn("double-space", rules("Run the setup script. `gcloud init` creates the project."))

    def test_real_double_space_is_flagged(self):
        self.assertIn("double-space", rules("First sentence.  Second sentence."))

    def test_proper_noun_heading_is_not_title_case(self):
        self.assertNotIn("heading-case", rules("## Deploy to Google Cloud\n"))

    def test_real_title_case_is_flagged(self):
        self.assertIn("heading-case", rules("## Getting Started With The Widget API\n"))

    def test_user_agent_is_not_the_reader(self):
        self.assertNotIn("the-user", rules("The user agent string is logged."))

    def test_the_user_as_reader_is_flagged(self):
        self.assertIn("the-user", rules("The user must sign in first."))

    def test_us_timezone_is_not_first_person(self):
        self.assertNotIn("first-person", rules("Use US and Canadian Pacific Standard Time (UTC-8)."))

    def test_organizational_we_is_flagged_at_info(self):
        self.assertIn("first-person", rules("We recommend rotating keys."))

    def test_product_name_is_not_condescending(self):
        self.assertNotIn("condescending", rules("Amazon Simple Storage Service stores objects."))

    def test_lowercase_simply_is_flagged(self):
        self.assertIn("condescending", rules("Simply restart the service."))

    def test_resource_utilization_is_allowed(self):
        self.assertNotIn("utilize", rules("When CPU utilization exceeds 75%, add a node."))

    def test_utilize_as_verb_is_flagged(self):
        self.assertIn("utilize", rules("You can utilize the cache."))

    def test_serial_comma_heuristic_was_removed(self):
        self.assertNotIn("serial-comma", rules("In addition, you can start and stop the service."))

    def test_long_sentence_starting_with_code_span(self):
        text = "`gcloud` " + "processes each request and " * 8 + "returns a result."
        self.assertIn("long-sentence", rules(text))

    def test_hit_enter_is_flagged(self):
        self.assertIn("banned-word", rules("Then hit Enter to continue."))

    def test_cache_hit_rate_is_allowed(self):
        self.assertNotIn("banned-word", rules("Check the cache hit rate."))

    def test_cli_flag_is_not_an_em_dash(self):
        self.assertNotIn("double-hyphen", rules("Pass the --verbose flag."))

    def test_spaced_dimensions_are_flagged(self):
        self.assertIn("dimensions", rules("Renders at 1280 \u00d7 1024 by default."))
        self.assertIn("dimensions", rules("Renders at 1280 x 1024 by default."))

    def test_compliant_dimensions_are_clean(self):
        self.assertNotIn("dimensions", rules("Renders at 1280x1024 by default."))

    def test_missing_unit_space_is_flagged(self):
        self.assertIn("unit-space", rules("Allocate 64GB of memory."))

    def test_correct_unit_space_is_clean(self):
        self.assertNotIn("unit-space", rules("Allocate 64 GB of memory."))

    def test_please_is_advisory_not_a_hard_ban(self):
        found = [f for f in lint_text("Please click Save.") if f.rule == "please"]
        self.assertTrue(found)
        self.assertEqual(found[0].level, "info")

    def test_unsourced_rules_are_advisory(self):
        """Rules with no entry in either guide report at info, not warning,
        so a warning-level pass only surfaces sourced rules."""
        for text, rule in [("This allows you to scale.", "wordy"),
                           ("The fix is obvious.", "condescending")]:
            found = [f for f in lint_text(text) if f.rule == rule]
            self.assertTrue(found, rule)
            self.assertEqual(found[0].level, "info", rule)

    def test_sourced_condescension_stays_a_warning(self):
        found = [f for f in lint_text("Simply restart it.") if f.rule == "condescending"]
        self.assertTrue(found)
        self.assertEqual(found[0].level, "warning")

    def test_comma_inside_decimal_is_flagged(self):
        self.assertIn("decimal-comma", rules("The price is $0.006,653 per vCPU hour."))

    def test_thousands_separator_is_clean(self):
        self.assertNotIn("decimal-comma", rules("The cluster holds 1,532,784 rows."))

    def test_plain_decimal_is_clean(self):
        self.assertNotIn("decimal-comma", rules("The price is $0.006653 per vCPU hour."))


if __name__ == "__main__":
    unittest.main(verbosity=2)
