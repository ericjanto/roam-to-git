import os
import re
from collections import defaultdict
from itertools import takewhile
from pathlib import Path
from typing import Dict, List, Match, Tuple

def read_markdown_directory(raw_directory: Path) -> Dict[str, str]:
    contents = {}
    for file in raw_directory.iterdir():
        if file.is_dir():
            # We recursively add the content of sub-directories.
            # They exists when there is a / in the note name.
            for child_name, content in read_markdown_directory(file).items():
                contents[f"{file.name}/{child_name}"] = content
        if not file.is_file():
            continue
        content = file.read_text(encoding="utf-8")
        parts = file.parts[len(raw_directory.parts):]
        file_name = os.path.join(*parts)
        contents[file_name] = content
    return contents


def format_markdown(contents: Dict[str, str]) -> Dict[str, str]:
    # Format and write the markdown files
    out = {}
    for file_name, content in contents.items():
        content = add_title(content, file_name)
        if len(content) > 0:
            out[file_name] = content
    return out

def add_title(content: str, file_name: str):
    return {file_name} + "\n\n" + {content}