# 实验一：实验基础工具使用

本仓库用于记录 Git/GitHub、Codex、CC Switch 与 LaTeX 图片排版实验。

## 目录

- `code/`：文本词频统计程序与测试
- `data/`：输入样例
- `result/`：程序输出与矢量实验图
- `report/`：LaTeX 实验报告源文件
- `evidence/`：脱敏后的实验过程截图

## 运行

```powershell
python code/text_stats.py data/sample.txt --top 10 --csv result/word_counts.csv
python -m unittest discover -s code -p "test_*.py" -v
```

程序只使用 Python 标准库。报告使用 XeLaTeX 编译，实验图采用 PDF 矢量格式。

远程更新记录：已在另一工作副本补充本行，用于验证 `git pull` 同步流程。

## 安全说明

仓库不保存 API Key、访问令牌、`auth.json` 或个人 Codex 配置。提交前请再次检查截图和差异。
