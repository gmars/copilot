"""
生成 42 个拼音命名的静态网站并打包为 pinyin_folders_42.zip。

用法 (Python 3):
    python3 generate_sites.py

脚本行为：
- 在脚本运行目录下，为每个拼音名称创建一个文件夹
- 每个文件夹包含：index.html, styles.css, app.js, assets/avatar.svg, README.md
- 每个站点使用不同的视觉风格（基于 HSL 色相分配）
- 最后生成 pinyin_folders_42.zip，包含所有 42 个文件夹

注意：脚本仅使用 Python 标准库，无需额外依赖。
"""

from __future__ import annotations
import os
import zipfile
import textwrap
from pathlib import Path
from html import escape

NAMES = [
    "liting",
    "ganrourou",
    "panjincheng",
    "huhao",
    "wangxinyu",
    "tanziqiang",
    "zhangxinghuo",
    "tanjierong",
    "fanli",
    "laishuanggui",
    "hehao",
    "liujunli",
    "zhongyupeng",
    "menghangxu",
    "xubo",
    "yuzhuokun",
    "shijiaxue",
    "zouyuxiang",
    "wuhan",
    "zhangyixin",
    "liuhongcheng",
    "zhouziyi",
    "renran",
    "zhengjiezhong",
    "chengyanping",
    "luoyi",
    "zhengronglei",
    "hemeilin",
    "yanghaoran",
    "dengxiaoyan",
    "wangjingsheng",
    "liaojiayu",
    "zhangjingxi",
    "zhangjieyi",
    "tangqiang",
    "huangjiajun",
    "hutao",
    "yangxiling",
    "xieyucan",
    "luoyifeng",
    "guwencai",
    "caichunmei",
]

OUTPUT_ZIP = "pinyin_folders_42.zip"

def make_css(hue: int) -> str:
    css = f"""
:root{{
  --h:{hue};
  --primary: hsl(var(--h) 80% 50%);
  --primary-700: hsl(var(--h) 70% 40%);
  --muted: hsl(var(--h) 20% 85%);
  --bg: #ffffff;
  --fg: #222222;
}}
*{{box-sizing: border-box;}}
body{{font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial;line-height:1.45;margin:0;background:var(--bg);color:var(--fg);}}
.header{{background:linear-gradient(90deg,var(--primary),var(--primary-700));color:white;padding:2rem 1rem;text-align:center;}}
.container{{max-width:900px;margin:1rem auto;padding:1rem;}}
.card{{background:var(--muted);padding:1rem;border-radius:10px;margin-bottom:1rem;}}
.avatar{{width:96px;height:96px;border-radius:50%;display:inline-block;vertical-align:middle;border:4px solid white;box-shadow:0 4px 10px rgba(0,0,0,0.12);}}
.flex{{display:flex;gap:1rem;align-items:center;}}
.nav{{display:flex;gap:0.5rem;justify-content:center;margin-top:1rem;}}
.nav a{{color:rgba(255,255,255,0.9);text-decoration:none;padding:0.5rem 0.8rem;border-radius:6px;background:rgba(0,0,0,0.08);}}
.footer{{text-align:center;padding:1rem;color:#666;font-size:0.9rem;}}
.button{{background:var(--primary);color:white;padding:0.5rem 0.8rem;border:none;border-radius:6px;cursor:pointer}}
@media (max-width:600px){{.container{{padding:.5rem}}.flex{{flex-direction:column;align-items:flex-start}}}}
"""
    return textwrap.dedent(css)

def make_js() -> str:
    js = """
// 简单交互：导航平滑滚动、主题切换和表单验证
document.addEventListener('DOMContentLoaded', function(){
  document.querySelectorAll('a[href^="#"]').forEach(a=>{
    a.addEventListener('click', e=>{
      e.preventDefault();
      document.querySelector(a.getAttribute('href')).scrollIntoView({behavior:'smooth'});
    });
  });
  const form = document.querySelector('form');
  if(form){
    form.addEventListener('submit', e=>{
      e.preventDefault();
      const name = form.querySelector('[name="name"]').value.trim();
      const msg = form.querySelector('[name="message"]').value.trim();
      if(!name || !msg){
        alert('请填写姓名和留言。');
        return;
      }
      alert('已提交（本地演示）：\n姓名：'+name+'\n留言：'+msg);
      form.reset();
    });
  }
});
"""
    return js

