#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import datetime
import os
import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


if sys.version_info < (3, 6):
    raise SystemExit("Python 3.6+ is required")


def log(msg):
    print(msg)


def info(msg):
    print("[ok] {0}".format(msg))


def warn(msg):
    print("[warn] {0}".format(msg), file=sys.stderr)


def err(msg):
    print("[err] {0}".format(msg), file=sys.stderr)


def run(cmd, check=True, capture=False, env=None, cwd=None):
    kwargs = {
        "check": check,
        "env": env,
        "cwd": cwd,
        "universal_newlines": True,
    }
    if capture:
        kwargs["stdout"] = subprocess.PIPE
        kwargs["stderr"] = subprocess.PIPE
    return subprocess.run(cmd, **kwargs)


def command_exists(name, env=None):
    search_path = None
    if env is not None:
        search_path = env.get("PATH")
    return shutil.which(name, path=search_path) is not None


def app_exists(app_path):
    return Path(app_path).is_dir()


def copy_path(src, dst):
    src = Path(src)
    dst = Path(dst)

    if src.is_symlink():
        target = os.readlink(str(src))
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() or dst.is_symlink():
            if dst.is_dir() and not dst.is_symlink():
                shutil.rmtree(str(dst))
            else:
                dst.unlink()
        os.symlink(target, str(dst))
        return

    if src.is_dir():
        if dst.exists():
            shutil.rmtree(str(dst))
        shutil.copytree(str(src), str(dst), symlinks=True)
        return

    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))


