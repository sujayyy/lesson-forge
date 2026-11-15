import os
import unittest
from unittest.mock import patch
from groq_run import configure
from lesson_forge.provider import APIProvider


class LauncherTests(unittest.TestCase):
    def test_evidence_options_preserve_exact_text(self):
        from lesson_forge.prompts import evidence_candidates
        lesson = '## Limits\n\nA claim. [S1]\nA claim. [S1]\n  Keep spacing.\n'
        self.assertEqual(evidence_candidates(lesson), ['## Limits', 'A claim. [S1]', '  Keep spacing.'])
        self.assertTrue(all(line in lesson for line in evidence_candidates(lesson)))

    def test_overrides_malformed_environment_without_changing_key(self):
        with patch.dict(os.environ, {"LLM_BASE_URL": "[https://wrong](https://wrong)", "LLM_API_KEY": "gsk_test"}):
            configure()
            provider = APIProvider()
            self.assertEqual(provider.base_url, "https://api.groq.com/openai/v1")
            self.assertEqual(provider.key, "gsk_test")
            self.assertEqual(provider.min_interval, 65)
            self.assertEqual(provider.max_tokens, 4000)
