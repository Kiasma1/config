import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import setup


class OhMyPoshThemeTests(unittest.TestCase):
    def test_write_omp_theme_uses_repo_theme_file(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="shell")
                bootstrap.write_omp_theme()

                theme_file = Path(home_dir) / ".config" / "bootstrap-managed" / "oh-my-posh" / "lambda.omp.json"
                expected = (Path(setup.__file__).resolve().parent / "assets" / "oh-my-posh" / "lambda.omp.json").read_text(
                    encoding="utf-8"
                )

                self.assertTrue(theme_file.exists())
                self.assertEqual(theme_file.read_text(encoding="utf-8"), expected)


if __name__ == "__main__":
    unittest.main()