class Bootstrap(object):
    PACKAGE_MATRIX = {
        "zsh": {
            "brew": "zsh",
            "apt": "zsh",
            "dnf": "zsh",
            "yum": "zsh",
            "pacman": "zsh",
            "zypper": "zsh",
            "apk": "zsh",
        },
        "git": {
            "brew": "git",
            "apt": "git",
            "dnf": "git",
            "yum": "git",
            "pacman": "git",
            "zypper": "git",
            "apk": "git",
        },
        "curl": {
            "brew": "curl",
            "apt": "curl",
            "dnf": "curl",
            "yum": "curl",
            "pacman": "curl",
            "zypper": "curl",
            "apk": "curl",
        },
        "wget": {
            "brew": "wget",
            "apt": "wget",
            "dnf": "wget",
            "yum": "wget",
            "pacman": "wget",
            "zypper": "wget",
            "apk": "wget",
        },
        "jq": {
            "brew": "jq",
            "apt": "jq",
            "dnf": "jq",
            "yum": "jq",
            "pacman": "jq",
            "zypper": "jq",
            "apk": "jq",
        },
        "ripgrep": {
            "brew": "ripgrep",
            "apt": "ripgrep",
            "dnf": "ripgrep",
            "yum": "ripgrep",
            "pacman": "ripgrep",
            "zypper": "ripgrep",
            "apk": "ripgrep",
        },
        "fd": {
            "brew": "fd",
            "apt": "fd-find",
            "dnf": "fd-find",
            "yum": "fd-find",
            "pacman": "fd",
            "zypper": "fd",
            "apk": "fd",
            "ubuntu": "fd-find",
            "debian": "fd-find",
            "fedora": "fd-find",
            "centos": "fd-find",
            "rhel": "fd-find",
            "rocky": "fd-find",
            "almalinux": "fd-find",
            "arch": "fd",
            "manjaro": "fd",
            "opensuse-tumbleweed": "fd",
            "opensuse-leap": "fd",
            "alpine": "fd",
        },
        "fzf": {
            "brew": "fzf",
            "apt": "fzf",
            "dnf": "fzf",
            "yum": "fzf",
            "pacman": "fzf",
            "zypper": "fzf",
            "apk": "fzf",
        },
        "tmux": {
            "brew": "tmux",
            "apt": "tmux",
            "dnf": "tmux",
            "yum": "tmux",
            "pacman": "tmux",
            "zypper": "tmux",
            "apk": "tmux",
        },
        "neovim": {
            "brew": "neovim",
            "apt": "neovim",
            "dnf": "neovim",
            "yum": "neovim",
            "pacman": "neovim",
            "zypper": "neovim",
            "apk": "neovim",
        },
        "htop": {
            "brew": "htop",
            "apt": "htop",
            "dnf": "htop",
            "yum": "htop",
            "pacman": "htop",
            "zypper": "htop",
            "apk": "htop",
        },
        "python3-pip": {
            "brew": "python",
            "apt": "python3-pip",
            "dnf": "python3-pip",
            "yum": "python3-pip",
            "pacman": "python-pip",
            "zypper": "python3-pip",
            "apk": "py3-pip",
            "ubuntu": "python3-pip",
            "debian": "python3-pip",
            "fedora": "python3-pip",
            "centos": "python3-pip",
            "rhel": "python3-pip",
            "rocky": "python3-pip",
            "almalinux": "python3-pip",
            "arch": "python-pip",
            "manjaro": "python-pip",
            "opensuse-tumbleweed": "python3-pip",
            "opensuse-leap": "python3-pip",
            "alpine": "py3-pip",
        },
        "node": {
            "brew": "node",
            "apt": "nodejs",
            "dnf": "nodejs",
            "yum": "nodejs",
            "pacman": "nodejs",
            "zypper": "nodejs",
            "apk": "nodejs",
        },
        "go": {
            "brew": "go",
            "apt": "golang-go",
            "dnf": "golang",
            "yum": "golang",
            "pacman": "go",
            "zypper": "go",
            "apk": "go",
            "ubuntu": "golang-go",
            "debian": "golang-go",
            "fedora": "golang",
            "centos": "golang",
            "rhel": "golang",
            "rocky": "golang",
            "almalinux": "golang",
            "arch": "go",
            "manjaro": "go",
            "opensuse-tumbleweed": "go",
            "opensuse-leap": "go",
            "alpine": "go",
        },
        "bat": {
            "brew": "bat",
            "apt": "bat",
            "dnf": "bat",
            "yum": "bat",
            "pacman": "bat",
            "zypper": "bat",
            "apk": "bat",
        },
        "eza": {
            "brew": "eza",
            "apt": "eza",
            "dnf": "eza",
            "yum": "eza",
            "pacman": "eza",
            "zypper": "eza",
            "apk": "eza",
        },
        "zoxide": {
            "brew": "zoxide",
            "apt": "zoxide",
            "dnf": "zoxide",
            "yum": "zoxide",
            "pacman": "zoxide",
            "zypper": "zoxide",
            "apk": "zoxide",
        },
        "lazygit": {
            "brew": "lazygit",
            "apt": "lazygit",
            "dnf": "lazygit",
            "yum": "lazygit",
            "pacman": "lazygit",
            "zypper": "lazygit",
            "apk": "lazygit",
        },
        "atuin": {
            "brew": "atuin",
            "apt": "atuin",
            "dnf": "atuin",
            "yum": "atuin",
            "pacman": "atuin",
            "zypper": "atuin",
            "apk": "atuin",
        },
        "ghostty": {
            "brew_cask": "ghostty",
        },
        "rectangle": {
            "brew_cask": "rectangle",
        },
        "stats": {
            "brew_cask": "stats",
        },
        "vscode": {
            "brew_cask": "visual-studio-code",
        },
        "hammerspoon": {
            "brew_cask": "hammerspoon",
        },
        "oh-my-posh": {
            "brew": "oh-my-posh",
            "apt": "oh-my-posh",
            "dnf": "oh-my-posh",
            "yum": "oh-my-posh",
            "pacman": "oh-my-posh",
            "zypper": "oh-my-posh",
            "apk": "oh-my-posh",
        },
        "yq": {
            "brew": "yq",
            "apt": "yq",
            "dnf": "yq",
            "yum": "yq",
            "pacman": "yq",
            "zypper": "yq",
            "apk": "yq",
        },
        "you-get": {
            "brew": "you-get",
            "apt": "you-get",
            "dnf": "you-get",
            "yum": "you-get",
            "pacman": "you-get",
            "zypper": "you-get",
            "apk": "you-get",
        },
    }

    def __init__(self, dry_run=False, only="all"):
        self.dry_run = dry_run
        self.only = only
        self.home = Path.home()
        self.system = platform.system().lower()

        if self.system not in ("linux", "darwin"):
            raise SystemExit("Only Linux and macOS are supported")

        env = dict(os.environ)
        base_path = [
            "/opt/homebrew/bin",
            "/usr/local/bin",
            "/usr/bin",
            "/bin",
            "/usr/sbin",
            "/sbin",
            str(self.home / ".local" / "bin"),
        ]
        existing = env.get("PATH", "")
        env["PATH"] = ":".join(base_path + ([existing] if existing else []))
        self.env = env

        self.python_exe = sys.executable or "python3"
        self.pkg_manager = self.detect_package_manager()
        self.distro_id = self.detect_distro_id()
        self.repo_updated = False
        self.repo_root = Path(__file__).resolve().parent

        self.tx_dir = Path(tempfile.mkdtemp(prefix="bootstrap-tx-"))
        ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.backup_root = self.home / ".bootstrap-backups" / ts

        self.modified_paths = []
        self.soft_failures = []
        self.git_config_backups = {}

        self.config_home = Path(env.get("XDG_CONFIG_HOME", str(self.home / ".config")))
        self.data_home = Path(env.get("XDG_DATA_HOME", str(self.home / ".local" / "share")))
        self.cache_home = Path(env.get("XDG_CACHE_HOME", str(self.home / ".cache")))

        self.managed_root = self.config_home / "bootstrap-managed"
        self.zsh_managed_dir = self.managed_root / "zsh"
        self.zsh_proxy_file = self.zsh_managed_dir / "proxy.env"

        self.omp_dir = self.managed_root / "oh-my-posh"
        self.omp_theme_file = self.omp_dir / "lambda.omp.json"
        self.omp_theme_source_file = self.repo_root / "assets" / "oh-my-posh" / "lambda.omp.json"

        self.atuin_dir = self.config_home / "atuin"
        self.atuin_config_file = self.atuin_dir / "config.toml"

        self.ghostty_dir = self.config_home / "ghostty"
        self.ghostty_config_file = self.ghostty_dir / "config"

        self.hammerspoon_dir = self.home / ".hammerspoon"
        self.hammerspoon_init_file = self.hammerspoon_dir / "init.lua"
        self.hammerspoon_managed_file = self.hammerspoon_dir / "bootstrap-managed.lua"

        self.nvim_dir = self.config_home / "nvim"
        self.zinit_home = self.data_home / "zinit" / "zinit.git"

        self.enable_proxy = env.get("BOOTSTRAP_ENABLE_PROXY", "0")
        self.http_proxy = env.get("BOOTSTRAP_HTTP_PROXY", "http://127.0.0.1:7897")
        self.all_proxy = env.get("BOOTSTRAP_ALL_PROXY", "socks5://127.0.0.1:7897")

        self.install_vscode = env.get("BOOTSTRAP_INSTALL_VSCODE", "1")
        self.install_ghostty = env.get("BOOTSTRAP_INSTALL_GHOSTTY", env.get("BOOTSTRAP_INSTALL_ALACRITTY", "1"))
        self.install_rectangle = env.get("BOOTSTRAP_INSTALL_RECTANGLE", "1")
        self.install_stats = env.get("BOOTSTRAP_INSTALL_STATS", "0")
        self.install_hammerspoon = env.get("BOOTSTRAP_INSTALL_HAMMERSPOON", "1")
        self.ghostty_hotkey_enabled = env.get("BOOTSTRAP_GHOSTTY_HOTKEY", env.get("BOOTSTRAP_ALACRITTY_HOTKEY", "1"))
        self.ghostty_hotkey_mods = env.get(
            "BOOTSTRAP_GHOSTTY_HOTKEY_MODS",
            env.get("BOOTSTRAP_ALACRITTY_HOTKEY_MODS", "ctrl,alt"),
        )
        self.ghostty_hotkey_key = env.get(
            "BOOTSTRAP_GHOSTTY_HOTKEY_KEY",
            env.get("BOOTSTRAP_ALACRITTY_HOTKEY_KEY", "return"),
        )

        if not self.dry_run:
            self.backup_root.mkdir(parents=True, exist_ok=True)

    # ---------- shared ----------

    def dry(self, msg):
        log("[DRY-RUN] {0}".format(msg))

    def detect_package_manager(self):
        if self.system == "darwin":
            return "brew"

        if command_exists("apt-get", self.env):
            return "apt"
        if command_exists("dnf", self.env):
            return "dnf"
        if command_exists("yum", self.env):
            return "yum"
        if command_exists("pacman", self.env):
            return "pacman"
        if command_exists("zypper", self.env):
            return "zypper"
        if command_exists("apk", self.env):
            return "apk"

        raise RuntimeError("No supported package manager found")

    def detect_distro_id(self):
        if self.system != "linux":
            return ""

        os_release = Path("/etc/os-release")
        if not os_release.exists():
            return ""

        data = {}
        for line in os_release.read_text(encoding="utf-8", errors="ignore").splitlines():
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            data[k.strip()] = v.strip().strip('"').lower()

        return data.get("ID", "")

    def resolve_package(self, key):
        mapping = self.PACKAGE_MATRIX.get(key, {})
        if not mapping:
            return None

        if self.distro_id and self.distro_id in mapping:
            return mapping.get(self.distro_id)

        return mapping.get(self.pkg_manager)

    def sudo_prefix(self):
        if self.system == "darwin":
            return []
        if hasattr(os, "geteuid") and os.geteuid() == 0:
            return []
        if command_exists("sudo", self.env):
            return ["sudo"]
        return []

    def prepend_path(self, path_value):
        path_value = str(path_value)
        if not Path(path_value).exists():
            return
        parts = self.env.get("PATH", "").split(":")
        if path_value not in parts:
            self.env["PATH"] = "{0}:{1}".format(path_value, self.env.get("PATH", ""))

    def module_enabled(self, name):
        return self.only in ("all", name)

    # ---------- backups / writes ----------

    def record_backup(self, path_obj):
        if self.dry_run:
            self.dry("would backup {0} to {1}".format(path_obj, self.backup_root))
            return

        for existing, _ in self.modified_paths:
            if existing == path_obj:
                return

        if path_obj.exists() or path_obj.is_symlink():
            rel_name = "path-{0}".format(len(self.modified_paths))
            tx_backup = self.tx_dir / rel_name
            copy_path(path_obj, tx_backup)

            perm_backup = self.backup_root / rel_name
            copy_path(path_obj, perm_backup)

            self.modified_paths.append((path_obj, tx_backup))
        else:
            self.modified_paths.append((path_obj, None))

    def rollback_paths(self):
        if self.dry_run:
            return

        for path_obj, tx_backup in reversed(self.modified_paths):
            try:
                if path_obj.exists() or path_obj.is_symlink():
                    if path_obj.is_dir() and not path_obj.is_symlink():
                        shutil.rmtree(str(path_obj))
                    else:
                        path_obj.unlink()

                if tx_backup is None:
                    continue

                path_obj.parent.mkdir(parents=True, exist_ok=True)
                copy_path(tx_backup, path_obj)
            except Exception as ex:
                warn("rollback failed for {0}: {1}".format(path_obj, ex))

        for key, values in self.git_config_backups.items():
            try:
                run(["git", "config", "--global", "--unset-all", key], check=False, env=self.env)
                if values is None:
                    continue
                for value in values:
                    run(["git", "config", "--global", "--add", key, value], env=self.env)
            except Exception as ex:
                warn("git config rollback failed for {0}: {1}".format(key, ex))

    def write_file_if_changed(self, dest, content, mode=None):
        current = None
        if dest.exists() or dest.is_symlink():
            try:
                current = dest.read_text(encoding="utf-8")
            except Exception:
                current = None

        if current == content:
            info("unchanged: {0}".format(dest))
            return

        if self.dry_run:
            action = "would overwrite" if (dest.exists() or dest.is_symlink()) else "would create"
            self.dry("{0} {1}".format(action, dest))
            return

        self.record_backup(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(prefix=dest.name + ".", dir=str(dest.parent))
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)

            if mode is not None:
                tmp_path.chmod(mode)

            os.replace(str(tmp_path), str(dest))
        except Exception:
            try:
                tmp_path.unlink()
            except OSError:
                pass
            raise

    def remove_and_replace_dir(self, dest, source):
        if self.dry_run:
            self.dry("would replace directory {0}".format(dest))
            return

        self.record_backup(dest)
        if dest.exists() or dest.is_symlink():
            if dest.is_dir() and not dest.is_symlink():
                shutil.rmtree(str(dest))
            else:
                dest.unlink()
        os.replace(str(source), str(dest))

    def clone_repo_to_path(self, repo, dest, strip_git=False):
        if self.dry_run:
            self.dry("would clone {0} to {1}".format(repo, dest))
            return

        tmp_dir = Path(tempfile.mkdtemp(dir=str(self.tx_dir), prefix="clone-"))
        run(["git", "clone", "--depth=1", repo, str(tmp_dir)], env=self.env)
        if strip_git:
            shutil.rmtree(str(tmp_dir / ".git"), ignore_errors=True)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.remove_and_replace_dir(dest, tmp_dir)

    # ---------- package install ----------

    def ensure_xcode_clt(self):
        if self.system != "darwin":
            return

        log("[1/8] checking Xcode Command Line Tools")
        result = run(["xcode-select", "-p"], check=False, capture=True, env=self.env)
        if result.returncode == 0:
            info("xcode command line tools present")
            return

        if self.dry_run:
            self.dry("would trigger xcode-select --install")
            return

        warn("xcode command line tools not found")
        run(["xcode-select", "--install"], check=False, env=self.env)
        raise RuntimeError("finish Xcode Command Line Tools installation, then rerun")

    def ensure_brew(self):
        if self.system != "darwin":
            return

        log("[2/8] checking Homebrew")

        if (
            command_exists("brew", self.env)
            or Path("/opt/homebrew/bin/brew").exists()
            or Path("/usr/local/bin/brew").exists()
        ):
            self.load_brew_shellenv()
            info("Homebrew present")
            return

        if self.dry_run:
            self.dry("would install Homebrew")
            return

        warn("Homebrew not found, installing")
        run(
            [
                "/bin/bash",
                "-lc",
                '$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)',
            ],
            env=self.env,
        )
        self.load_brew_shellenv()
        info("Homebrew installed")

    def load_brew_shellenv(self):
        brew_bin = None
        for candidate in (Path("/opt/homebrew/bin/brew"), Path("/usr/local/bin/brew")):
            if candidate.exists():
                brew_bin = candidate
                break

        if brew_bin is None:
            found = shutil.which("brew", path=self.env.get("PATH", ""))
            if found:
                brew_bin = Path(found)

        if brew_bin is None:
            if self.dry_run:
                self.dry("brew not found yet; would load shellenv after install")
                return
            raise RuntimeError("brew not found")

        result = run([str(brew_bin), "--prefix"], capture=True, env=self.env)
        prefix = result.stdout.strip()
        if not prefix:
            if self.dry_run:
                self.dry("brew prefix not available yet")
                return
            raise RuntimeError("brew prefix not found")

        self.prepend_path(Path(prefix) / "bin")
        self.prepend_path(Path(prefix) / "sbin")
        self.prepend_path(Path(prefix) / "opt" / "node@20" / "bin")
        self.prepend_path(self.home / ".local" / "bin")
        self.prepend_path("/Applications/Visual Studio Code.app/Contents/Resources/app/bin")

    def update_repo_once(self):
        if self.repo_updated:
            return

        pm = self.pkg_manager
        if pm == "brew":
            cmd = ["brew", "update"]
        elif pm == "apt":
            cmd = self.sudo_prefix() + ["apt-get", "update"]
        elif pm == "dnf":
            cmd = self.sudo_prefix() + ["dnf", "makecache"]
        elif pm == "yum":
            cmd = self.sudo_prefix() + ["yum", "makecache"]
        elif pm == "pacman":
            cmd = []
        elif pm == "zypper":
            cmd = self.sudo_prefix() + ["zypper", "refresh"]
        elif pm == "apk":
            cmd = self.sudo_prefix() + ["apk", "update"]
        else:
            cmd = []

        if not cmd:
            return

        if self.dry_run:
            self.dry("would refresh package metadata: {0}".format(" ".join(cmd)))
        else:
            run(cmd, env=self.env)

        self.repo_updated = True

    def install_system_packages(self, packages, soft_fail=False, cask=False):
        packages = [p for p in packages if p]
        if not packages:
            return True

        self.update_repo_once()
        pm = self.pkg_manager

        if pm == "brew":
            cmd = ["brew", "install"]
            if cask:
                cmd.append("--cask")
            cmd += packages
        elif pm == "apt":
            cmd = self.sudo_prefix() + ["apt-get", "install", "-y"] + packages
        elif pm == "dnf":
            cmd = self.sudo_prefix() + ["dnf", "install", "-y"] + packages
        elif pm == "yum":
            cmd = self.sudo_prefix() + ["yum", "install", "-y"] + packages
        elif pm == "pacman":
            cmd = self.sudo_prefix() + ["pacman", "-S", "--noconfirm", "--needed"] + packages
        elif pm == "zypper":
            cmd = self.sudo_prefix() + ["zypper", "--non-interactive", "install"] + packages
        elif pm == "apk":
            cmd = self.sudo_prefix() + ["apk", "add", "--no-cache"] + packages
        else:
            raise RuntimeError("unsupported package manager: {0}".format(pm))

        if self.dry_run:
            self.dry("would install via {0}: {1}".format(pm, " ".join(packages)))
            return True

        result = run(cmd, check=False, env=self.env)
        if result.returncode == 0:
            return True

        if soft_fail:
            warn("package install failed: {0}".format(" ".join(packages)))
            self.soft_failures.append("package install failed: {0}".format(" ".join(packages)))
            return False

        raise RuntimeError("package install failed: {0}".format(" ".join(packages)))

    def install_core_packages(self):
        log("[3/8] installing core packages")
        keys = [
            "zsh",
            "git",
            "curl",
            "wget",
            "jq",
            "ripgrep",
            "fd",
            "fzf",
            "tmux",
            "neovim",
            "htop",
            "node",
            "go",
            "bat",
            "eza",
            "zoxide",
            "lazygit",
            "atuin",
            "oh-my-posh",
            "yq",
            "you-get",
        ]
        pkgs = []
        for key in keys:
            pkg = self.resolve_package(key)
            if pkg:
                pkgs.append(pkg)
        self.install_system_packages(pkgs, soft_fail=False, cask=False)

    def install_optional_system_packages(self):
        log("[4/8] installing optional desktop apps")

        if self.system == "darwin":
            if self.install_vscode == "1":
                self.install_optional_app_cask("vscode", Path("/Applications/Visual Studio Code.app"))
            if self.install_rectangle == "1":
                self.install_optional_app_cask("rectangle", Path("/Applications/Rectangle.app"))
            if self.install_stats == "1":
                self.install_optional_app_cask("stats", Path("/Applications/Stats.app"))
            self.ensure_jetbrains_nerd_font()

    def install_hotkey_dependencies(self):
        if self.system != "darwin":
            return

        if self.install_ghostty == "1":
            self.install_optional_app_cask("ghostty", Path("/Applications/Ghostty.app"))

        if self.install_hammerspoon == "1" and self.ghostty_hotkey_enabled == "1":
            self.install_optional_app_cask("hammerspoon", Path("/Applications/Hammerspoon.app"))

    def install_optional_app_cask(self, key, app_path):
        cask = self.resolve_package(key)
        if not cask:
            return

        app_path = Path(app_path)

        if app_exists(app_path):
            warn("app already exists at {0}, skipping {1}".format(app_path, cask))
            return

        self.install_system_packages([cask], soft_fail=True, cask=True)

    def ensure_jetbrains_nerd_font(self):
        font_dir = self.home / "Library" / "Fonts"
        patterns = [
            "JetBrainsMono* Nerd Font*.*",
            "JetBrainsMonoNLNerdFont-*.*",
            "JetBrainsMonoNerdFont-*.*",
        ]
        for pattern in patterns:
            if any(font_dir.glob(pattern)):
                warn("JetBrains Mono Nerd Font already exists, skipping install")
                return

        self.install_system_packages(["font-jetbrains-mono-nerd-font"], soft_fail=True, cask=True)

    def ensure_pip(self):
        result = run([self.python_exe, "-m", "pip", "--version"], check=False, capture=True, env=self.env)
        if result.returncode == 0:
            return True

        if self.dry_run:
            self.dry("would ensure pip is available for {0}".format(self.python_exe))
            return True

        result = run([self.python_exe, "-m", "ensurepip", "--upgrade"], check=False, capture=True, env=self.env)
        if result.returncode == 0:
            return True

        pkg = self.resolve_package("python3-pip")
        if pkg:
            self.install_system_packages([pkg], soft_fail=True, cask=False)

        result = run([self.python_exe, "-m", "pip", "--version"], check=False, capture=True, env=self.env)
        return result.returncode == 0

    def pip_install_user(self, packages):
        if not packages:
            return True

        if self.dry_run:
            self.dry("would install python user packages: {0}".format(" ".join(packages)))
            return True

        base = [self.python_exe, "-m", "pip", "install", "--user", "--upgrade"] + packages
        result = run(base, check=False, capture=True, env=self.env)
        if result.returncode == 0:
            return True

        fallback = [self.python_exe, "-m", "pip", "install", "--user", "--upgrade", "--break-system-packages"] + packages
        result2 = run(fallback, check=False, capture=True, env=self.env)
        return result2.returncode == 0

    def record_git_config_backup(self, key):
        if key in self.git_config_backups:
            return

        result = run(["git", "config", "--global", "--get-all", key], check=False, capture=True, env=self.env)
        if result.returncode == 0:
            self.git_config_backups[key] = result.stdout.splitlines()
        else:
            self.git_config_backups[key] = None

    def install_python_tools(self):
        log("[5/8] installing python user tools")
        if not self.ensure_pip():
            warn("pip not available, skipping python user tools")
            self.soft_failures.append("pip not available, skipping python user tools")
            return

        for pkg in ("uv",):
            ok = self.pip_install_user([pkg])
            if ok:
                info("python user tool installed: {0}".format(pkg))
            else:
                warn("python user tool install failed: {0}".format(pkg))
                self.soft_failures.append("python user tool install failed: {0}".format(pkg))

        self.prepend_path(self.home / ".local" / "bin")

    def ensure_zinit(self):
        log("[6/8] managing zinit")
        self.clone_repo_to_path("https://github.com/zdharma-continuum/zinit.git", self.zinit_home, strip_git=False)
        if not self.dry_run:
            info("zinit refreshed")

    def ensure_lazyvim(self):
        log("[7/8] managing Neovim / LazyVim")
        self.clone_repo_to_path("https://github.com/LazyVim/starter", self.nvim_dir, strip_git=True)

        now_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.write_file_if_changed(
            self.nvim_dir / "lazyvim.json",
            """{
  \"extras\": [
    \"lazyvim.plugins.extras.coding.yanky\",
    \"lazyvim.plugins.extras.editor.fzf\",
    \"lazyvim.plugins.extras.editor.mini-files\",
    \"lazyvim.plugins.extras.lang.json\",
    \"lazyvim.plugins.extras.lang.markdown\",
    \"lazyvim.plugins.extras.lang.toml\",
    \"lazyvim.plugins.extras.lang.yaml\",
    \"lazyvim.plugins.extras.ui.mini-animate\"
  ],
  \"version\": 6
}
""",
            0o644,
        )

        self.write_file_if_changed(
            self.nvim_dir / ".neoconf.json",
            """{
  \"neodev\": {
    \"library\": {
      \"enabled\": true,
      \"plugins\": true
    }
  },
  \"neoconf\": {
    \"plugins\": {
      \"lua_ls\": {
        \"enabled\": true
      }
    }
  }
}
""",
            0o644,
        )

        self.write_file_if_changed(
            self.nvim_dir / ".bootstrap-managed",
            "managed_by=setup.py\nmanaged_at={0}\n".format(now_text),
            0o644,
        )
        if not self.dry_run:
            info("LazyVim refreshed")

    def write_proxy_file(self):
        if self.enable_proxy == "1":
            content = (
                "# Managed by setup.py\n"
                'export http_proxy="{0}"\n'
                'export https_proxy="{0}"\n'
                'export all_proxy="{1}"\n'
            ).format(self.http_proxy, self.all_proxy)
        else:
            content = "# Managed by setup.py\n# Proxy disabled.\n"
        self.write_file_if_changed(self.zsh_proxy_file, content, 0o644)

    def write_atuin_config(self):
        content = """# Managed by setup.py
auto_sync = false
update_check = false
sync_frequency = \"1h\"
style = \"compact\"
inline_height = 20
enter_accept = true
filter_mode = \"global\"
workspaces = true
"""
        self.write_file_if_changed(self.atuin_config_file, content, 0o644)

    def write_omp_theme(self):
        content = self.omp_theme_source_file.read_text(encoding="utf-8")
        self.write_file_if_changed(self.omp_theme_file, content, 0o644)

    def write_zprofile(self):
        lines = [
            "# Managed by setup.py",
            'export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"',
        ]
        if self.system == "darwin":
            lines += [
                "",
                "if [ -x /opt/homebrew/bin/brew ]; then",
                '  eval "$(/opt/homebrew/bin/brew shellenv)"',
                "elif [ -x /usr/local/bin/brew ]; then",
                '  eval "$(/usr/local/bin/brew shellenv)"',
                "fi",
            ]
        lines += [
            "",
            'export PATH="${HOME}/.local/bin:${PATH}"',
        ]
        if self.system == "darwin":
            lines += [
                "",
                'if [ -d "/Applications/Visual Studio Code.app/Contents/Resources/app/bin" ]; then',
                '  export PATH="/Applications/Visual Studio Code.app/Contents/Resources/app/bin:${PATH}"',
                "fi",
            ]
        else:
            lines += [
                "",
                'if [ -d "/usr/share/code/bin" ]; then',
                '  export PATH="/usr/share/code/bin:${PATH}"',
                "fi",
                'if [ -d "/snap/bin" ]; then',
                '  export PATH="/snap/bin:${PATH}"',
                "fi",
            ]
        content = "\n".join(lines) + "\n"

        self.write_file_if_changed(self.home / ".zprofile", content, 0o644)

    def write_zshrc(self):
        finder_cmd = "open ." if self.system == "darwin" else "xdg-open ."

        template = r'''# Managed by setup.py

if [ -f "${HOME}/.zprofile" ]; then
  source "${HOME}/.zprofile"
fi

if [ -f "__ZSH_PROXY_FILE__" ]; then
  source "__ZSH_PROXY_FILE__"
fi

export TERM="xterm-256color"
export EDITOR="nvim"
export VISUAL="nvim"
export PAGER="less"
export LESS="-FRX"

_fd_cmd() {
  if command -v fd >/dev/null 2>&1; then
    command fd "$@"
  elif command -v fdfind >/dev/null 2>&1; then
    command fdfind "$@"
  else
    return 127
  fi
}

_bat_cmd() {
  if command -v bat >/dev/null 2>&1; then
    command bat "$@"
  elif command -v batcat >/dev/null 2>&1; then
    command batcat "$@"
  else
    return 127
  fi
}

_ls_cmd() {
  if command -v eza >/dev/null 2>&1; then
    command eza "$@"
  else
    command ls "$@"
  fi
}

if command -v oh-my-posh >/dev/null 2>&1 && [ "${TERM_PROGRAM:-}" != "Apple_Terminal" ]; then
  eval "$(oh-my-posh init zsh --config "__OMP_THEME_FILE__")"
fi

ZINIT_HOME="__ZINIT_HOME__"
if [ -f "${ZINIT_HOME}/zinit.zsh" ]; then
  source "${ZINIT_HOME}/zinit.zsh"
  zinit snippet OMZP::git
  zinit snippet OMZP::sudo
  zinit light zsh-users/zsh-completions
fi

autoload -Uz compinit
mkdir -p "__CACHE_ZSH_DIR__"
compinit -C -d "__CACHE_ZSH_DIR__/zcompdump"

if [ -f "${ZINIT_HOME}/zinit.zsh" ]; then
  zinit light Aloxaf/fzf-tab
  zinit light zsh-users/zsh-autosuggestions
  zinit light zsh-users/zsh-syntax-highlighting
fi

if command -v atuin >/dev/null 2>&1; then
  eval "$(atuin init zsh --disable-up-arrow)"
  typeset -ga ZSH_AUTOSUGGEST_STRATEGY
  ZSH_AUTOSUGGEST_STRATEGY=(atuin completion history)
fi

bindkey -e
bindkey '^p' history-search-backward
bindkey '^n' history-search-forward

HISTSIZE=5000
HISTFILE="${HOME}/.zsh_history"
SAVEHIST="${HISTSIZE}"
setopt appendhistory sharehistory hist_ignore_space hist_ignore_all_dups hist_save_no_dups hist_find_no_dups

zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'
zstyle ':completion:*' menu no
zstyle ':fzf-tab:complete:cd:*' fzf-preview '_ls_cmd -a "$realpath" 2>/dev/null || true'
zstyle ':fzf-tab:complete:__zoxide_z:*' fzf-preview '_ls_cmd -a "$realpath" 2>/dev/null || true'
ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=8'

if command -v fzf >/dev/null 2>&1; then
  eval "$(fzf --zsh)"
fi

if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
fi

alias vim='nvim'
alias vi='nvim'
alias c='clear'
alias rz='exec zsh -l'
alias reloadz='exec zsh -l'
alias md='mkdir -p'
alias py='python3'
alias lg='lazygit'
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

alias tm='tmux'
alias tma='tmux attach -t'
alias tml='tmux ls'
alias tmn='tmux new -s'
alias tmc='tmux new-session -A -s'
alias tmd='tmux detach'
alias tmk='tmux kill-session -t'

if command -v eza >/dev/null 2>&1; then
  alias ls='eza'
  alias la='eza -a --git --color-scale'
  alias ll='eza -lbGF --git'
  alias llm='eza -lbGd --git --sort=modified'
  alias lt='eza --tree --level=2'
  alias lta='eza --tree --all --level=2'
  alias l1='eza -1'
else
  alias la='ls -la'
  alias ll='ls -lah'
fi

if command -v bat >/dev/null 2>&1; then
  alias cat='bat --paging=never --style=plain'
  alias catp='bat --paging=never'
elif command -v batcat >/dev/null 2>&1; then
  alias cat='batcat --paging=never --style=plain'
  alias catp='batcat --paging=never'
fi

if command -v htop >/dev/null 2>&1; then
  alias top='htop'
fi

alias j='jq'
alias y='yq'
alias hh='atuin search'
alias hhi='atuin search --interactive'
alias hs='atuin stats'

alias ports='lsof -nP -iTCP -sTCP:LISTEN'
alias psg='ps aux | rg -i'
alias myip='curl ip-api.com'
alias finder='__FINDER_CMD__'

alias gs='git status -sb'
alias ga='git add'
alias gaa='git add -A'
alias gc='git commit'
alias gca='git commit --amend'
alias gcm='git commit -m'
alias gco='git checkout'
alias gcb='git checkout -b'
alias gsw='git switch'
alias gswc='git switch -c'
alias gb='git branch'
alias gba='git branch -a'
alias gd='git diff'
alias gds='git diff --staged'
alias gl='git pull'
alias gp='git push'
alias gpf='git push --force-with-lease'
alias gcl='git clone'
alias gfetch='git fetch --all --prune'
alias gundo='git reset --soft HEAD~1'
alias gst='git stash'
alias gsta='git stash apply'
alias gsp='git stash pop'
alias groot='cd "$(git rev-parse --show-toplevel 2>/dev/null)"'

alias u='uv'
alias uvv='uv venv'
alias uvs='source .venv/bin/activate'
alias upy='uv run python'
alias upip='uv pip'
alias usync='uv sync'
alias ur='uv run'

alias gor='go run .'
alias gofmtw='gofmt -w'
alias got='go test ./...'
alias gob='go build ./...'
alias gom='go mod tidy'

alias vzsh='nvim ~/.zshrc ~/.zprofile'
alias vnvim='nvim ~/.config/nvim'
alias vatuin='nvim ~/.config/atuin/config.toml'
alias vboot='nvim "__HOME__/.zprofile" "__HOME__/.zshrc"'

alias yi='you-get -i'
alias yc='you-get -c'
alias yd='you-get'
alias ydl='you-get -l'

mkcd() {
  [ "$#" -eq 1 ] || { echo "usage: mkcd <dir>"; return 1; }
  mkdir -p "$1" && cd "$1"
}

take() {
  mkcd "$@"
}

ff() {
  local target="${1:-.}"
  _fd_cmd --type f . "$target" -HI 2>/dev/null | \
    fzf --height=80% --layout=reverse --border \
      --preview '_bat_cmd --color=always --style=plain --line-range=:200 {} 2>/dev/null || head -200 {}' \
      --preview-window='right,60%,wrap'
}

cdf() {
  local target="${1:-.}"
  local dir
  dir="$(_fd_cmd --type d . "$target" -HI 2>/dev/null | \
    fzf --height=80% --layout=reverse --border \
      --preview '_ls_cmd -a "{}" 2>/dev/null || true' \
      --preview-window='right,60%')" || return 1
  [ -n "$dir" ] && cd "$dir"
}

vf() {
  local file
  file="$(ff "${1:-.}")" || return 1
  [ -n "$file" ] && nvim "$file"
}

cf() {
  local file
  file="$(ff "${1:-.}")" || return 1
  [ -n "$file" ] && _bat_cmd --paging=always --style=plain "$file"
}

rgf() {
  local q="$1"
  [ -n "$q" ] || { echo "usage: rgf <pattern> [path]"; return 1; }
  rg --line-number --no-heading --smart-case "$q" "${2:-.}" | \
    fzf --delimiter : \
      --preview '_bat_cmd --color=always --style=plain --highlight-line {2} {1}' \
      --preview-window='right,70%,wrap'
}

cdfg() {
  local dir
  dir="$(_fd_cmd --type d . . -HI 2>/dev/null | rg -v '/(\.git|node_modules|dist|build|target)(/|$)' | \
    fzf --height=80% --layout=reverse --border)" || return 1
  [ -n "$dir" ] && cd "$dir"
}

jpp() {
  if [ "$#" -gt 0 ]; then
    jq . "$@"
  else
    jq .
  fi
}

jkeys() {
  if [ "$#" -gt 0 ]; then
    jq 'keys' "$@"
  else
    jq 'keys'
  fi
}

jget() {
  local expr="$1"
  shift
  jq -r "$expr" "$@"
}

ypp() {
  if [ "$#" -gt 0 ]; then
    yq '.' "$@"
  else
    yq '.'
  fi
}

yget() {
  local expr="$1"
  shift
  yq "$expr" "$@"
}

jsonf() {
  local file="$1"
  [ -n "$file" ] || { echo "usage: jsonf <file>"; return 1; }
  jq . "$file" | _bat_cmd --language json --paging=never --style=plain
}

yamlf() {
  local file="$1"
  [ -n "$file" ] || { echo "usage: yamlf <file>"; return 1; }
  yq '.' "$file" | _bat_cmd --language yaml --paging=never --style=plain
}

glogg() {
  git log --oneline --graph --decorate --all -n "${1:-30}"
}

gcleanmerged() {
  git branch --merged | rg -v '(^\*|main|master|dev|develop)' | xargs -n 1 git branch -d
}

gnew() {
  local name="$1"
  [ -n "$name" ] || { echo "usage: gnew <branch-name>"; return 1; }
  git switch -c "$name"
}

gfixup() {
  local hash="$1"
  [ -n "$hash" ] || { echo "usage: gfixup <commit>"; return 1; }
  git commit --fixup "$hash"
}

uvinit() {
  local pyver="${1:-3.12}"
  uv venv --python "$pyver" && source .venv/bin/activate
}

uvadd() {
  [ "$#" -gt 0 ] || { echo "usage: uvadd <package...>"; return 1; }
  uv add "$@"
}

uvdev() {
  [ "$#" -gt 0 ] || { echo "usage: uvdev <package...>"; return 1; }
  uv add --dev "$@"
}

uvxrun() {
  [ "$#" -gt 0 ] || { echo "usage: uvxrun <tool> [args...]"; return 1; }
  uvx "$@"
}

gorace() {
  go test -race ./...
}

gocov() {
  go test ./... -cover
}

nconf() {
  nvim ~/.config/nvim/lazyvim.json ~/.config/nvim/.neoconf.json
}

fkill() {
  local pid
  pid="$(ps -ef | sed 1d | fzf --height=80% --layout=reverse --border | awk '{print $2}')" || return 1
  [ -n "$pid" ] && kill -9 "$pid"
}

fport() {
  lsof -nP -iTCP -sTCP:LISTEN | sed 1d | fzf --height=80% --layout=reverse --border
}
'''
        finder_cmd = "open ." if self.system == "darwin" else "xdg-open ."
        content = (
            template
            .replace("__ZSH_PROXY_FILE__", str(self.zsh_proxy_file))
            .replace("__OMP_THEME_FILE__", str(self.omp_theme_file))
            .replace("__ZINIT_HOME__", str(self.zinit_home))
            .replace("__CACHE_ZSH_DIR__", str(self.cache_home / "zsh"))
            .replace("__HOME__", str(self.home))
            .replace("__FINDER_CMD__", finder_cmd)
        )
        self.write_file_if_changed(self.home / ".zshrc", content, 0o644)

    def write_ghostty_files(self):
        if self.install_ghostty != "1":
            return

        if self.dry_run:
            self.dry("would ensure Ghostty config under {0}".format(self.ghostty_dir))

        if not self.dry_run:
            self.ghostty_dir.mkdir(parents=True, exist_ok=True)

        content = """# Managed by setup.py
font-size = 16
background = #181818
foreground = #d8d8d8
window-padding-x = 15
window-padding-y = 15
shell-integration = detect
"""
        self.write_file_if_changed(self.ghostty_config_file, content, 0o644)

    def write_hammerspoon_config(self):
        if self.system != "darwin":
            return
        if self.install_hammerspoon != "1" or self.ghostty_hotkey_enabled != "1":
            return

        mods = [m.strip() for m in self.ghostty_hotkey_mods.split(",") if m.strip()]
        mods_lua = "{" + ", ".join(['"{0}"'.format(m) for m in mods]) + "}"
        key = self.ghostty_hotkey_key

        managed_content = """-- Managed by setup.py

local ghostty_path = "/Applications/Ghostty.app"
local mods = {mods}
local key = "{key}"

if hs.hotkey.systemAssigned(mods, key) then
  hs.alert.show("Ghostty hotkey is already used by macOS")
else
  hs.hotkey.bind(mods, key, function()
    hs.application.launchOrFocus(ghostty_path)
  end)
end
""".format(mods=mods_lua, key=key)

        self.write_file_if_changed(self.hammerspoon_managed_file, managed_content, 0o644)

        start_marker = "-- bootstrap-managed:start"
        end_marker = "-- bootstrap-managed:end"
        managed_path = str(self.hammerspoon_managed_file).replace("\\", "\\\\").replace('"', '\\"')
        block = """{start_marker}
local bootstrap_managed_ok, bootstrap_managed_err = pcall(function()
  dofile("{managed_path}")
end)
if not bootstrap_managed_ok then
  hs.alert.show("bootstrap-managed.lua failed to load")
  print(bootstrap_managed_err)
end
{end_marker}
""".format(
            start_marker=start_marker,
            managed_path=managed_path,
            end_marker=end_marker,
        )

        current = ""
        if self.hammerspoon_init_file.exists() or self.hammerspoon_init_file.is_symlink():
            try:
                current = self.hammerspoon_init_file.read_text(encoding="utf-8")
            except Exception:
                current = ""

        if start_marker in current and end_marker in current:
            before, _, rest = current.partition(start_marker)
            _, _, after = rest.partition(end_marker)
            if after.startswith("\n"):
                after = after[1:]
            init_content = before.rstrip() + "\n\n" + block.rstrip()
            if after.strip():
                init_content += "\n\n" + after.lstrip()
            else:
                init_content += "\n"
        elif current.strip():
            init_content = current.rstrip() + "\n\n" + block
        else:
            init_content = block

        self.write_file_if_changed(self.hammerspoon_init_file, init_content, 0o644)

    def apply_git_config(self):
        log("[git] applying global git config")
        key = "url.ssh://git@ssh.github.com:443/.insteadOf"
        cmd = [
            "git",
            "config",
            "--global",
            key,
            'git@github.com:',
        ]
        if self.dry_run:
            self.dry("would run: {0}".format(" ".join(cmd)))
            return
        self.record_git_config_backup(key)
        run(cmd, env=self.env)
        info("git github ssh-over-443 mapping applied")

    # ---------- health check ----------

    def shell_command_exists(self, cmd):
        if self.dry_run:
            return True
        result = run(
            ["zsh", "-lic", "command -v {0}".format(cmd)],
            check=False,
            capture=True,
            env=self.env,
        )
        return result.returncode == 0

    def shell_any_command_exists(self, cmds):
        for cmd in cmds:
            if self.shell_command_exists(cmd):
                return True
        return False

    def health_check(self):
        log("[8/8] health check")

        if self.dry_run:
            self.dry("would validate a real zsh login shell after changes")
            return

        hard_failures = []

        checks = [
            ("zsh", ["zsh"]),
            ("git", ["git"]),
            ("curl", ["curl"]),
            ("jq", ["jq"]),
            ("ripgrep", ["rg"]),
            ("fd", ["fd", "fdfind"]),
            ("fzf", ["fzf"]),
            ("tmux", ["tmux"]),
            ("neovim", ["nvim"]),
            ("python3", [Path(self.python_exe).name, "python3"]),
        ]

        for label, cmds in checks:
            if self.shell_any_command_exists(cmds):
                info("found {0} in real zsh shell".format(label))
            else:
                hard_failures.append(label)
                err("missing in real zsh shell: {0}".format(label))

        soft_checks = [
            ("bat", ["bat", "batcat"]),
            ("eza", ["eza"]),
            ("zoxide", ["zoxide"]),
            ("go", ["go"]),
            ("node", ["node"]),
            ("uv", ["uv"]),
            ("atuin", ["atuin"]),
            ("lazygit", ["lazygit"]),
            ("code", ["code"]),
        ]

        for label, cmds in soft_checks:
            if self.shell_any_command_exists(cmds):
                info("found {0} in real zsh shell".format(label))
            else:
                warn("missing in real zsh shell: {0}".format(label))
                self.soft_failures.append("missing in real zsh shell: {0}".format(label))

        if self.module_enabled("shell"):
            if not (self.home / ".zprofile").exists():
                hard_failures.append(".zprofile")
                err("missing ~/.zprofile")
            else:
                info("managed ~/.zprofile exists")

            if not (self.home / ".zshrc").exists():
                hard_failures.append(".zshrc")
                err("missing ~/.zshrc")
            else:
                info("managed ~/.zshrc exists")

        if self.module_enabled("hotkey") and self.system == "darwin" and self.ghostty_hotkey_enabled == "1":
            if not Path("/Applications/Hammerspoon.app").is_dir():
                warn("Hammerspoon missing for Ghostty hotkey")
                self.soft_failures.append("Hammerspoon missing for Ghostty hotkey")

        if hard_failures:
            raise RuntimeError("hard failures: {0}".format(", ".join(hard_failures)))

        if self.soft_failures:
            warn("non-fatal issues:")
            for item in self.soft_failures:
                warn("  - {0}".format(item))

    def cleanup(self):
        shutil.rmtree(str(self.tx_dir), ignore_errors=True)

    def main(self):
        log("start bootstrap")
        log("========================================")
        log("system: {0}".format(self.system))
        if self.system == "linux":
            log("distro: {0}".format(self.distro_id or "unknown"))
        log("package manager: {0}".format(self.pkg_manager))
        log("only: {0}".format(self.only))
        if self.dry_run:
            log("mode: dry-run")

        if self.system == "darwin" and (self.module_enabled("packages") or self.module_enabled("hotkey")):
            self.ensure_xcode_clt()
            self.ensure_brew()

        if self.module_enabled("packages"):
            self.install_core_packages()
            self.install_optional_system_packages()
            self.install_python_tools()

        if self.module_enabled("shell"):
            self.ensure_zinit()
            self.write_proxy_file()
            self.write_atuin_config()
            self.write_omp_theme()
            self.write_zprofile()
            self.write_zshrc()
            self.write_ghostty_files()

        if self.module_enabled("hotkey"):
            self.install_hotkey_dependencies()
            self.write_hammerspoon_config()

        if self.module_enabled("nvim"):
            self.ensure_lazyvim()

        if self.only == "all":
            self.health_check()
        elif self.dry_run:
            self.dry("would skip full health check because --only is not all")
        else:
            info("skipped full health check because --only is not all")

        if self.module_enabled("git"):
            self.apply_git_config()

        log("----------------------------------------")
        if self.dry_run:
            log("dry-run finished")
            log("next:")
            log("  1. review the plan above")
            log("  2. run: python3 setup.py")
        else:
            log("bootstrap finished")
            log("next:")
            log("  1. exec zsh -l")
            log("  2. echo $PATH")
            log("  3. code --version")
            log("  4. nvim")
            if self.system == "darwin" and self.ghostty_hotkey_enabled == "1":
                log("  5. open Hammerspoon once, grant Accessibility, then reload config")
            else:
                log("  5. press Ctrl-R for Atuin")


def parse_args():
    parser = argparse.ArgumentParser(description="Bootstrap Linux/macOS dev environment")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what would change without changing the system",
    )
    parser.add_argument(
        "--only",
        choices=["all", "packages", "shell", "nvim", "hotkey", "git"],
        default="all",
        help="run only one module",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    bs = Bootstrap(dry_run=args.dry_run, only=args.only)
    try:
        bs.main()
    except Exception as ex:
        err(str(ex))
        warn("rolling back config changes")
        bs.rollback_paths()
        bs.cleanup()
        raise SystemExit(1)
    else:
        bs.cleanup()


if __name__ == "__main__":
    main()
