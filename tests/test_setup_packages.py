import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import setup


class InstallCorePackagesTests(unittest.TestCase):
    def test_install_core_packages_includes_required_cli_tools(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="packages")
                captured = {}

                bootstrap.resolve_package = lambda key: "pkg-" + key

                def fake_install_system_packages(packages, soft_fail=False, cask=False):
                    captured["packages"] = packages
                    captured["soft_fail"] = soft_fail
                    captured["cask"] = cask

                bootstrap.install_system_packages = fake_install_system_packages
                bootstrap.install_core_packages()

                expected = [
                    "pkg-zsh",
                    "pkg-git",
                    "pkg-curl",
                    "pkg-wget",
                    "pkg-jq",
                    "pkg-ripgrep",
                    "pkg-fd",
                    "pkg-fzf",
                    "pkg-tmux",
                    "pkg-neovim",
                    "pkg-htop",
                    "pkg-node",
                    "pkg-go",
                    "pkg-bat",
                    "pkg-eza",
                    "pkg-zoxide",
                    "pkg-lazygit",
                    "pkg-atuin",
                    "pkg-oh-my-posh",
                    "pkg-yq",
                    "pkg-you-get",
                ]

                self.assertEqual(captured["packages"], expected)
                self.assertFalse(captured["soft_fail"])
                self.assertFalse(captured["cask"])


class InstallPythonToolsTests(unittest.TestCase):
    def test_install_python_tools_installs_only_uv_and_updates_local_bin_path(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="packages")
                installed = []
                prepended = []

                bootstrap.ensure_pip = lambda: True
                bootstrap.pip_install_user = lambda packages: installed.append(packages) or True
                bootstrap.prepend_path = lambda path: prepended.append(Path(path))

                bootstrap.install_python_tools()

                self.assertEqual(installed, [["uv"]])
                self.assertEqual(prepended, [Path(home_dir) / ".local" / "bin"])
                self.assertNotIn(["pipx"], installed)


class InstallOptionalSystemPackagesTests(unittest.TestCase):
    def test_install_optional_system_packages_on_macos_respects_switches(self):
        with tempfile.TemporaryDirectory() as home_dir:
            env = {
                "HOME": home_dir,
                "BOOTSTRAP_INSTALL_VSCODE": "1",
                "BOOTSTRAP_INSTALL_RECTANGLE": "0",
                "BOOTSTRAP_INSTALL_STATS": "1",
            }
            with mock.patch.dict(os.environ, env, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="packages")
                bootstrap.system = "darwin"
                installed = []
                font_calls = []

                def fake_install_optional_app_cask(key, app_path):
                    installed.append((key, Path(app_path)))

                bootstrap.install_optional_app_cask = fake_install_optional_app_cask
                bootstrap.ensure_jetbrains_nerd_font = lambda: font_calls.append("font")

                bootstrap.install_optional_system_packages()

                self.assertEqual(
                    installed,
                    [
                        ("vscode", Path("/Applications/Visual Studio Code.app")),
                        ("stats", Path("/Applications/Stats.app")),
                    ],
                )
                self.assertEqual(font_calls, ["font"])


if __name__ == "__main__":
    unittest.main()
