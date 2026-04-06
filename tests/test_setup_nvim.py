import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import setup


class EnsureLazyVimTests(unittest.TestCase):
    def test_ensure_lazyvim_writes_insert_mode_jj_escape_plugin(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="nvim")

                def fake_clone_repo_to_path(repo, dest, strip_git=False):
                    dest.mkdir(parents=True, exist_ok=True)

                bootstrap.clone_repo_to_path = fake_clone_repo_to_path
                bootstrap.ensure_lazyvim()

                plugin_file = Path(home_dir) / ".config" / "nvim" / "lua" / "plugins" / "jj-escape.lua"

                self.assertTrue(plugin_file.exists())
                plugin_content = plugin_file.read_text(encoding="utf-8")
                self.assertIn('mode = "i"', plugin_content)
                self.assertIn('{ "jj", "<Esc>"', plugin_content)


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
