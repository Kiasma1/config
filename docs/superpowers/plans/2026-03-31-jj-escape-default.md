# JJ Escape Default Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the repository's default Neovim bootstrap create a LazyVim-managed insert-mode `jj` to `<Esc>` mapping.

**Architecture:** Keep the change inside `setup.py` so `python3 setup.py --only nvim` remains the single source of truth for generated Neovim defaults. Generate one managed Lua file under `lua/plugins/` so the mapping follows LazyVim's extension pattern instead of editing starter-owned files.

**Tech Stack:** Python 3 standard library, LazyVim plugin configuration, unittest

---

### Task 1: Lock the desired generated file behavior with a regression test

**Files:**
- Create: `tests/test_setup_nvim.py`
- Modify: none
- Test: `tests/test_setup_nvim.py`

- [ ] **Step 1: Write the failing test**

```python
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import setup


class EnsureLazyVimTests(unittest.TestCase):
    def test_ensure_lazyvim_writes_insert_mode_jj_escape_plugin(self):
        with tempfile.TemporaryDirectory() as home_dir:
            with mock.patch.dict(os.environ, {"HOME": home_dir}, clear=False):
                bootstrap = setup.Bootstrap(dry_run=False, only="nvim")

                def fake_clone_repo_to_path(repo, dest, strip_git=False):
                    dest.mkdir(parents=True, exist_ok=True)

                bootstrap.clone_repo_to_path = fake_clone_repo_to_path
                bootstrap.ensure_lazyvim()

                plugin_file = Path(home_dir) / ".config" / "nvim" / "lua" / "plugins" / "jj-escape.lua"

                self.assertTrue(plugin_file.exists())
                plugin_content = plugin_file.read_text(encoding="utf-8")
                self.assertIn('mode = "i"', plugin_content)
                self.assertIn('{ "jj", "<Esc>"', plugin_content)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_setup_nvim -v`
Expected: FAIL because `jj-escape.lua` is not created yet.

- [ ] **Step 3: Write minimal implementation**

```python
        self.write_file_if_changed(
            self.nvim_dir / "lua" / "plugins" / "jj-escape.lua",
            """return {
  {
    "LazyVim/LazyVim",
    keys = {
      { "jj", "<Esc>", mode = "i", desc = "Exit insert mode" },
    },
  },
}
""",
            0o644,
        )
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_setup_nvim -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/superpowers/plans/2026-03-31-jj-escape-default.md tests/test_setup_nvim.py setup.py
git commit -m "feat: add default nvim jj escape mapping"
```
