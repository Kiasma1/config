# Python Bootstrap

一个用 **Python 标准库** 写的个人开发环境开荒脚本。

它的定位不是“严格锁版本、完全可复现”，而是：

- 可重复执行
- 收敛到当前最新可用状态
- 完全接管个人配置
- Linux / macOS 都能跑
- Linux 可以直接用系统自带的 `python3`
- 不依赖第三方 Python 库

---

## 这份脚本适合什么场景

适合你这种需求：

- 新机器开荒
- 老机器重新统一环境
- 想把 shell / nvim / alacritty / 常用 CLI 工具快速拉齐
- 不想维护 bash 大脚本
- 希望用 Python 标准库做一个更容易维护的 setup

它**不追求**：

- 精确复现某个历史环境
- 锁死每一个版本
- GUI App 一定要由同一个包管理器严格接管

它**追求**：

- 重复执行安全
- 配置统一
- 尽量自动修正环境
- 出问题后容易恢复

---

## 支持平台

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

## Python 要求

只使用 Python 标准库。

最低要求：

```text
Python 3.6+
```

推荐运行方式：

```bash
python3 setup.py
```

如果你的 `python` 本身就是 Python 3，也可以：

```bash
python setup.py
```

---

## 这版脚本已经修好的关键问题

### 1. `~/.zshrc` 现在会先加载 `~/.zprofile`

这解决了之前那种情况：

- alias 生效了
- 但 `brew` / `nvim` 不在 PATH 里

现在脚本生成的 `~/.zshrc` 会先 source `~/.zprofile`，所以非 login zsh 也更稳。

### 2. health check 现在会检查真实 zsh shell

不再只是检查 Python 自己临时构造的 PATH。  
现在会用真实的：

```bash
zsh -lic 'command -v ...'
```

去验证像 `brew`、`nvim`、`code` 这类命令是否真的能在新 shell 里工作。

### 3. 支持 `--dry-run`

你可以先预演，不真的改系统：

```bash
python3 setup.py --dry-run
```

---

## dry-run 是什么

`dry-run` = **只预演，不动手**

比如：

```bash
python3 setup.py --dry-run
```

它会告诉你：

- 准备安装哪些包
- 准备覆盖哪些配置文件
- 准备克隆哪些仓库
- 准备写哪些内容

但**不会真正修改系统**。

这个模式非常适合：

- 先检查是否会覆盖你不想动的文件
- 看 Linux / macOS 上会走哪些分支
- 看包名映射是否符合预期

---

## 快速开始

### 1. 先预演

```bash
python3 setup.py --dry-run
```

### 2. 正式执行

```bash
python3 setup.py
```

### 3. 执行完成后

```bash
exec zsh -l
brew --version
code --version
nvim --version
```

Linux 上如果没有 `brew`，就跳过那条，重点看：

```bash
exec zsh -l
command -v nvim
command -v uv
command -v atuin
```

---

## 脚本会做什么

### 1. 安装核心工具

尽量通过系统包管理器安装：

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

### 2. 安装一批可选工具

尽量通过系统包管理器安装：

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

### 3. 用 pip 安装用户级工具

尽量通过：

```bash
python3 -m pip install --user --upgrade ...
```

安装：

- `pipx`
- `uv`
- `yq`
- `you-get`

### 4. 刷新并接管配置

会接管这些内容：

```text
~/.zprofile
~/.zshrc
~/.config/nvim
~/.config/atuin/config.toml
~/.config/alacritty/alacritty.toml
```

### 5. 克隆和刷新仓库

会刷新：

- `zinit`
- `LazyVim starter`

---

## 自动备份

旧配置在覆盖前会备份到：

```text
~/.bootstrap-backups/<timestamp>/
```

所以这不是“无脑覆盖”，而是：

- 先备份
- 再写入新内容

---

## Linux 包名差异说明

不同发行版里，同一个工具的包名可能不同。

例如：

- `fd`
  - Debian / Ubuntu 常见包名：`fd-find`
  - Arch 常见包名：`fd`

- `go`
  - Debian / Ubuntu：`golang-go`
  - Fedora / RHEL：`golang`
  - Arch：`go`

- `python3-pip`
  - Alpine：`py3-pip`

