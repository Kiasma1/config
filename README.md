# Python Bootstrap

一个用 **Python 标准库** 写的个人开发环境开荒脚本。

它的目标不是“锁死版本、完全复现”，而是：

- 可以重复执行
- 把一台 Linux / macOS 机器快速收敛到一个统一、顺手、可维护的开发环境
- 完全接管你自己的 shell / nvim / ghostty 配置
- Linux 上可以直接用系统自带的 `python3` 来运行
- 不依赖第三方 Python 库

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

#### `--only hotkey`
只处理 Ghostty 全局快捷键相关内容：

- Hammerspoon 配置
- 热键配置写入

#### `--only git`
只处理 git 全局配置。

---

## 先理解这几个基础工具

后面很多命令都基于这些工具。

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

---

### `ff`

#### 输入这个命令

```bash
ff
```

#### 它是干什么的

**交互式选文件。**

你运行它之后，会看到一个可搜索的文件列表：

- 你一边输入关键词
- 它一边筛选文件
- 右边会预览文件内容

#### 实际原理

它大致等于：

- 用 `fd` 找文件
- 用 `fzf` 弹出选择界面
- 用 `bat` 预览文件内容

#### 怎么用

```bash
ff
ff .
ff src
```

#### 适合场景

- 我记得文件名里大概有个关键词，但不想慢慢 `cd`
- 我想快速找到某个配置文件
- 我想边看内容边选文件

---

### `vf`

#### 输入这个命令

```bash
vf
```

#### 它是干什么的

**交互式选文件，然后直接用 `nvim` 打开。**

#### 实际行为

它会先执行“像 `ff` 那样选文件”，然后把你选中的文件交给：

```text
nvim
```

#### 怎么用

```bash
vf
vf .
vf src
```

#### 适合场景

- 我想快速打开某个文件，但不想先找路径再输文件名
- 看见预览后，确认就是它，直接打开编辑

---

### `cdf`

#### 输入这个命令

```bash
cdf
```

#### 它是干什么的

**交互式选目录，然后直接切进去。**

#### 实际原理

- 用 `fd` 找目录
- 用 `fzf` 让你筛选
- 选中后执行 `cd`

#### 怎么用

```bash
cdf
cdf .
cdf ~/WKSpace
```

#### 适合场景

- 我知道目录大概叫什么，但懒得一级一级 `cd`
- 项目很多，想快速跳进去

---

### `rgf keyword`

#### 输入这个命令

```bash
rgf keyword
```

#### 它是干什么的

**在文件里搜索关键字，并把结果放到一个可交互选择器里。**

#### 实际原理

- 用 `rg` 搜文本
- 用 `fzf` 展示结果
- 右边预览对应文件和高亮行

#### 怎么用

```bash
rgf TODO
rgf bootstrap .
rgf zprofile ~/.config
```

#### 适合场景

- 在项目里找某个函数、配置、关键字
- 想搜出结果后再挑一个继续看

---

### `gs`

#### 输入这个命令

```bash
gs
```

#### 实际执行的是

```text
git status -sb
```

#### 它是干什么的

**快速看 Git 当前状态。**

比普通 `git status` 更短、更适合日常频繁看。

#### 怎么用

```bash
gs
```

#### 适合场景

- 我改了什么文件
- 当前在哪个分支
- 有没有未提交内容

---

### `glogg`

#### 输入这个命令

```bash
glogg
```

#### 它是干什么的

**图形化地看 Git 提交历史。**

#### 怎么用

```bash
glogg
glogg 50
```

#### 适合场景

- 想看最近有哪些提交
- 想快速理解分支和提交关系
- 比 `git log` 更直观

---

### `gnew feature/xxx`

#### 输入这个命令

```bash
gnew feature/login
```

#### 它是干什么的

**快速新建并切换到一个新分支。**

#### 实际执行的是

```text
git switch -c <branch-name>
```

#### 怎么用

```bash
gnew feature/login
gnew fix/nvim-path
```

---

### `lg`

#### 输入这个命令

```bash
lg
```

#### 实际执行的是

```text
lazygit
```

#### 它是干什么的

**打开一个终端里的 Git 图形界面。**

#### 适合场景

- 提交代码
- 看 diff
- 切分支
- 推送 / 拉取

如果你不想一直记很多 Git 子命令，这个很值。

---

### `hh`