def make_avatar_svg(name: str, hue: int) -> str:
    initial = (name[:2] if len(name)>=2 else name).upper()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewBox="0 0 200 200">
  <rect width="200" height="200" rx="20" fill="hsl({hue} 70% 55%)" />
  <text x="50%" y="54%" dominant-baseline="middle" text-anchor="middle" font-family="sans-serif" font-size="56" fill="white">{escape(initial)}</text>
</svg>'''
    return svg

def make_index_html(title: str, name: str) -> str:
    html = f"""
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{escape(title)} - 个人静态站</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="header">
    <div class="container">
      <div class="flex">
        <img src="assets/avatar.svg" alt="头像" class="avatar">
        <div>
          <h1 style="margin:0">{escape(title)}</h1>
          <p style="margin:0.25rem 0 0 0">一个用 HTML5 + CSS3 + JS 实现的静态演示站</p>
        </div>
      </div>
      <nav class="nav">
        <a href="#about">关于</a>
        <a href="#demo">演示</a>
        <a href="#contact">联系</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <section id="about" class="card">
      <h2>关于</h2>
      <p>这是为 <strong>{escape(title)}</strong> 生成的示例静态站，展示响应式布局、CSS 动画与基础交互。</p>
    </section>

    <section id="demo" class="card">
      <h2>演示：图片轮播（本地静态版）</h2>
      <p>下面是一个简单的图像占位轮播（无依赖）。</p>
      <div id="carousel" style="display:grid;grid-template-columns:1fr;gap:8px">
        <img src="assets/avatar.svg" alt="示例1" style="width:100%;border-radius:8px">
      </div>
    </section>

    <section id="contact" class="card">
      <h2>联系</h2>
      <form>
        <label>姓名<br><input name="name" type="text" style="width:100%;padding:.4rem;margin-top:.25rem"></label>
        <label>留言<br><textarea name="message" style="width:100%;padding:.4rem;margin-top:.25rem"></textarea></label>
        <div style="margin-top:.5rem"><button class="button" type="submit">提交</button></div>
      </form>
    </section>
  </main>

  <footer class="footer">&copy; 本示例站 - {escape(title)}</footer>
  <script src="app.js"></script>
</body>
</html>
"""
    return textwrap.dedent(html)

def make_folder_readme(title: str) -> str:
    md = f"""
# {title}

这是为 `{title}` 生成的静态站演示。

包含文件：
- index.html：主页
- styles.css：样式
- app.js：前端交互（表单验证、平滑滚动）
- assets/avatar.svg：占位头像

打开方法：在浏览器中直接打开 `index.html` 即可。
"""
    return textwrap.dedent(md)

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_text_file(p: Path, content: str) -> None:
    p.write_text(content, encoding='utf-8')

def main():
    base = Path.cwd()
    created = []
    for i, name in enumerate(NAMES):
        folder = base / name
        assets = folder / 'assets'
        ensure_dir(assets)
        hue = int((i * 360 / max(1, len(NAMES))) % 360)
        # write files
        write_text_file(folder / 'styles.css', make_css(hue))
        write_text_file(folder / 'app.js', make_js())
        write_text_file(folder / 'index.html', make_index_html(name, name))
        write_text_file(folder / 'README.md', make_folder_readme(name))
        write_text_file(assets / 'avatar.svg', make_avatar_svg(name, hue))
        created.append(folder)

    # zip
    zip_path = base / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for folder in created:
            for root, _, files in os.walk(folder):
                for f in files:
                    full = Path(root) / f
                    rel = full.relative_to(base)
                    zf.write(full, arcname=str(rel))
    print(f'已创建 {len(created)} 个文件夹，导出为 {zip_path}')


if __name__ == '__main__':
    main()
