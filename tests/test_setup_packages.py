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


if __name__ == "__main__":
    unittest.main()
