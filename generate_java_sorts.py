#!/usr/bin/env python3
"""
生成 42 个以拼音命名的文件夹，每个文件夹内包含 Java 示例代码：
- src/BubbleSort.java
- src/QuickSort.java
- src/Main.java  （用于演示排序）
- README.md

脚本会在当前目录创建所有文件夹，并在完成后生成 java_sorts_42.zip。
运行： python3 generate_java_sorts.py
"""
from __future__ import annotations
import os
import zipfile
import textwrap
from pathlib import Path

NAMES = [
    "liting","ganrourou","panjincheng","huhao","wangxinyu","tanziqiang","zhangxinghuo","tanjierong","fanli","laishuanggui",
    "hehao","liujunli","zhongyupeng","menghangxu","xubo","yuzhuokun","shijiaxue","zouyuxiang","wuhan","zhangyixin",
    "liuhongcheng","zhouziyi","renran","zhengjiezhong","chengyanping","luoyi","zhengronglei","hemeilin","yanghaoran",
    "dengxiaoyan","wangjingsheng","liaojiayu","zhangjingxi","zhangjieyi","tangqiang","huangjiajun","hutao","yangxiling",
    "xieyucan","luoyifeng","guwencai","caichunmei",
]

OUTPUT_ZIP = "java_sorts_42.zip"

BUBBLE_SRC = textwrap.dedent("""\
public class BubbleSort {
    // 原地冒泡排序（升序）
    public static void sort(int[] a) {
        int n = a.length;
        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (a[j] > a[j+1]) {
                    int t = a[j];
                    a[j] = a[j+1];
                    a[j+1] = t;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }
}
""")

QUICK_SRC = textwrap.dedent("""\
public class QuickSort {
    // 原地快速排序（升序）
    public static void sort(int[] a) {
        quick(a, 0, a.length - 1);
    }
    private static void quick(int[] a, int lo, int hi) {
        if (lo >= hi) return;
        int p = partition(a, lo, hi);
        quick(a, lo, p - 1);
        quick(a, p + 1, hi);
    }
    private static int partition(int[] a, int lo, int hi) {
        int pivot = a[hi];
        int i = lo - 1;
        for (int j = lo; j < hi; j++) {
            if (a[j] <= pivot) {
                i++;
                int t = a[i];
                a[i] = a[j];
                a[j] = t;
            }
        }
        int t = a[i+1];
        a[i+1] = a[hi];
        a[hi] = t;
        return i+1;
    }
}
""")

MAIN_TEMPLATE = textwrap.dedent("""\
import java.util.Arrays;
import java.util.Random;

public class Main {{
    // 简单演示：生成随机数组，复制一份分别用冒泡排序和快速排序排序，并打印前后对比
    public static void main(String[] args) {{
        int[] demo = sampleArray();
        int[] a = Arrays.copyOf(demo, demo.length);
        int[] b = Arrays.copyOf(demo, demo.length);
        System.out.println("原数组: " + Arrays.toString(demo));
        BubbleSort.sort(a);
        System.out.println("冒泡排序结果: " + Arrays.toString(a));
        QuickSort.sort(b);
        System.out.println("快速排序结果: " + Arrays.toString(b));
    }}

    private static int[] sampleArray() {{
        // 固定种子以便演示可重复
        Random r = new Random(42);
        int n = 12;
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) arr[i] = r.nextInt(100);
        return arr;
    }}
}}
""")

README_FOLDER = textwrap.dedent("""\
# {name}

此文件夹包含 Java 排序示例代码：

- src/BubbleSort.java — 冒泡排序（Bubble Sort）
- src/QuickSort.java — 快速排序（Quick Sort）
- src/Main.java — 演示如何��用上述两个排序方法

编译与运行（在包含该文件夹的目录中）：

    javac -d bin src/*.java
    java -cp bin Main

或在 CI 中使用 `javac` 批量编译所有子文件夹后可打包为 zip。
""")

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_text(p: Path, s: str):
    p.write_text(s, encoding="utf-8")

def main():
    base = Path.cwd()
    created = []
    for name in NAMES:
        folder = base / name
        src = folder / "src"
        ensure_dir(src)
        # 写入 Java 源码
        write_text(src / "BubbleSort.java", BUBBLE_SRC)
        write_text(src / "QuickSort.java", QUICK_SRC)
        write_text(src / "Main.java", MAIN_TEMPLATE.format(name=name))
        # README
        write_text(folder / "README.md", README_FOLDER.format(name=name))
        created.append(folder)

    # 打包为 zip
    zip_path = base / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder in created:
            for root, _, files in os.walk(folder):
                for f in files:
                    full = Path(root) / f
                    zf.write(full, arcname=str(full.relative_to(base)))
    print(f"已为 {len(created)} 个文件夹生成 Java 示例，导出为 {zip_path}")

if __name__ == "__main__":
    main()
