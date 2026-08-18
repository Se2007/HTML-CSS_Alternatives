import os
import math
import pandas as pd
from collections import Counter
from bs4 import BeautifulSoup
import tiktoken
from transformers import AutoTokenizer

class PhDCodeAnalyzer:
    def __init__(self):
        # OpenAI Tokenizers
        self.enc_gpt4 = tiktoken.get_encoding("cl100k_base")
        self.enc_gpt4o = tiktoken.get_encoding("o200k_base")
        
        # HuggingFace Tokenizer for Code LLMs
        try:
            self.hf_tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
        except Exception:
            self.hf_tokenizer = None

    def calculate_entropy(self, tokens):
        if not tokens:
            return 0.0
        counts = Counter(tokens)
        total_tokens = len(tokens)
        entropy = sum(-(count / total_tokens) * math.log2(count / total_tokens) for count in counts.values())
        return round(entropy, 4)

    def calculate_max_depth(self, html_content):
        """محاسبه عمق درخت DOM برای کدهای HTML یا خروجی کامپایل‌شده"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            def get_depth(node):
                if not hasattr(node, 'children') or not list(node.children):
                    return 1
                children_depths = [get_depth(child) for child in node.children if child.name is not None]
                return 1 + (max(children_depths) if children_depths else 0)
            return get_depth(soup)
        except Exception:
            return 0

    def extract_classes_info(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            classes = []
            for tag in soup.find_all(True):
                if 'class' in tag.attrs:
                    cls = tag.attrs['class']
                    if isinstance(cls, list):
                        classes.extend(cls)
                    else:
                        classes.append(cls)
            return len(classes), len(set(classes))
        except Exception:
            return 0, 0

    def analyze_entry(self, name, file_paths):
        """
        ورودی می‌تواند یک فایل یا لیستی از فایل‌ها (مثل main.tsx + styles.css.ts) باشد.
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]

        combined_code = ""
        total_raw_lines = 0

        for path in file_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    combined_code += f"\n/* File: {os.path.basename(path)} */\n" + content
                    total_raw_lines += len([line for line in content.splitlines() if line.strip()])
            else:
                print(f"⚠️ Warning: File {path} not found.")

        if not combined_code:
            return None

        # محاسبات کارهای متنی
        char_count = len(combined_code)

        # محاسبه توکن‌ها روی مجموع کدها
        gpt4_tokens = self.enc_gpt4.encode(combined_code)
        gpt4o_tokens = self.enc_gpt4o.encode(combined_code)
        
        gpt4_count = len(gpt4_tokens)
        gpt4o_count = len(gpt4o_tokens)
        
        hf_count = len(self.hf_tokenizer.encode(combined_code)) if self.hf_tokenizer else "N/A"

        # انتروپی و Redundancy
        unique_tokens = len(set(gpt4o_tokens))
        redundancy_ratio = round(1 - (unique_tokens / gpt4o_count), 4) if gpt4o_count > 0 else 0
        entropy = self.calculate_entropy(gpt4o_tokens)
        char_per_token = round(char_count / gpt4o_count, 2) if gpt4o_count > 0 else 0

        # عمق DOM و کلاس‌ها (فقط روی فایل‌هایی که حاوی HTML/JSX هستند)
        nesting_depth = self.calculate_max_depth(combined_code)
        total_classes, unique_classes = self.extract_classes_info(combined_code)

        return {
            "Framework / Alternative": name,
            "Files Included": ", ".join([os.path.basename(p) for p in file_paths]),
            "Lines": total_raw_lines,
            "Chars": char_count,
            "GPT-4 Tokens": gpt4_count,
            "GPT-4o Tokens": gpt4o_count,
            "Code-LLM Tokens": hf_count,
            "Char/Token Ratio": char_per_token,
            "Nesting Depth": nesting_depth,
            "Total Classes": total_classes,
            "Unique Classes": unique_classes,
            "Redundancy Ratio": redundancy_ratio,
            "Entropy": entropy
        }

# --- نحوه تعریف فایل‌ها ---
if __name__ == "__main__":
    analyzer = PhDCodeAnalyzer()

    # تعریف تارگت‌ها: هم تک‌فایل و هم کامپوننت‌های چندفایلی
    targets = [
        {
            "name": "Baseline (HTML+CSS)",
            "files": ["./index.html"] # یا اگر CSS جداست: ["files/index.html", "files/style.css"]
        },
        {
            "name": "Tailwind CSS",
            "files": ["./tailwind.html"]
        },
        {
            "name": "UnoCSS (Attributify)",
            "files": ["./unocss.html"]
        },
        {
            "name": "Bootstrap",
            "files": ["./bootstrap.html"]
        },
        {
            "name": "Daisy UI",
            "files": ["./daisyui.html"]
        },        
        {
            "name": "Vanilla Extract (TSX + CSS.TS)",
            "files": [
                "./vanilla-extract-demo/src/main.ts",
                "./vanilla-extract-demo/src/styles.css.ts"
            ]
        },
        {
            "name": "Open Props",
            "files": ["./open_props.html"]
        },
        {
            "name": "Formantic UI",
            "files": ["./fomanticui.html"]
        },
        {
            "name": "HAML",
            "files": ["./haml.haml"]
        },
        {
            "name": "Pug",
            "files": ["./pug.pug"]
        }
    ]

    results = []
    for target in targets:
        data = analyzer.analyze_entry(target["name"], target["files"])
        if data:
            results.append(data)

    df = pd.DataFrame(results)

    print("\n### Comprehensive PhD Metrics Matrix\n")
    print(df.to_markdown(index=False))
    df.to_csv("phd_comparative_analysis1.csv", index=False)