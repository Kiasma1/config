# Python Bootstrap

一个用 **Python 标准库** 写的个人开发环境开荒脚本。  
目标不是锁死版本做“完全复现”，而是把一台 Linux / macOS 机器**快速收敛到一个统一、顺手、可重复执行的开发环境**。

---

## Why

这份脚本解决的是这些问题：

- 新机器开荒很麻烦
- 老机器配置越来越乱
- shell / nvim / alacritty / 常用 CLI 工具不统一
- 想反复执行 setup，但不想每次都手工排错
- 想用 Python 而不是越来越难维护的 bash 大脚本

---

## What it does

- 安装核心开发工具
- 完全接管 `~/.zprofile` 和 `~/.zshrc`
- 刷新 `nvim` / `LazyVim`
- 配好 `Atuin` / `fzf` / `zoxide` / `oh-my-posh`
- 配好 Alacritty
- 支持通过 **Hammerspoon** 给 Alacritty 加全局快捷键
- 自动写入 GitHub SSH over 443 的全局 git config
- 支持 `--dry-run`
- 支持 `--only`

---

## Platforms

### Linux

支持这些包管理器：

- `apt`
- `dnf`
- `yum`
- `pacman`
- `zypper`
- `apk`

### macOS

支持：

- `Homebrew`

---

## Quick start

### 先预演

```bash
python3 setup.py --dry-run
```

### 正式执行

```bash
python3 setup.py
```

### 完成后

```bash
exec zsh -l
code --version
nvim
```

---

## Modules

你可以整套跑，也可以只跑一部分：

```bash
python3 setup.py --only packages
python3 setup.py --only shell
python3 setup.py --only nvim
python3 setup.py --only hotkey
python3 setup.py --only git
```

---

## Alacritty global hotkey

在 macOS 上，脚本可以通过 **Hammerspoon** 给 Alacritty 配一个全局快捷键。

默认热键：

```text
ctrl + alt + return
```

作用：

- Alacritty 没开：启动
- Alacritty 已开：聚焦

---

## GitHub SSH over 443

脚本会自动写入这条全局 Git 配置：

```bash
git config --global url."ssh://git@ssh.github.com:443/".insteadOf "git@github.com:"
```

适合网络环境下 GitHub SSH 直连不稳定的情况。

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

## Common aliases

### before -> after

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

## Features you may care about

- 用系统自带 `python3` 就能跑
- 不依赖第三方 Python 库
- Linux 包名差异做了兼容
- `fd / fdfind`、`bat / batcat` 已兼容
- `health check` 会检查真实 zsh shell，不只检查 Python 自己的 PATH
- 旧配置会自动备份到：

```text
~/.bootstrap-backups/<timestamp>/
```

---

## Philosophy

这不是一个“锁版本、完全可复现”的环境管理系统。  
它更像：

> 一份可以重复执行、能逐步收敛、适合个人长期维护的 setup script

重点不是“完美复刻历史环境”，而是：

- 环境统一
- 反复执行安全
- 机器尽快可用
- 后续容易维护

---

## Docs

更详细的说明见：

- `README.zh-CN.md`
- `README.en.md`