脚本内部已经做了一层包名映射，会优先根据：

1. Linux 发行版 ID
2. 包管理器类型
3. 默认映射

来选择更合理的包名。

---

## 常用环境变量

### 启用代理

```bash
BOOTSTRAP_ENABLE_PROXY=1 python3 setup.py
```

自定义代理：

```bash
BOOTSTRAP_ENABLE_PROXY=1 \
BOOTSTRAP_HTTP_PROXY=http://127.0.0.1:7897 \
BOOTSTRAP_ALL_PROXY=socks5://127.0.0.1:7897 \
python3 setup.py
```

### 不装 Alacritty

```bash
BOOTSTRAP_INSTALL_ALACRITTY=0 python3 setup.py
```

### 不装 VS Code

```bash
BOOTSTRAP_INSTALL_VSCODE=0 python3 setup.py
```

### 不装 Rectangle

```bash
BOOTSTRAP_INSTALL_RECTANGLE=0 python3 setup.py
```

### 不装 Stats

```bash
BOOTSTRAP_INSTALL_STATS=0 python3 setup.py
```

---

## 默认 shell 能力

### history / 搜索

- `Ctrl-R`：Atuin 历史搜索
- `hh`：Atuin search
- `hhi`：Atuin interactive search
- `hs`：Atuin stats

### 文件 / 搜索

- `ff`：`fd + fzf` 选文件
- `vf`：选文件后直接 `nvim`
- `cf`：选文件后直接预览
- `cdf`：交互式切目录
- `rgf keyword`：`rg + fzf` 查看搜索结果

### JSON / YAML

- `jpp`
- `jkeys`
- `jget`
- `ypp`
- `yget`
- `jsonf`
- `yamlf`

### Git

- `gs`
- `glogg`
- `gnew`
- `gfixup`
- `gcleanmerged`
- `lg`

### uv

- `uvinit`
- `uvadd`
- `uvdev`
- `uvxrun`

### Go

- `gor`
- `got`
- `gob`
- `gom`
- `gorace`
- `gocov`

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

## 目录说明

### shell

```text
~/.zprofile
~/.zshrc
```

### bootstrap 管理目录

```text
~/.config/bootstrap-managed/
```

### Atuin 配置

```text
~/.config/atuin/config.toml
```

### Alacritty 配置

```text
~/.config/alacritty/alacritty.toml
~/.config/alacritty/bootstrap-managed.toml
~/.config/alacritty/bootstrap-colors.toml
```

### Neovim 配置

```text
~/.config/nvim
```

### 备份目录

```text
~/.bootstrap-backups/<timestamp>/
```

---

## 常见问题

### 1. `brew` 找不到

先执行：

```bash
exec zsh -l
```

再试：

```bash
command -v brew
brew --version
```

如果 macOS 上还是找不到，重点检查：

```bash
sed -n '1,80p' ~/.zprofile
sed -n '1,120p' ~/.zshrc
```

### 2. `vim` 变成 `nvim`，但 `nvim` 找不到

这说明：

- `.zshrc` 已经生效
- 但 `nvim` 没装好，或者 PATH 还不对

先检查：

```bash
command -v nvim
```

### 3. Linux 上 `fd` 命令名不一样

有些系统命令名是：

```bash
fdfind
```

脚本里已经兼容了：

- `fd`
- `fdfind`

所以平时直接用：

```bash
ff
cdf
vf
```

就行。

### 4. Linux 上 `bat` 命令名不一样

有些系统命令名是：

```bash
batcat
```

脚本也已经兼容了。

### 5. 脚本会不会保留我的旧配置

不会直接沿用。  
这版是**完全接管**，不是局部插入 managed block。

但旧文件会先备份到：

```text
~/.bootstrap-backups/<timestamp>/
```

---

## 推荐验证命令

```bash
command -v zsh
command -v git
command -v jq
command -v rg
command -v fzf
command -v nvim
command -v code
command -v uv
command -v atuin
```

再试：

```bash
ff
vf
cdf
hh
nvim
```

---

## 一句话总结

这份脚本适合这样用：

> 用系统自带 Python 直接跑，  
> 把 Linux / macOS 机器快速拉到一个统一、顺手、可重复执行的个人开发环境。
