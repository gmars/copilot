#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 42 个以拼音命名的文件夹，每个文件夹内包含 Java 控制台小程序（使用集合框架）和 README。
最后生成 java_collections_42.zip。

用法:
    python3 generate_java_collections.py
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

OUTPUT_ZIP = "java_collections_42.zip"

# 多个模板，使用简单的占位符 {STUDENT} 和 {SEED}
TEMPLATES = []

# 模板 1: 使用 ArrayList 模拟待办事项 (Todo list)
TEMPLATES.append(textwrap.dedent("""\
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
public class Main {{
    public static void main(String[] args) {{
        List<String> todo = new ArrayList<>();
        todo.add("写作业");
        todo.add("阅读");
        todo.add("复习");
        System.out.println("欢迎，{STUDENT} 的简单 Todo 列表演示");
        Scanner sc = new Scanner(System.in);
        System.out.println(\"当前待办：\" + todo);
        System.out.print(\"输入一条新任务并回车（空输入结束）：\");
        while (true) {{
            String line = sc.nextLine().trim();
            if (line.isEmpty()) break;
            todo.add(line);
            System.out.println(\"已添加，当前列表：\" + todo);
            System.out.print(\"继续输入（空结束）：\");
        }}
        sc.close();
        System.out.println(\"最终待办：\" + todo);
    }}
}}
"""))

# 模板 2: 使用 HashMap 实现学生成绩登记
TEMPLATES.append(textwrap.dedent("""\
import java.util.HashMap;
import java.util.Map;
public class Main {{
    public static void main(String[] args) {{
        Map<String, Integer> grades = new HashMap<>();
        grades.put(\"Alice\", 85);
        grades.put(\"Bob\", 92);
        grades.put(\"Carol\", 78);
        System.out.println(\"{STUDENT} 的成绩登记演示：\" + grades);
        // 增加/更新
        grades.put(\"Bob\", grades.get(\"Bob\") + 1);
        System.out.println(\"更新 Bob 成绩后：\" + grades);
        // 统计平均分
        double avg = grades.values().stream().mapToInt(Integer::intValue).average().orElse(0.0);
        System.out.printf(\"平均分: %.2f\\n\", avg);
    }}
}}
"""))

# 模板 3: 使用 HashSet 做唯一性检测
TEMPLATES.append(textwrap.dedent("""\
import java.util.HashSet;
import java.util.Set;
public class Main {{
    public static void main(String[] args) {{
        Set<String> set = new HashSet<>();
        String[] names = {{\"Anna\",\"Bob\",\"Anna\",\"Dave\",\"{STUDENT}\"}};
        for (String n : names) set.add(n);
        System.out.println(\"{STUDENT} 的唯一名字集合：\" + set);
        System.out.println(\"集合大小：\" + set.size());
    }}
}}
"""))

# 模板 4: 使用 PriorityQueue 做任务调度（优先级）
TEMPLATES.append(textwrap.dedent("""\
import java.util.PriorityQueue;
public class Main {{
    public static void main(String[] args) {{
        PriorityQueue<String> pq = new PriorityQueue<>();
        pq.add(\"低优先级任务\");
        pq.add(\"中优先级任务\");
        pq.add(\"高优先级任务\");
        System.out.println(\"{STUDENT} 的任务（按字典序）出队演示：\");
        while (!pq.isEmpty()) {{
            System.out.println(pq.poll());
        }}
    }}
}}
"""))

# 模板 5: 使用 LinkedHashMap 做简单 LRU 风格缓存示例（非严格实现）
TEMPLATES.append(textwrap.dedent("""\
import java.util.LinkedHashMap;
import java.util.Map;
public class Main {{
    public static void main(String[] args) {{
        Map<Integer, String> cache = new LinkedHashMap<>(16, 0.75f, true);
        cache.put(1, \"one\"); cache.put(2, \"two\"); cache.put(3, \"three\");
        System.out.println(\"{STUDENT} 的伪 LRU 缓存初始：\" + cache);
        // 访问 2
        cache.get(2);
        cache.put(4, \"four\");
        System.out.println(\"访问 2 并加入 4 后：\" + cache);
    }}
}}
"""))

# 模板 6: 使用 TreeMap 做有序联系人
TEMPLATES.append(textwrap.dedent("""\
import java.util.Map;
import java.util.TreeMap;
public class Main {{
    public static void main(String[] args) {{
        Map<String, String> contacts = new TreeMap<>();
        contacts.put(\"Zhang\", \"1001\");
        contacts.put(\"Li\", \"1002\");
        contacts.put(\"Wang\", \"1003\");
        System.out.println(\"{STUDENT} 的有序联系人：\" + contacts);
        System.out.println(\"首条联系人：\" + ((TreeMap<String,String>)contacts).firstEntry());
    }}
}}
"""))

# 模板 7: 使用 Deque 实现命令历史（栈/队列）
TEMPLATES.append(textwrap.dedent("""\
import java.util.ArrayDeque;
import java.util.Deque;
public class Main {{
    public static void main(String[] args) {{
        Deque<String> history = new ArrayDeque<>();
        history.push(\"打开\");
        history.push(\"编辑\");
        history.push(\"保存\");
        System.out.println(\"{STUDENT} 的命令历史（最近在上）：\" + history);
        System.out.println(\"撤销：\" + history.pop());
        System.out.println(\"剩余历史：\" + history);
    }}
}}
"""))

