import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import setup


class HelixConfigTests(unittest.TestCase):
    def test_write_helix_config_uses_repo_config_file(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="helix")
                bootstrap.write_helix_config()

                config_file = Path(home_dir) / ".config" / "helix" / "config.toml"
                expected = (Path(setup.__file__).resolve().parent / "assets" / "helix" / "config.toml").read_text(
                    encoding="utf-8"
                )

                self.assertTrue(config_file.exists())
                self.assertEqual(config_file.read_text(encoding="utf-8"), expected)

    def test_remove_managed_nvim_config_removes_only_bootstrap_managed_dir(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="helix")
                nvim_dir = Path(home_dir) / ".config" / "nvim"
                nvim_dir.mkdir(parents=True)
                (nvim_dir / ".bootstrap-managed").write_text("managed_by=setup.py\n", encoding="utf-8")
                (nvim_dir / "init.lua").write_text("return {}\n", encoding="utf-8")

                bootstrap.remove_managed_nvim_config()

                self.assertFalse(nvim_dir.exists())


class StarshipConfigTests(unittest.TestCase):
    def test_write_starship_config_uses_repo_theme_file(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="shell")
                bootstrap.write_starship_config()

                config_file = Path(home_dir) / ".config" / "bootstrap-managed" / "starship.toml"
                expected = (Path(setup.__file__).resolve().parent / "assets" / "starship" / "starship.toml").read_text(
                    encoding="utf-8"
                )

                self.assertTrue(config_file.exists())
                self.assertEqual(config_file.read_text(encoding="utf-8"), expected)

    def test_starship_theme_keeps_lambda_git_and_status_shape(self):
        expected = (Path(setup.__file__).resolve().parent / "assets" / "starship" / "starship.toml").read_text(
            encoding="utf-8"
        )

        self.assertIn('palette = "bootstrap"', expected)
        self.assertIn('format = "$directory$git_branch$git_commit$git_state$git_status$status$character"', expected)
        self.assertIn('right_format = "$cmd_duration"', expected)
        self.assertIn('format = "[ · ](fg:muted)[git:](fg:foreground)[$branch](fg:accent)"', expected)
        self.assertIn('format = "[ · exit:$status](fg:error)"', expected)
        self.assertIn('success_symbol = "[ λ ](fg:accent)"', expected)
        self.assertIn('[git_status]', expected)


class ZshrcGenerationTests(unittest.TestCase):
    def test_write_zshrc_uses_starship_and_helix_without_lazygit_or_nvim(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="shell")
                bootstrap.write_zshrc()

                zshrc_file = Path(home_dir) / ".zshrc"
                content = zshrc_file.read_text(encoding="utf-8")

                self.assertIn('eval "$(starship init zsh)"', content)
                self.assertIn('export EDITOR="${BOOTSTRAP_EDITOR_BIN}"', content)
                self.assertIn('alias vim="${BOOTSTRAP_EDITOR_BIN}"', content)
                self.assertIn('alias vhelix="${BOOTSTRAP_EDITOR_BIN} ~/.config/helix/config.toml"', content)
                self.assertIn("alias t='tldr'", content)
                self.assertIn("alias ts='tldr --search'", content)
                self.assertIn("alias tu='tldr --update'", content)
                self.assertIn("alias helpme='cmdh'", content)
                self.assertIn('tldrp() {', content)
                self.assertIn('cmdh() {', content)
                self.assertNotIn("OMZP::git", content)
                self.assertNotIn("lazygit", content)
                self.assertNotIn("nvim", content)


if __name__ == "__main__":
    unittest.main()
