# Python Bootstrap

一个用 **Python 标准库** 写的个人开发环境开荒脚本。

它的目标不是“锁死版本、完全复现”，而是：

- 可以重复执行
- 把一台 Linux / macOS 机器快速收敛到一个统一、顺手、可维护的开发环境
- 完全接管你自己的 shell / nvim / ghostty 配置
- Linux 上可以直接用系统自带的 `python3` 来运行
- 不依赖第三方 Python 库

## 阅读地图

如果你现在的目标很明确，可以直接跳到对应位置：

| 你现在想做什么 | 先看这里 | 你大概率会用到 |
|---|---|---|
| 我只想先试跑，不想马上改系统 | [快速开始](#快速开始) | `python3 setup.py --dry-run` |
| 我想知道它到底会改什么 | [它会做什么](#它会做什么) | 安装项、接管配置、备份路径 |
| 我只想改某一部分 | [运行模式](#运行模式) | `python3 setup.py --only shell` |
| 我想学会最有用的命令 | [最值得先记住的一批命令](#最值得先记住的一批命令) | `ff` / `vf` / `cdf` / `rgf` |
| 我只想查 alias | [常用 alias 说明](#常用-alias-说明) | `gs` / `tmc` / `uvinit` |
| 我已经跑过 setup，现在想排错 | [常见问题](#常见问题) | `brew` / `nvim` / `fd` / `bat` |

### 目录

1. [这是什么](#这是什么)
2. [适用平台](#适用平台)
3. [快速开始](#快速开始)
4. [它会做什么](#它会做什么)
5. [运行模式](#运行模式)
6. [先理解这几个基础工具](#先理解这几个基础工具)
7. [最值得先记住的一批命令](#最值得先记住的一批命令)
8. [常用 alias 说明](#常用-alias-说明)
9. [新手建议：先这样学](#新手建议先这样学)
10. [常见问题](#常见问题)
11. [一句话总结](#一句话总结)

---

## 这是什么

你可以把它理解成：

> 一份长期维护的个人机器初始化脚本

它主要解决这些问题：

- 新机器开荒很麻烦
- 老机器越用越乱
- shell、nvim、终端、常用 CLI 工具不统一
- 想反复执行 setup，但不想每次都手工修环境
- 不想继续维护越来越难看的 bash 大脚本

### 它更适合什么人

- 想把新机器快速整理成统一环境的人
- 接受“脚本直接接管我的 shell / nvim 配置”的人
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
| 只更新 Neovim | `python3 setup.py --only nvim` |
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
nvim
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
- `neovim`
- `htop`
- `node`
- `go`
- `bat`
- `eza`
- `zoxide`
- `lazygit`
- `atuin`
- `oh-my-posh`
- `yq`
- `you-get`

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
~/.config/nvim
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
- `LazyVim starter`

`oh-my-posh` 主题文件放在仓库里：

```text
assets/oh-my-posh/lambda.omp.json
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
python3 setup.py --only nvim
python3 setup.py --only hotkey
python3 setup.py --only git
```

### `--only` 分别是什么意思

如果你只想记住最常用的三个：

- `--only packages`：装软件
- `--only shell`：改 shell / 终端环境
- `--only nvim`：改 Neovim / LazyVim

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
- `oh-my-posh`
- Ghostty 配置

#### `--only nvim`
只处理 Neovim / LazyVim。

默认会额外生成一个 LazyVim 插件文件，提供插入模式下：

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

## 先理解这几个基础工具

后面很多命令都基于这些工具。

如果你不想一口气读完整个 README，可以这样跳着看：

- **我只想学会最常用命令**：直接跳到「最值得先记住的一批命令」
- **我只想查 alias**：直接跳到「常用 alias 说明」
- **我已经跑过 setup，只想排错**：直接跳到「常见问题」

### `fzf`
一个**交互式选择器**。

你可以把它理解成：

> 在终端里弹出一个可搜索的小面板，让你边输入边筛选

比如：

- 选文件
- 选目录
- 选历史命令
- 选搜索结果

### `fd`
一个比 `find` 更好用的找文件工具。

你可以把它理解成：

> 用更短、更顺手的方式找文件和目录

### `rg`
`ripgrep`，一个比 `grep` 更快、更适合搜代码的工具。

你可以把它理解成：

> 在一堆文件里搜关键字

### `atuin`
一个更好用的 shell 历史命令管理工具。

你可以把它理解成：

> 强化版命令历史搜索

### `uv`
一个现代 Python 工具链。

你可以把它理解成：

> 更快、更顺手的 Python 包和虚拟环境工具

---

## 最值得先记住的一批命令

这部分是最重要的。  
如果你是第一次接触 `fzf / fd / rg / atuin / uv`，优先把这些命令学会就够了。

### 怎么读这部分

下面统一按一种卡片格式来写：

- **用途**：这个命令解决什么问题
- **常用输入**：你平时最可能直接敲的写法
- **实际执行 / 组合**：它背后大致调用了什么
- **适合场景**：什么时候最值得用它

---

### `ff`

> **用途：交互式找文件，边搜边看预览。**

**常用输入**

```bash
ff
ff .
ff src
```

**实际组合**

- `fd` 找文件
- `fzf` 做交互筛选
- `bat` 做右侧预览

**适合场景**

- 记得文件名里大概有关键词，但不想慢慢找
- 想快速定位某个配置文件
- 想一边看内容一边选文件

---

### `vf`

> **用途：交互式选文件，然后直接用 `nvim` 打开。**

**常用输入**

```bash
vf
vf .
vf src
```

**实际组合**

- 先像 `ff` 一样选文件
- 然后把结果交给 `nvim`

**适合场景**

- 想快速打开某个文件
- 不想先找路径再手输文件名
- 看到预览后确认就是它，直接进编辑

---

### `cdf`

> **用途：交互式选目录，然后直接切进去。**

**常用输入**

```bash
cdf
cdf .
cdf ~/WKSpace
```

**实际组合**

- `fd` 找目录
- `fzf` 做筛选
- 选中后执行 `cd`

**适合场景**

- 知道目录大概叫什么，但懒得一级一级 `cd`
- 项目很多，想快速跳进去

---

### `rgf keyword`

> **用途：搜索关键字，并把结果放进一个可交互选择器。**

**常用输入**

```bash
rgf TODO
rgf bootstrap .
rgf zprofile ~/.config
```

**实际组合**

- `rg` 搜文本
- `fzf` 展示结果
- 右侧预览对应文件和高亮行

**适合场景**

- 在项目里找函数、配置、关键字
- 想搜出一批结果后再挑一个继续看

---

### `gs`

> **用途：快速看 Git 当前状态。**

**常用输入**

```bash
gs
```

**实际执行的是**

```text
git status -sb
```

**适合场景**

- 我改了哪些文件
- 当前在哪个分支
- 有没有未提交内容

---

### `glogg`

> **用途：更直观地看 Git 提交历史。**

**常用输入**

```bash
glogg
glogg 50
```

**实际效果**

- 用图形化分支线展示提交关系
- 比普通 `git log` 更适合快速扫历史

**适合场景**

- 想看最近有哪些提交
- 想快速理解分支和提交关系

---

### `gnew feature/xxx`

> **用途：快速新建并切换到一个新分支。**

**常用输入**

```bash
gnew feature/login
gnew fix/nvim-path
```

**实际执行的是**

```text
git switch -c <branch-name>
```

**适合场景**

- 开一个新功能分支
- 开一个修复分支

---

### `lg`

> **用途：打开终端里的 Git 图形界面。**

**常用输入**

```bash
lg
```

**实际执行的是**

```text
lazygit
```

**适合场景**

- 提交代码
- 看 diff
- 切分支
- 推送 / 拉取

---

### `hh`

> **用途：搜索以前执行过的命令历史。**

**常用输入**

```bash
hh
```

**实际执行的是**

```text
atuin search
```

**适合场景**

- 以前跑过一条长命令，但忘了
- 不想重新敲一遍

---

### `hhi`

> **用途：交互式搜索命令历史。**

**常用输入**

```bash
hhi
```

**实际执行的是**

```text
atuin search --interactive
```

**适合场景**

- 想一边翻历史一边找
- 历史记录很多，普通搜索不够顺手

---

### `uvinit`

> **用途：在当前目录创建 Python 虚拟环境，并自动激活。**

**常用输入**

```bash
uvinit
uvinit 3.11
```

**默认行为**

```text
Python 3.12
```

**适合场景**

- 新开一个 Python 项目
- 想马上开始装依赖

---

### `uvadd xxx`

> **用途：给当前 Python 项目添加依赖。**

**常用输入**

```bash
uvadd requests
uvadd fastapi pydantic
```

**实际执行的是**

```text
uv add <package...>
```

**适合场景**

- 给项目补运行时依赖
- 不想记 `uv add` 的完整写法

---

### `uvdev pytest`

> **用途：给当前 Python 项目添加开发依赖。**

**常用输入**

```bash
uvdev pytest
uvdev pytest ruff mypy
```

**实际执行的是**

```text
uv add --dev <package...>
```

**适合场景**

- 安装测试工具
- 安装格式化工具
- 安装 lint / 类型检查工具

---

### `gor`

> **用途：运行当前 Go 项目。**

**常用输入**

```bash
gor
```

**实际执行的是**

```text
go run .
```

**适合场景**

- 当前目录就是一个 Go 应用
- 想快速跑起来看看

---

### `got`

> **用途：跑当前项目的全部 Go 测试。**

**常用输入**

```bash
got
```

**实际执行的是**

```text
go test ./...
```

**适合场景**

- 本地快速回归
- 提交前先跑一遍 Go 测试

---

### `gom`

> **用途：整理 Go 模块依赖。**

**常用输入**

```bash
gom
```

**实际执行的是**

```text
go mod tidy
```

**适合场景**

- 加了依赖
- 删了依赖
- `go.mod` / `go.sum` 需要整理

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
| 查 JSON / YAML / 历史命令 | [JSON / YAML / 历史命令](#json--yaml--历史命令) |
| 处理 Git 日常操作 | [Git](#git) |
| 管理 tmux session | [tmux](#tmux) |
| 跑 Python / uv | [Python / uv](#python--uv) |
| 跑 Go 项目 | [Go](#go) |

---

### 编辑器 / shell

| 你输入这个命令 | 实际执行的是 | 说明 |
|---|---|---|
| `vim` | `nvim` | 让你直接把 `vim` 当成 `nvim` 用 |
| `vi` | `nvim` | 同上 |
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
| `lg` | `lazygit` | 打开 lazygit |

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
lg
hh
```

学会这 4 个以后，你就已经能：

- 看当前改动
- 看提交历史
- 用 TUI 做常见 Git 操作
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

**现象**

- `brew --version` 跑不起来
- 明明装了 Homebrew，但当前 shell 里找不到

**先查**

```bash
exec zsh -l
command -v brew
brew --version
```

**说明**

- 这通常是 login shell 还没重进，`brew shellenv` 还没重新加载

### `vim` 变成 `nvim`，但 `nvim` 找不到

**现象**

- `.zshrc` 生效了
- 但 `nvim` 没装好，或者 PATH 不对

**先查**

```bash
command -v nvim
```

**说明**

- `vim` 被 alias 到了 `nvim`
- 如果 `nvim` 本体没装好，就会出现这个现象

### Linux 上 `fd` 不存在

**现象**

- 你输入 `fd`，系统提示命令不存在

**说明**

某些系统里命令名是：

```bash
fdfind
```

脚本里已经兼容了。

### Linux 上 `bat` 不存在

**现象**

- 你输入 `bat`，系统提示命令不存在

**说明**

某些系统里命令名是：

```bash
batcat
```

脚本里也已经兼容了。

### 我不想直接改太多，只想看会做什么

**直接用这个命令**

```bash
python3 setup.py --dry-run
```

---

## 一句话总结

这份脚本适合这样用：

> 用系统自带 Python 直接跑，  
> 把 Linux / macOS 机器快速拉到一个统一、顺手、可重复执行的个人开发环境。