# 模板 8: 使用 Map<String, List<String>> 实现简单 MultiMap（分组）
TEMPLATES.append(textwrap.dedent("""\
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
public class Main {{
    public static void main(String[] args) {{
        Map<String, List<String>> multi = new HashMap<>();
        add(multi, \"fruit\", \"apple\");
        add(multi, \"fruit\", \"banana\");
        add(multi, \"veg\", \"carrot\");
        System.out.println(\"{STUDENT} 的 MultiMap 示例：\" + multi);
    }}
    private static void add(Map<String, List<String>> m, String k, String v) {{
        m.computeIfAbsent(k, x -> new ArrayList<>()).add(v);
    }}
}}
"""))

# 模板 9: 使用 Collections.frequency 做词频统计
TEMPLATES.append(textwrap.dedent("""\
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
public class Main {{
    public static void main(String[] args) {{
        List<String> words = Arrays.asList(\"apple\",\"banana\",\"apple\",\"orange\",\"banana\",\"apple\");
        System.out.println(\"{STUDENT} 的词频示例：\");
        for (String w : Arrays.asList(\"apple\",\"banana\",\"orange\")) {{
            System.out.println(w + \": \" + Collections.frequency(words, w));
        }}
    }}
}}
"""))

# 模板 10: 使用 LinkedList 做双向队列演示
TEMPLATES.append(textwrap.dedent("""\
import java.util.LinkedList;
import java.util.List;
public class Main {{
    public static void main(String[] args) {{
        LinkedList<Integer> list = new LinkedList<>();
        for (int i = 1; i <= 5; i++) list.add(i);
        System.out.println(\"{STUDENT} 的 LinkedList 初始：\" + list);
        list.addFirst(0); list.addLast(6);
        System.out.println(\"addFirst/addLast 后：\" + list);
    }}
}}
"""))

# 模板 11: 使用 TreeSet 做排序并去重
TEMPLATES.append(textwrap.dedent("""\
import java.util.Arrays;
import java.util.Set;
import java.util.TreeSet;
public class Main {{
    public static void main(String[] args) {{
        Set<Integer> s = new TreeSet<>(Arrays.asList(5,3,9,3,1,5));
        System.out.println(\"{STUDENT} 的 TreeSet（排序去重）：\" + s);
    }}
}}
"""))

# 模板 12: 使用 Arrays.asList + Collections.shuffle 演示集合操作
TEMPLATES.append(textwrap.dedent("""\
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
public class Main {{
    public static void main(String[] args) {{
        List<String> items = Arrays.asList(\"a\",\"b\",\"c\",\"d\",\"e\");
        System.out.println(\"{STUDENT} 原序：\" + items);
        Collections.shuffle(items, new java.util.Random({SEED}));
        System.out.println(\"shuffle({SEED}) 后：\" + items);
    }}
}}
"""))

# 模板 13: 使用 Map + Stream 做查找过滤演示
TEMPLATES.append(textwrap.dedent("""\
import java.util.HashMap;
import java.util.Map;
public class Main {{
    public static void main(String[] args) {{
        Map<String, Integer> map = new HashMap<>();
        map.put(\"a\", 1); map.put(\"bb\", 2); map.put(\"ccc\", 3);
        System.out.println(\"{STUDENT} 的 map: \" + map);
        System.out.println(\"键长度大于1的项：\");
        map.entrySet().stream().filter(e->e.getKey().length()>1).forEach(System.out::println);
    }}
}}
"""))

# 模板 14: 使用 java.util.concurrent 的 ConcurrentLinkedQueue（只是演示，不真正并发）
TEMPLATES.append(textwrap.dedent("""\
import java.util.Queue;
import java.util.concurrent.ConcurrentLinkedQueue;
public class Main {{
    public static void main(String[] args) {{
        Queue<String> q = new ConcurrentLinkedQueue<>();
        q.add(\"task1\"); q.add(\"task2\"); q.add(\"task3\");
        System.out.println(\"{STUDENT} 的 ConcurrentLinkedQueue（演示）：\" + q);
        System.out.println(\"poll: \" + q.poll());
        System.out.println(\"剩余: \" + q);
    }}
}}
"""))

NUM_TEMPLATES = len(TEMPLATES)

def stable_index(name: str) -> int:
    # 稳定的整数映射，不依赖 Python 的 hash 随机化
    s = sum(ord(c) for c in name)
    return s % NUM_TEMPLATES

def make_readme(name: str, idx: int) -> str:
    return textwrap.dedent(f"""\
    # {name}

    这是为 {name} 生成的集合框架控制台小程序（模板 #{idx}）。

    运行：
        javac -d bin src/*.java
        java -cp bin Main

    程序说明在 Main.java 的注释中。
    """)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def write_text(p: Path, content: str):
    p.write_text(content, encoding="utf-8")

def main():
    base = Path.cwd()
    created = []
    for name in NAMES:
        idx = stable_index(name)
        seed = sum(ord(c) for c in name) % 97  # 用于 shuffle 等确定性变化
        src_dir = base / name / "src"
        ensure_dir(src_dir)
        tmpl = TEMPLATES[idx]
        java_src = tmpl.replace("{STUDENT}", name).replace("{SEED}", str(seed))
        # 写入 Main.java
        write_text(src_dir / "Main.java", java_src)
        # 写 README
        write_text(base / name / "README.md", make_readme(name, idx))
        created.append(base / name)

    # 打包 zip
    zip_path = base / OUTPUT_ZIP
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for folder in created:
            for root, _, files in os.walk(folder):
                for f in files:
                    full = Path(root) / f
                    zf.write(full, arcname=str(full.relative_to(base)))
    print(f"已生成 {len(created)} 个文件夹，输出：{zip_path}")

if __name__ == "__main__":
    main()
