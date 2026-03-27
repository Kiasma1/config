# Python Bootstrap

A standard-library-only bootstrap script for **macOS + Linux**.

It is designed for:

- repeatable personal machine setup
- converging to a usable latest-state environment
- fully taking over your shell / nvim / alacritty config
- running with built-in `python3` on Linux

It is **not** trying to be a fully locked, reproducible environment system.

---

## What this version includes

- `--dry-run`
- `--only packages|shell|nvim|hotkey|git`
- real shell health checks via `zsh -lic`
- `~/.zshrc` now sources `~/.zprofile` first
- GitHub SSH-over-443 global git config
- Hammerspoon + Alacritty global hotkey on macOS
- Linux package-name mapping for common distro differences
- backups before overwriting config

---

## Supported package managers

Linux:

- `apt`
- `dnf`
- `yum`
- `pacman`
- `zypper`
- `apk`

macOS:

- `Homebrew`

---

## Quick start

### Preview first

```bash
python3 setup.py --dry-run
```

### Apply for real

```bash
python3 setup.py
```

### Reload shell

```bash
exec zsh -l
```

---

## Useful module-only runs

```bash
python3 setup.py --only packages
python3 setup.py --only shell
python3 setup.py --only nvim
python3 setup.py --only hotkey
python3 setup.py --only git
```

---

## What it installs

### Core

- `zsh`
- `git`
- `curl`
- `wget`
- `jq`
- `ripgrep`
- `fd` / `fdfind`
- `fzf`
- `tmux`
- `neovim`
- `htop`

### Optional

- `node`
- `go`
- `bat`
- `eza`
- `zoxide`
- `lazygit`
- `atuin`
- `oh-my-posh`
- `alacritty`
- `yq`
- `you-get`
- macOS optional apps: `Visual Studio Code`, `Rectangle`, `Stats`, `Hammerspoon`

### Python user tools

Only these are installed via Python user site:

- `pipx`
- `uv`

`yq` and `you-get` are intentionally **not** installed twice anymore.

---

## Config takeover

This script fully manages:

```text
~/.zprofile
~/.zshrc
~/.config/nvim
~/.config/atuin/config.toml
~/.config/alacritty/alacritty.toml
```

Backups are saved to:

```text
~/.bootstrap-backups/<timestamp>/
```

---

## Alacritty global hotkey on macOS

If enabled, setup writes `~/.hammerspoon/init.lua` and binds:

```text
Ctrl + Alt + Enter
```

Behavior:

- launch Alacritty if not running
- focus Alacritty if already running

After setup:

```bash
open -a Hammerspoon
```

Then:

- grant Accessibility permission
- reload config from the Hammerspoon menu

---

## Git config added

The script writes this global Git config:

```bash
git config --global url."ssh://git@ssh.github.com:443/".insteadOf "git@github.com:"
```

This helps force GitHub SSH traffic over port 443.

---

## Most worth remembering

```bash
ff
vf
cdf
rgf keyword

gs
glogg
gnew feature/xxx
lg

uvinit
uvadd xxx
uvdev pytest

gor
got
gom

hh
hhi
```

---

## Common aliases (before -> after)

```text
vim      -> nvim
vi       -> nvim
ls       -> eza
la       -> eza -a --git --color-scale
ll       -> eza -lbGF --git
lt       -> eza --tree --level=2
cat      -> bat --paging=never --style=plain
top      -> htop
j        -> jq
y        -> yq
hh       -> atuin search
hhi      -> atuin search --interactive
u        -> uv
gor      -> go run .
got      -> go test ./...
gom      -> go mod tidy
gs       -> git status -sb
lg       -> lazygit
rz       -> exec zsh -l
```

---

## Notes

- `dry-run` no longer creates the Alacritty config directory.
- health checks now account for distro command differences such as `fd` vs `fdfind`, and `bat` vs `batcat`.
- `--only hotkey` is now scoped to hotkey-related work instead of rewriting all shell config.
