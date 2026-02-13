# 文件夹重命名说明

## 已完成的工作

✅ 已更新所有文档和程序中的项目根目录路径引用：
- `README.md`
- `docs/Project_Structure.md`
- `docs/QUICK_REFERENCE.md`
- `gui_app/docs/GUI_ENTRY.md`
- `gui_app/docs/Architecture_Design.md`
- `cli_app/docs/CLI_ENTRY.md`
- `程序分析文档.md`

所有文档中的项目根目录名称已从 `ls_dyna_md` 更新为 `ls-dyna-doc-gen`。

**注意**：核心功能包 `ls_dyna_md/` 的名称保持不变（因为它是 Python 包名，在代码中被导入）。

## 需要手动完成的操作

由于文件夹可能被 Cursor 或其他程序占用，需要手动重命名：

### 方法 1：在文件资源管理器中重命名

1. **关闭 Cursor**（如果正在使用）
2. 打开文件资源管理器
3. 导航到 `C:\CAE\Cursor_Test\`
4. 找到文件夹 `ls_dyna_md`
5. 右键点击 → 重命名
6. 将名称改为 `ls-dyna-doc-gen`
7. 重新打开 Cursor，打开新文件夹

### 方法 2：使用命令行（需要先关闭 Cursor）

```powershell
cd C:\CAE\Cursor_Test
Rename-Item -Path "ls_dyna_md" -NewName "ls-dyna-doc-gen"
```

### 方法 3：如果重命名失败

如果文件夹被锁定无法重命名，可以：
1. 重启计算机
2. 或者使用 `robocopy` 复制到新名称，然后删除旧文件夹：

```powershell
cd C:\CAE\Cursor_Test
robocopy "ls_dyna_md" "ls-dyna-doc-gen" /E /MOVE
```

## 验证

重命名完成后，请验证：
1. 新文件夹路径：`C:\CAE\Cursor_Test\ls-dyna-doc-gen`
2. 运行程序测试：
   ```bash
   python gui_app/main_gui.py
   python cli_app/main.py
   ```
3. 检查 Git 仓库是否正常工作：
   ```bash
   git status
   ```

## 重要提示

- ✅ 核心功能包 `ls_dyna_md/` 的名称**保持不变**（这是 Python 包名）
- ✅ 只有项目根目录名称从 `ls_dyna_md` 改为 `ls-dyna-doc-gen`
- ✅ 所有代码中的 `from ls_dyna_md import ...` 保持不变
- ✅ 所有文档中的 `ls_dyna_md/docs/` 路径保持不变（这是包内路径）
