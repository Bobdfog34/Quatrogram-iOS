#!/usr/bin/env python3
"""Brand the imported iOS source for Quatrogram.

Runs in the import workflow after cloning gramsrv-Telegram-iOS with submodules.
Only user-visible literals are changed; bundle ids, symbols and class names stay.
"""
import json
import os
import re
from pathlib import Path

ROOT = Path('src')
APP_NAME = os.environ.get('APP_DISPLAY_NAME', 'Quatrogram')
DOMAIN = os.environ.get('LINK_DOMAIN', 'quatrogram.net')
VERSION = os.environ.get('APP_VERSION_NAME', '13.3.1')

PAIRS = [
    ('telegram.org', DOMAIN),
    ('Telegram.org', DOMAIN),
    ('telegram.me', DOMAIN),
    ('telegram.dog', DOMAIN),
    ('t.me', DOMAIN),
    ('telesrv.net', DOMAIN),
    ('Telesrv', APP_NAME),
    ('telesrv', APP_NAME.lower()),
]


def brand(value):
    for old, new in PAIRS:
        value = value.replace(old, new)
    value = re.sub(r'(?<![\w.])Telegram(?![\w.])', APP_NAME, value)
    value = re.sub(r'(?<![\w.])TELEGRAM(?![\w.])', APP_NAME.upper(), value)
    value = re.sub(r'(?<![\w.])telegram(?![\w.])', APP_NAME.lower(), value)
    return value


def patch_literals(text):
    out = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] != '"':
            out.append(text[i])
            i += 1
            continue
        j = i + 1
        literal = ['"']
        while j < n:
            if text[j] == '\\' and j + 1 < n:
                literal.append(text[j:j + 2])
                j += 2
                continue
            if text[j] == '"':
                literal.append('"')
                j += 1
                break
            literal.append(text[j])
            j += 1
        out.append(brand(''.join(literal)))
        i = j
    return ''.join(out)


def patch_xml(text):
    return re.sub(r'(<string\b[^>]*>)(.*?)(</string>)',
                  lambda m: m.group(1) + brand(m.group(2)) + m.group(3),
                  text, flags=re.S)


def patch_strings(text):
    # In .strings files only the value after '=' is user-visible.
    return re.sub(r'(=\s*")(.*?)(")',
                  lambda m: m.group(1) + brand(m.group(2)) + m.group(3),
                  text, flags=re.S)


EXTENSIONS = {'.swift', '.m', '.mm', '.h', '.c', '.cpp', '.strings', '.plist', '.json', '.js', '.sh'}

changed = 0
for path in ROOT.rglob('*'):
    if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
        continue
    try:
        text = path.read_text(encoding='utf-8')
    except (UnicodeDecodeError, OSError):
        continue
    if path.name == 'versions.json':
        continue
    if path.suffix.lower() == '.strings':
        new = patch_strings(text)
    elif path.suffix.lower() in {'.plist', '.xml'}:
        new = patch_xml(text)
    else:
        new = patch_literals(text)
    if new != text:
        path.write_text(new, encoding='utf-8')
        changed += 1

versions_path = ROOT / 'versions.json'
if versions_path.exists():
    versions = json.loads(versions_path.read_text(encoding='utf-8'))
    versions['app'] = VERSION
    versions_path.write_text(json.dumps(versions, indent=4, ensure_ascii=False) + '\n', encoding='utf-8')
    changed += 1

print(f'Quatrogram iOS branding applied to {changed} files, version {VERSION}')
