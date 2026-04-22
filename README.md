# Python Bootstrap

一个用 **Python 标准库** 写的个人开发环境开荒脚本。

它的目标不是“锁死版本、完全复现”，而是：

- 可以重复执行
- 把一台 Linux / macOS 机器快速收敛到一个统一、顺手、可维护的开发环境
- 完全接管你自己的 shell / helix / ghostty 配置
- Linux 上可以直接用系统自带的 `python3` 来运行
- 不依赖第三方 Python 库

## 阅读地图

如果你现在的目标很明确，可以直接跳到对应位置：

| 你现在想做什么 | 先看这里 | 你大概率会用到 |
|---|---|---|
| 我只想先试跑，不想马上改系统 | [快速开始](#快速开始) | `python3 setup.py --dry-run` |
| 我想知道它到底会改什么 | [它会做什么](#它会做什么) | 安装项、接管配置、备份路径 |
| 我只想改某一部分 | [运行模式](#运行模式) | `python3 setup.py --only shell` |
| 我想知道每个工具最常怎么用 | [CLI 工具速查](#cli-工具速查) | `rg` / `fd` / `hx` / `tmux` |
| 我想学会最有用的命令 | [最值得先记住的一批命令](#最值得先记住的一批命令) | `ff` / `vf` / `cdf` / `rgf` |
| 我只想查 alias | [常用 alias 说明](#常用-alias-说明) | `gs` / `tmc` / `uvinit` |
| 我已经跑过 setup，现在想排错 | [常见问题](#常见问题) | `brew` / `hx` / `fd` / `bat` |

### 目录

1. [这是什么](#这是什么)
2. [适用平台](#适用平台)
3. [快速开始](#快速开始)
4. [它会做什么](#它会做什么)
5. [运行模式](#运行模式)
6. [CLI 工具速查](#cli-工具速查)
7. [先理解这几个基础工具](#先理解这几个基础工具)
8. [最值得先记住的一批命令](#最值得先记住的一批命令)
9. [常用 alias 说明](#常用-alias-说明)
10. [新手建议：先这样学](#新手建议先这样学)
11. [常见问题](#常见问题)
12. [一句话总结](#一句话总结)

---

## 这是什么

你可以把它理解成：

> 一份长期维护的个人机器初始化脚本

它主要解决这些问题：

- 新机器开荒很麻烦
- 老机器越用越乱
- shell、helix、终端、常用 CLI 工具不统一
- 想反复执行 setup，但不想每次都手工修环境
- 不想继续维护越来越难看的 bash 大脚本

### 它更适合什么人

- 想把新机器快速整理成统一环境的人
- 接受“脚本直接接管我的 shell / helix 配置”的人
- 希望以后继续反复执行同一份 setup 的人

### 它不太适合什么人

- 只想零散装几个软件、不想接管配置的人
- 非常在意“系统必须完全不被脚本改动”的人
- 想做通用团队级、强约束、可审计企业镜像的人

---

## 适用平台

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

## 快速开始

### 第一次使用，推荐这样读

- **只想先跑起来**：看「先预演」「正式执行」「执行完成后」
- **担心它会改太多**：先看「它会做什么」和「运行模式」
- **想知道命令怎么用**：后面再看「基础工具」「最值得先记住的一批命令」「常用 alias」

### 常用操作速查

| 场景 | 命令 |
|---|---|
| 先预演，不改系统 | `python3 setup.py --dry-run` |
| 全量执行 | `python3 setup.py` |
| 只装软件 | `python3 setup.py --only packages` |
| 只更新 shell 环境 | `python3 setup.py --only shell` |
| 只更新 Helix | `python3 setup.py --only helix` |
| 执行后重新进入 login shell | `exec zsh -l` |

### 先预演（不真正修改系统）

```bash
python3 setup.py --dry-run
```

### 正式执行

```bash
python3 setup.py
```

### 执行完成后

```bash
exec zsh -l
code --version
hx
```

---

## 它会做什么

你可以把这部分理解成：

> 这份脚本默认会安装什么、覆盖什么、顺手帮你配什么

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
- `helix`
- `htop`
- `node`
- `go`
- `bat`
- `eza`
- `zoxide`
- `atuin`
- `starship`
- `yq`
- `you-get`
- `tlrc`（实际命令名是 `tldr`）

### 2. 安装 Python 用户级工具

通过：

```bash
python3 -m pip install --user --upgrade ...
```

安装：

- `uv`

### 3. macOS 附加应用

默认会按开关安装这些应用：

- `ghostty`
- `Visual Studio Code`
- `Rectangle`
- `Hammerspoon`

默认关闭：

- `Stats`

### 4. 完全接管这些配置

```text
~/.zprofile
~/.zshrc
~/.config/helix/config.toml
~/.config/atuin/config.toml
~/.config/ghostty/config
```

### 5. 自动备份旧配置

旧文件会先备份到：

```text
~/.bootstrap-backups/<timestamp>/
```

### 6. 刷新这些仓库配置

- `zinit`

`starship` 提示符配置文件放在仓库里：

```text
assets/starship/starship.toml
```

### 7. 配置 Ghostty 全局快捷键（macOS）

通过 **Hammerspoon** 给 Ghostty 配置全局快捷键。

默认热键：

```text
ctrl + alt + return
```

作用：

- Ghostty 没开：启动
- Ghostty 已开：切到前台

### 8. 配置 GitHub SSH over 443

自动写入：

```bash
git config --global url."ssh://git@ssh.github.com:443/".insteadOf "git@github.com:"
```

适合 GitHub SSH 直连不稳定的场景。

---

## 运行模式

大多数情况下，你只会用下面两种方式：

- **整套执行**：新机器、重装后、想整体收敛环境时
- **按模块执行**：只想改某一部分配置时

### 整套运行

```bash
python3 setup.py
```

### 只运行某一部分

```bash
python3 setup.py --only packages
python3 setup.py --only shell
python3 setup.py --only helix
python3 setup.py --only hotkey
python3 setup.py --only git
```

### `--only` 分别是什么意思

如果你只想记住最常用的三个：

- `--only packages`：装软件
- `--only shell`：改 shell / 终端环境
- `--only helix`：改 Helix

#### `--only packages`
只处理安装包相关的事情：

- 核心包
- macOS 附加应用
- Python 用户级工具

#### `--only shell`
只处理 shell 和终端环境：

- `~/.zprofile`
- `~/.zshrc`
- `zinit`
- `Atuin`
- `starship`
- Ghostty 配置

> 注意：`--only shell` **不会安装** `starship`、`helix`、`tlrc/tldr` 这些程序本体。  
> 它只会写配置和 alias。新机器如果还没装过这些工具，请先跑：
>
> ```bash
> python3 setup.py --only packages
> ```
>
> 或直接跑全量：
>
> ```bash
> python3 setup.py
> ```

#### `--only helix`
只处理 Helix 配置。

> 注意：`--only helix` **不会安装** `hx/helix` 可执行文件，只会写 `~/.config/helix/config.toml`。

默认会写入一份 Helix 配置，包含插入模式下：

```text
jj -> <Esc>
```

#### `--only hotkey`
只处理 Ghostty 全局快捷键相关内容：

- Hammerspoon 配置
- 热键配置写入

#### `--only git`
只处理 git 全局配置。

---

## CLI 工具速查

如果你只想知道：

> 这些工具各自最常用的一条命令是什么、它们大概是干什么的

直接看这张表就够了。

| 工具 | 最推荐命令 | 这工具是干什么的 |
|---|---|---|
| `zsh` | `exec zsh -l` | 重新进入 shell，加载最新配置 |
| `git` | `git status -sb` | 看当前仓库状态和分支 |
| `curl` | `curl https://example.com` | 发 HTTP 请求，常用来测接口 |
| `wget` | `wget https://example.com/file.zip` | 直接下载文件 |
| `jq` | `jq . package.json` | 查看和处理 JSON |
| `rg` | `rg "TODO"` | 全项目快速搜文本 |
| `fd` | `fd config` | 快速找文件和目录 |
| `fzf` | `history \| fzf` | 从大量候选里模糊筛选 |
| `tmux` | `tmux new -s work` | 创建可复用的终端会话 |
| `hx` | `hx README.md` | 打开文件编辑；你现在的主编辑器 |
| `htop` | `htop` | 查看进程和资源占用 |
| `node` | `node -v` | Node.js 运行时入口 |
| `go` | `go test ./...` | 跑整个 Go 项目的测试 |
| `bat` | `bat README.md` | 更好看的文件查看器 |
| `eza` | `eza -la` | 更好看的目录列表 |
| `zoxide` | `z project` | 快速跳转常用目录 |
| `atuin` | `atuin search` | 搜索历史命令 |
| `starship` | `starship explain` | 查看 prompt 是怎么生成的 |
| `yq` | `yq . config.yaml` | 查看和处理 YAML |
| `you-get` | `you-get -i <URL>` | 查看媒体链接可下载信息 |
| `tldr` | `tldr git-commit` | 看命令的简明示例，而不是长 man page |
| `cmdh` | `cmdh git commit` | 统一命令帮助入口：先看 tldr，再退到 `--help` / `man` |
| `uv` | `uv run python main.py` | 更现代地运行 Python 项目或脚本 |

### 如果你只想先记住 8 个

1. `rg "关键词"`
2. `fd 文件名`
3. `hx 文件名`
4. `git status -sb`
5. `tmux new -s work`
6. `z 项目名`
7. `jq . file.json`
8. `atuin search`

---

## 先理解这几个基础工具

后面很多命令都建立在这 5 个工具上：

| 工具 | 一句话理解 | 最常见用途 |
|---|---|---|
| `fzf` | 终端里的模糊选择器 | 从一堆结果里选一个 |
| `fd` | 更顺手的 `find` | 找文件、找目录 |
| `rg` | 更适合代码搜索的 `grep` | 搜关键字、搜函数、搜配置 |
| `atuin` | 强化版命令历史 | 把以前跑过的命令找回来 |
| `uv` | 现代 Python 工具链 | 建虚拟环境、装依赖、跑脚本 |

如果你只想快速上手：

- 学命令：看「最值得先记住的一批命令」
- 查缩写：看「常用 alias 说明」
- 排错：看「常见问题」

---

## 最值得先记住的一批命令

这部分只保留最常用、最值得先学的命令。

### 文件 / 目录 / 搜索

| 命令 | 最常见写法 | 用来干什么 |
|---|---|---|
| `ff` | `ff` / `ff src` | 交互式找文件并预览 |
| `vf` | `vf` / `vf .` | 交互式选文件后直接用 Helix 打开 |
| `cdf` | `cdf` / `cdf ~/WKSpace` | 交互式选目录并切进去 |
| `rgf` | `rgf TODO` | 搜关键字，再从结果里挑一个继续看 |

### Git

| 命令 | 最常见写法 | 用来干什么 |
|---|---|---|
| `gs` | `gs` | 看当前仓库状态 |
| `glogg` | `glogg` / `glogg 50` | 图形化看提交历史 |
| `gnew` | `gnew feature/login` | 新建并切到一个分支 |

### 历史命令

| 命令 | 最常见写法 | 用来干什么 |
|---|---|---|
| `hh` | `hh` | 搜以前跑过的命令 |
| `hhi` | `hhi` | 交互式翻历史命令 |
| `cmdh` | `cmdh tar` / `cmdh git commit` | 优先看 tldr，不够再退到帮助文本 |

### Python / uv

| 命令 | 最常见写法 | 用来干什么 |
|---|---|---|
| `uvinit` | `uvinit` / `uvinit 3.11` | 创建并激活虚拟环境 |
| `uvadd` | `uvadd requests` | 添加运行时依赖 |
| `uvdev` | `uvdev pytest ruff` | 添加开发依赖 |

### Go

| 命令 | 最常见写法 | 用来干什么 |
|---|---|---|
| `gor` | `gor` | 运行当前 Go 项目 |
| `got` | `got` | 跑全部 Go 测试 |
| `gom` | `gom` | 整理 Go 模块依赖 |

---

## 常用 alias 说明

这里不用“前 / 后”这种容易歧义的说法。  
统一写成：

- **你输入这个命令**
- **实际执行的是**

如果你只是想快速找一类命令，可以直接看这里：

| 你现在想做什么 | 看哪一段 |
|---|---|
| 改 shell / 打开编辑器 / 快速回目录 | [编辑器 / shell](#编辑器--shell) |
| 看文件、列目录、树状浏览 | [文件列表 / 目录浏览](#文件列表--目录浏览) |
| 看端口、看进程、看文件内容 | [查看文件 / 系统状态](#查看文件--系统状态) |
| 查 JSON / YAML / 历史命令 / 命令帮助 | [JSON / YAML / 历史命令](#json--yaml--历史命令) |
| 处理 Git 日常操作 | [Git](#git) |
| 管理 tmux session | [tmux](#tmux) |
| 跑 Python / uv | [Python / uv](#python--uv) |
| 跑 Go 项目 | [Go](#go) |

---

### 编辑器 / shell

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `vim` | `hx` / `helix` | 让你直接把 `vim` 当成 Helix 用 |
| `vi` | `hx` / `helix` | 同上 |
| `c` | `clear` | 清屏 |
| `rz` | `exec zsh -l` | 重新启动一个 login zsh |
| `reloadz` | `exec zsh -l` | 同上 |
| `md` | `mkdir -p` | 递归创建目录 |
| `py` | `python3` | 更短的 Python 入口 |
| `..` | `cd ..` | 回到上一级目录 |
| `...` | `cd ../..` | 回到上两级目录 |
| `....` | `cd ../../..` | 回到上三级目录 |

---

### 文件列表 / 目录浏览

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `ls` | `eza` | 用更友好的文件列表代替原生 `ls` |
| `la` | `eza -a --git --color-scale` | 看所有文件，带 git 信息 |
| `ll` | `eza -lbGF --git` | 更详细的长列表 |
| `llm` | `eza -lbGd --git --sort=modified` | 按修改时间看目录 |
| `lt` | `eza --tree --level=2` | 树状查看目录 |
| `lta` | `eza --tree --all --level=2` | 树状查看所有文件 |
| `l1` | `eza -1` | 每行只显示一个条目 |

---

### 查看文件 / 系统状态

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `cat` | `bat --paging=never --style=plain` | 更好看的 `cat` |
| `catp` | `bat --paging=never` | 保留更多格式 |
| `top` | `htop` | 更好用的进程查看器 |
| `ports` | `lsof -nP -iTCP -sTCP:LISTEN` | 看本机监听端口 |
| `psg` | `ps aux \| rg -i` | 查进程 |

---

### JSON / YAML / 历史命令

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `j` | `jq` | JSON 工具 |
| `y` | `yq` | YAML 工具 |
| `hh` | `atuin search` | 搜历史命令 |
| `hhi` | `atuin search --interactive` | 交互式搜历史命令 |
| `hs` | `atuin stats` | 看历史命令统计 |
| `t` | `tldr` | 直接查 tldr 示例页 |
| `ts` | `tldr --search` | 按关键词搜索 tldr 页面 |
| `tu` | `tldr --update` | 手动更新本地 tldr 缓存 |
| `helpme` | `cmdh` | `cmdh` 的更直白别名 |

---

### TLDR / 命令速查

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `t` | `tldr` | 用更短的示例页看命令用法 |
| `ts` | `tldr --search` | 先按关键词搜命令，再打开对应页面 |
| `tu` | `tldr --update` | 刷新本地页面缓存 |
| `tldrp` | `tldr --list-all | fzf` 后打开 | 用 `fzf` 交互式选 tldr 页面 |
| `cmdh` | `tldr -> --help -> man` | 统一命令帮助入口，适合“我就想知道怎么用” |
| `helpme` | `cmdh` | `cmdh` 的别名 |

你可以这样理解：

- **想看最短示例**：`t git-commit`
- **只记得关键词**：`ts archive`
- **想统一走一个帮助入口**：`cmdh git commit`
- **想交互式翻所有页**：`tldrp`

---

### Git

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `gs` | `git status -sb` | 看 Git 状态 |
| `ga` | `git add` | 添加文件 |
| `gaa` | `git add -A` | 添加全部变更 |
| `gc` | `git commit` | 提交 |
| `gcm` | `git commit -m` | 带 message 提交 |
| `gca` | `git commit --amend` | 修改上次提交 |
| `gco` | `git checkout` | checkout |
| `gcb` | `git checkout -b` | 建新分支并切换 |
| `gsw` | `git switch` | switch |
| `gswc` | `git switch -c` | 新建并切换 |
| `gb` | `git branch` | 看分支 |
| `gba` | `git branch -a` | 看所有分支 |
| `gd` | `git diff` | 看 diff |
| `gds` | `git diff --staged` | 看 staged diff |
| `gl` | `git pull` | 拉取 |
| `gp` | `git push` | 推送 |
| `gpf` | `git push --force-with-lease` | 安全一点的强推 |
| `gfetch` | `git fetch --all --prune` | 刷新远端分支 |
| `gundo` | `git reset --soft HEAD~1` | 撤回上一次提交但保留改动 |
| `gst` | `git stash` | 暂存当前工作区改动 |
| `gsta` | `git stash apply` | 应用某个 stash |
| `gsp` | `git stash pop` | 应用并删除最近一个 stash |

---

### tmux

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `tm` | `tmux` | tmux 主命令 |
| `tml` | `tmux ls` | 列出 session |
| `tmn` | `tmux new -s` | 新建一个命名 session |
| `tmc` | `tmux new-session -A -s` | 不存在就创建，存在就连接 |
| `tma` | `tmux attach -t` | 连接到指定 session |
| `tmd` | `tmux detach` | 从当前 tmux session 脱离 |
| `tmk` | `tmux kill-session -t` | 关闭指定 session |

---

### Python / uv

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `u` | `uv` | uv 主命令 |
| `uvv` | `uv venv` | 创建虚拟环境 |
| `uvs` | `source .venv/bin/activate` | 激活虚拟环境 |
| `upy` | `uv run python` | 用 uv 跑 Python |
| `upip` | `uv pip` | 用 uv 的 pip |
| `usync` | `uv sync` | 同步依赖 |
| `ur` | `uv run` | 用 uv 运行命令 |

---

### Go

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `gor` | `go run .` | 运行当前项目 |
| `gofmtw` | `gofmt -w` | 格式化 Go 文件 |
| `got` | `go test ./...` | 运行所有测试 |
| `gob` | `go build ./...` | 构建 |
| `gom` | `go mod tidy` | 整理依赖 |

---

## 新手建议：先这样学

如果你刚接触这套工具，不要试图一次全记住。  
照这个顺序学，基本最省力：

### 第 1 步：先学文件和目录导航

```bash
ff
vf
cdf
rgf keyword
```

学会这 4 个以后，你就已经能：

- 找文件
- 打开文件
- 快速切目录
- 在项目里搜关键字

### 第 2 步：再学 Git 和历史命令

```bash
gs
glogg
hh
```

学会这 4 个以后，你就已经能：

- 看当前改动
- 看提交历史
- 把以前跑过的长命令找回来

### 第 3 步：最后学项目运行

```bash
uvinit
uvadd requests
gor
got
```

学会这 4 个以后，你就已经能：

- 起一个 Python 项目环境
- 安装 Python 依赖
- 跑 Go 项目
- 跑 Go 测试

---

## 常见问题

### `brew` 找不到

| 现象 | 先查 | 常见原因 |
|---|---|---|
| `brew --version` 跑不起来 | `exec zsh -l`<br>`command -v brew`<br>`brew --version` | login shell 还没重进，`brew shellenv` 还没重新加载 |

### `vim` 变成 `hx`，但 `hx` 找不到

| 现象 | 先查 | 常见原因 |
|---|---|---|
| `.zshrc` 生效了，但编辑器命令打不开 | `command -v hx`<br>`command -v helix` | `vim` / `vi` 被 alias 到了 `hx` / `helix`，但本体还没装好、PATH 不对，或者你只跑了 `--only shell` / `--only helix` 而没先装 packages |

### 跑了 `--only shell`，但还是默认 prompt / `tldr` 不能用

| 现象 | 先查 | 常见原因 |
|---|---|---|
| prompt 还是默认 `%`，或 `t` / `cmdh` 找不到 `tldr` | `command -v starship`<br>`command -v tldr` | `--only shell` 只写配置，不安装 `starship` / `tlrc`；新机器需要先跑 `python3 setup.py --only packages` 或全量执行 |

### Linux 上 `fd` 不存在

| 现象 | 先查 | 常见原因 |
|---|---|---|
| 输入 `fd` 提示命令不存在 | `command -v fd`<br>`command -v fdfind` | 有些发行版把命令名装成了 `fdfind`；脚本已兼容 |

### Linux 上 `bat` 不存在

| 现象 | 先查 | 常见原因 |
|---|---|---|
| 输入 `bat` 提示命令不存在 | `command -v bat`<br>`command -v batcat` | 有些发行版把命令名装成了 `batcat`；脚本已兼容 |

### 我不想直接改太多，只想看会做什么

```bash
python3 setup.py --dry-run
```

---

## 一句话总结

这份脚本适合这样用：

> 用系统自带 Python 直接跑，  
> 把 Linux / macOS 机器快速拉到一个统一、顺手、可重复执行的个人开发环境。
