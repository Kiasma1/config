# Python Bootstrap

一个只用 **Python 标准库** 写的 **macOS + Linux** 开荒脚本。

它适合：

- 个人机器重复开荒
- 把环境收敛到“当前最新可用状态”
- 完全接管 shell / nvim / alacritty 配置
- Linux 直接用系统自带 `python3` 运行

它**不是**一个严格锁版本、完全可复现的环境系统。

---

## 这版新增 / 修复了什么

- 支持 `--dry-run`
- 支持 `--only packages|shell|nvim|hotkey|git`
- 用真实 `zsh -lic` 做 health check
- `~/.zshrc` 现在会先加载 `~/.zprofile`
- 自动写入 GitHub SSH over 443 的全局 git 配置
- 支持 macOS 上的 Hammerspoon + Alacritty 全局快捷键
- 补了常见 Linux 发行版的包名差异映射
- 覆盖配置前自动备份

---

## 支持的包管理器

Linux：

- `apt`
- `dnf`
- `yum`
- `pacman`
- `zypper`
- `apk`

macOS：

- `Homebrew`

---

## 快速开始

### 先预演

```bash
python3 setup.py --dry-run
```

### 正式执行

```bash
python3 setup.py
```

### 重新加载 shell

```bash
exec zsh -l
```

---

## 只跑某个模块

```bash
python3 setup.py --only packages
python3 setup.py --only shell
python3 setup.py --only nvim
python3 setup.py --only hotkey
python3 setup.py --only git
```

---

## 会安装什么

### 核心工具

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

### 可选工具

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
- macOS 可选 App：`Visual Studio Code`、`Rectangle`、`Stats`、`Hammerspoon`

### Python 用户级工具

只通过 Python 用户目录安装：

- `pipx`
- `uv`

`yq` 和 `you-get` 这版已经**不再双重安装**。

---

## 接管哪些配置

脚本会直接接管：

```text
~/.zprofile
~/.zshrc
~/.config/nvim
~/.config/atuin/config.toml
~/.config/alacritty/alacritty.toml
```

旧配置会备份到：

```text
~/.bootstrap-backups/<timestamp>/
```

---

## macOS 上的 Alacritty 全局快捷键

如果启用，脚本会写入 `~/.hammerspoon/init.lua`，默认热键为：

```text
Ctrl + Alt + Enter
```

行为：

- Alacritty 没开：启动
- Alacritty 已开：切到前台

执行完成后：

```bash
open -a Hammerspoon
```

然后：

- 允许 Accessibility 权限
- 在 Hammerspoon 菜单里 Reload Config

---

## 自动写入的 Git 配置

脚本会写入：

```bash
git config --global url."ssh://git@ssh.github.com:443/".insteadOf "git@github.com:"
```

作用是把 GitHub SSH 尽量走 443 端口。

---

## 最值得先记住的一批命令

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

## 常用 alias（前 -> 后）

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

## 这版修掉的几个关键问题

- `dry-run` 不再偷偷创建 Alacritty 目录
- health check 现在兼容 `fd / fdfind`、`bat / batcat`
- `--only hotkey` 不再顺手重写整套 shell 配置
- `yq / you-get` 不再走系统包 + pip 双重安装

