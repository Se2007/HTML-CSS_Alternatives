import re
import shutil
import logging
from pathlib import Path

import cssutils
from bs4 import BeautifulSoup

from tailwind_mapper import TailwindMapper

# Silence cssutils' noisy warnings in the terminal
cssutils.log.setLevel(logging.CRITICAL)

# Pseudo-classes that only affect a special state (hover, focus, ...)
# and don't affect the page's default/static appearance, so they're
# fully ignored.
IGNORED_PSEUDO_CLASSES = {
    "hover", "focus", "active", "visited", "focus-within",
    "focus-visible", "disabled", "checked", "target",
}

# Only simple single-class selectors are accepted, e.g.: .btn
# Something like .a .b (descendant) or .a.b (compound) will NOT match.
SIMPLE_CLASS_SELECTOR_RE = re.compile(r'^\.([a-zA-Z0-9_-]+)(::?[\w-]+)?$')


class ProjectConverter:
    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.mapper = TailwindMapper()
        # Mapping 
        self.css_mapping = {}
        # Stats of skipped selectors, for the final report to the user
        self.skipped_selectors = []

    def _classify_selector(self, selector: str):
        """
        Check what kind of selector this is and whether it's processable.
        Returns:
            - dict with class_name  ->  if the selector is a simple class (with or without pseudo)
            - None  ->  if the selector is complex (compound/descendant/ID/tag) and should be skipped
            - "SKIP_PSEUDO"  ->  if the selector is a pseudo-class irrelevant to static appearance (e.g. hover)
        """
        selector = selector.strip()
        match = SIMPLE_CLASS_SELECTOR_RE.match(selector)

        if not match:
            # Complex selector (compound, descendant, ID, tag, etc.)
            return None

        class_name = match.group(1)
        pseudo_part = match.group(2)  # ":hover" or None

        if pseudo_part:
            pseudo_name = pseudo_part.lstrip(":")
            if pseudo_name in IGNORED_PSEUDO_CLASSES:
                return "SKIP_PSEUDO"
            # Unknown pseudo-class is also skipped, to be safe
            return None

        return {"class_name": class_name}

    def parse_css_files(self):
        """
            Parse all CSS files and store the classes in the mapping dictionary
        """

        print("1. Parsing CSS files")
        for css_file in self.input_dir.rglob("*.css"):
            parser = cssutils.CSSParser()
            try:
                sheet = parser.parseFile(str(css_file))
                for rule in sheet:
                    if rule.type != rule.STYLE_RULE:
                        # Non-style rules (e.g. @media) are not supported yet
                        continue

                    # A rule can have multiple comma-separated selectors (e.g. ".a, .b { ... }")
                    for selector in rule.selectorText.split(","):
                        selector = selector.strip()
                        result = self._classify_selector(selector)

                        if result == "SKIP_PSEUDO":
                            # Intentionally and silently skipped (hover and similar, by design)
                            continue

                        if result is None:
                            self.skipped_selectors.append((css_file.name, selector))
                            continue

                        class_name = result["class_name"]
                        tailwind_classes = []
                        for prop in rule.style:
                            tw_cls = self.mapper.map_property(prop.name, prop.value)
                            tailwind_classes.append(tw_cls)

                        if class_name not in self.css_mapping:
                            self.css_mapping[class_name] = []
                        self.css_mapping[class_name].extend(tailwind_classes)

            except Exception as e:
                print(f"Unexpected error in file {css_file.name}: {e}")

        if self.skipped_selectors:
            print(f"{len(self.skipped_selectors)} complex selector(s) (compound/descendant/ID/tag) skipped:")
            for file_name, sel in self.skipped_selectors[:10]:
                print(f"   - [{file_name}] {sel}")
            if len(self.skipped_selectors) > 10:
                print(f"   ... and {len(self.skipped_selectors) - 10} more")

    def process_html_files(self):
        """
            Read HTML files, edit the DOM, and replace classes
        """

        print("2. Processing the DOM and updating HTML files...")

        for html_file in self.input_dir.rglob("*.html"):
            with open(html_file, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            # 1. Remove local CSS <link> tags from the DOM
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href", "")
                if href.endswith(".css") and not href.startswith("http"):
                    link.decompose()

            # 2. Add the Tailwind CDN script to <head> if not already present
            if soup.head:
                has_tailwind = soup.find("script", src=lambda s: s and "tailwindcss" in s)
                if not has_tailwind:
                    tailwind_cdn = soup.new_tag("script", src="https://cdn.tailwindcss.com")
                    soup.head.append(tailwind_cdn)

            # 3. Walk the DOM tree and replace old classes with Tailwind ones
            for tag in soup.find_all(True):
                old_classes = tag.get("class")
                if old_classes:
                    new_classes = []
                    for cls in old_classes:
                        if cls in self.css_mapping:
                            new_classes.extend(self.css_mapping[cls])
                        else:
                            # If the class wasn't defined in a CSS file, leave it untouched
                            new_classes.append(cls)

                    # Remove duplicate classes and update the class attribute in the DOM
                    tag["class"] = list(dict.fromkeys(new_classes))

            # 4. Save the new HTML structure into the output folder
            relative_path = html_file.relative_to(self.input_dir)
            output_file_path = self.output_dir / relative_path
            output_file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(soup.prettify())

    def copy_assets(self):
        """Copy remaining files (images, fonts, scripts) to the new folder"""
        print("3. Transferring other files (images, fonts, etc.)...")
        for item in self.input_dir.rglob("*"):
            if item.is_file() and item.suffix.lower() not in [".css", ".html"]:
                relative_path = item.relative_to(self.input_dir)
                dest_path = self.output_dir / relative_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

    def convert(self):
        if not self.input_dir.exists():
            print(f"Input folder not found: {self.input_dir}")
            return

        # Rebuild the output folder
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.parse_css_files()
        self.process_html_files()
        self.copy_assets()
        print(f"\nConversion completed. The path of new project is '{self.output_dir}'.")


if __name__ == "__main__":
    # --- Quick test ---
    import argparse
 
    parser = argparse.ArgumentParser(
        description="Convert an HTML/CSS project into Tailwind CSS classes."
    )
    parser.add_argument(
        "input_dir",
        help="Path to the input project folder (containing .html and .css files)",
    )
    parser.add_argument(
        "output_dir",
        help="Path to the output folder where the converted project will be saved",
    )
 
    args = parser.parse_args()
 
    converter = ProjectConverter(args.input_dir, args.output_dir)
    converter.convert()