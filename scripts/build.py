#!/usr/bin/env python3
"""
Build script for MicroPython deployment.

Combines all source files into a single main.py for easy upload.
"""
import re
from pathlib import Path


SRC_DIR = Path(__file__).parent.parent / "src"
BUILD_DIR = Path(__file__).parent.parent / "build"
OUTPUT_FILE = BUILD_DIR / "main.py"

FILES_ORDER = [
    "config.py",
    "lib/sensor.py",
    "lib/light.py",
    "lib/presence.py",
    "lib/power.py",
    "main.py",
]

IMPORTS_TO_REMOVE = [
    r"^from config import.*$",
    r"^from lib import.*$",
    r"^from lib\.\w+ import.*$",
]


def read_file(path: Path) -> str:
    """Read file content."""
    return path.read_text()


def remove_local_imports(content: str) -> str:
    """Remove imports of local modules."""
    lines = content.split("\n")
    filtered = []
    for line in lines:
        skip = False
        for pattern in IMPORTS_TO_REMOVE:
            if re.match(pattern, line.strip()):
                skip = True
                break
        if not skip:
            filtered.append(line)
    return "\n".join(filtered)


def remove_module_docstring(content: str) -> str:
    """Remove module-level docstring."""
    content = re.sub(r'^"""[\s\S]*?"""\n', '', content)
    content = re.sub(r"^'''[\s\S]*?'''\n", '', content)
    return content


def build() -> None:
    """Combine all files into single main.py."""
    BUILD_DIR.mkdir(exist_ok=True)
    
    header = '''"""
Mirror Light Controller - Combined build.

Auto-generated from src/ files. Do not edit directly.
Edit source files in src/ and run: uv run python scripts/build.py
"""
'''
    
    combined = [header]
    
    for filename in FILES_ORDER:
        filepath = SRC_DIR / filename
        if not filepath.exists():
            print(f"Warning: {filepath} not found, skipping")
            continue
        
        content = read_file(filepath)
        content = remove_local_imports(content)
        
        if filename != "main.py":
            content = remove_module_docstring(content)
        
        section_header = f"\n# {'=' * 60}\n# {filename}\n# {'=' * 60}\n"
        combined.append(section_header)
        combined.append(content.strip())
        combined.append("\n")
    
    output = "\n".join(combined)
    OUTPUT_FILE.write_text(output)
    
    print(f"Built: {OUTPUT_FILE}")
    print(f"Size: {len(output)} bytes")
    print(f"\nTo upload: uv run mpremote connect /dev/ttyUSB0 cp {OUTPUT_FILE} :main.py")


if __name__ == "__main__":
    build()