#### 输入这个命令

```bash
hh
```

#### 实际执行的是

```text
atuin search
```

#### 它是干什么的

**搜索你以前执行过的命令历史。**

#### 怎么用

```bash
hh
```

一般你输入后，会进入命令历史搜索界面。

#### 适合场景

- 我以前跑过某条很长的命令，但忘了
- 我不想重新敲一遍

---

### `hhi`

#### 输入这个命令

```bash
hhi
```

#### 实际执行的是

```text
atuin search --interactive
```

#### 它是干什么的

**交互式搜索命令历史。**

比普通 `hh` 更适合一边翻一边找。

---

### `uvinit`

#### 输入这个命令

```bash
uvinit
```

#### 它是干什么的

**在当前目录创建 Python 虚拟环境，并自动激活。**

#### 默认行为

默认会用：

```text
Python 3.12
```

#### 怎么用

```bash
uvinit
uvinit 3.11
```

#### 适合场景

- 新开一个 Python 项目
- 想马上开始装依赖

---

### `uvadd xxx`

#### 输入这个命令

```bash
uvadd requests
```

#### 实际执行的是

```text
uv add requests
```

#### 它是干什么的

**给当前 Python 项目加依赖。**

#### 怎么用

```bash
uvadd requests
uvadd fastapi pydantic
```

---

### `uvdev pytest`

#### 输入这个命令

```bash
uvdev pytest
```

#### 实际执行的是

```text
uv add --dev pytest
```

#### 它是干什么的

**安装开发依赖。**

#### 适合场景

- 测试工具
- 格式化工具
- lint 工具

例如：

```bash
uvdev pytest ruff mypy
```

---

### `gor`

#### 输入这个命令

```bash
gor
```

#### 实际执行的是

```text
go run .
```

#### 它是干什么的

**运行当前 Go 项目。**

#### 适合场景

- 当前目录就是一个 Go 应用
- 想快速跑起来看看

---

### `got`

#### 输入这个命令

```bash
got
```

#### 实际执行的是

```text
go test ./...
```

#### 它是干什么的

**跑当前项目的全部 Go 测试。**

---

### `gom`

#### 输入这个命令

```bash
gom
```

#### 实际执行的是

```text
go mod tidy
```

#### 它是干什么的

**整理 Go 模块依赖。**

#### 适合场景

- 加了依赖
- 删了依赖
- `go.mod` / `go.sum` 需要整理

---

## 常用 alias 说明

这里不用“前 / 后”这种容易歧义的说法。  
统一写成：

- **你输入这个命令**
- **实际执行的是**

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

### 第 1 步：先学这 4 个

```bash
ff
vf
cdf
rgf keyword
```

你只要先理解：

- `ff`：找文件
- `vf`：找文件并打开
- `cdf`：找目录并进入
- `rgf`：搜文本并浏览结果

这 4 个学会了，`fzf / fd / rg` 的核心感觉就出来了。

### 第 2 步：再学这 4 个

```bash
gs
glogg
lg
hh
```

理解：

- `gs`：看 Git 状态
- `glogg`：看提交历史
- `lg`：打开 Git TUI
- `hh`：搜历史命令

### 第 3 步：再学这 4 个

```bash
uvinit
uvadd requests
gor
got
```

理解：

- `uvinit`：起一个 Python 项目环境
- `uvadd`：加 Python 依赖
- `gor`：跑 Go 项目
- `got`：跑 Go 测试

---

## 常见问题

### `brew` 找不到

先执行：

```bash
exec zsh -l
```

再试：

```bash
command -v brew
brew --version
```

### `vim` 变成 `nvim`，但 `nvim` 找不到

说明：

- `.zshrc` 生效了
- 但 `nvim` 没装好，或者 PATH 不对

先查：

```bash
command -v nvim
```

### Linux 上 `fd` 不存在

某些系统里命令名是：

```bash
fdfind
```

脚本里已经兼容了。

### Linux 上 `bat` 不存在

某些系统里命令名是：

```bash
batcat
```

脚本里也已经兼容了。

### 我不想直接改太多，只想看会做什么

用：

```bash
python3 setup.py --dry-run
```

---

## 一句话总结

这份脚本适合这样用：

> 用系统自带 Python 直接跑，  
> 把 Linux / macOS 机器快速拉到一个统一、顺手、可重复执行的个人开发环境。
