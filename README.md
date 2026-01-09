````markdown
```text
pinyin_folders_42 — 生成 42 个拼音命名的静态演示站

说明
----
本仓库（或本脚本）包含一个 Python 3 脚本 generate_sites.py，
运行后会在当前目录生成 42 个以拼音命名的文件夹（见脚本内列表），
每个文件夹里是一个可直接打开的静态示例站（index.html + styles.css + app.js + assets/avatar.svg + README.md）。
每个站点使用不同的配色（依据 HSL 色相），演示响应式布局、CSS3 效果与基础 JS 交互（表单验证、平滑滚动）。

使用方法
-------
1. 确保已安装 Python 3。
2. 将 generate_sites.py 放在目标目录并运行：
   python3 generate_sites.py
3. 运行结束后将生成 pinyin_folders_42.zip（包含所有 42 个文件夹），以及在当前目录产生的各文件夹。

提交/分支
-------
建议创建新分支：generate-sites
提交信息建议：Add generator script and README for creating 42 unique static sites

许可
----
脚本与生成内容供学习/演示使用，按 MIT/你所选许可使用（可在提交中添加 LICENSE）。
```
````