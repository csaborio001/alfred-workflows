#!/usr/bin/python3
"""Alfred lorem ipsum preview and text generation. No external dependencies."""
import json
import re
import sys

SENTENCES = (
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
    'Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
    'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.',
    'Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.',
    'Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    'Donec ac odio tempor orci dapibus ultrices in iaculis nunc.',
    'Viverra ipsum nunc aliquet bibendum enim facilisis gravida neque convallis.',
    'Amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus et netus.',
    'Eget nulla facilisi etiam dignissim diam quis enim lobortis scelerisque.',
    'Tellus in metus vulputate eu scelerisque felis imperdiet proin fermentum.',
    'Nunc sed blandit libero volutpat sed cras ornare arcu dui.',
    'Pellentesque massa placerat duis ultricies lacus sed turpis tincidunt id.',
)
WORDS = re.findall(r'[A-Za-z]+', ' '.join(SENTENCES).lower())
UNITS = {'p': 'paragraph', 's': 'sentence', 'w': 'word'}


def parse(query):
    match = re.fullmatch(r'\s*([0-9]+)\s*(p(?:aragraphs?)?|s(?:entences?)?|w(?:ords?)?)\s*', query, re.I)
    if not match:
        raise ValueError('Use a number followed by p, s, or w: li 3p, li 5s, li 20w')
    count = int(match[1])
    if count < 1:
        raise ValueError('Enter a positive number, for example li 3p')
    return count, match[2][0].lower()


def chunks(count, unit):
    if unit == 'w':
        for index in range(count):
            word = WORDS[index % len(WORDS)]
            yield (' ' if index else '') + (word.capitalize() if index == 0 else word)
    elif unit == 's':
        for index in range(count):
            yield (' ' if index else '') + SENTENCES[index % len(SENTENCES)]
    else:
        for index in range(count):
            paragraph = ' '.join(SENTENCES[(index * 5 + offset) % len(SENTENCES)] for offset in range(5))
            yield ('\n\n' if index else '') + paragraph


def preview(query):
    if not query.strip():
        return {'items': [{
            'title': 'Generate lorem ipsum',
            'subtitle': 'Type li 3p for paragraphs, li 5s for sentences, or li 20w for words',
            'valid': False,
        }]}
    try:
        count, unit = parse(query)
    except ValueError as error:
        return {'items': [{'title': 'Enter an amount and element', 'subtitle': str(error), 'valid': False}]}
    label = UNITS[unit] + ('s' if count != 1 else '')
    return {'items': [{
        'title': f'Generate {count:,} {label} of lorem ipsum',
        'subtitle': 'Return to paste into the current app · ⌘Return to copy only',
        'arg': f'{count}{unit}',
        'valid': True,
        'mods': {'cmd': {'subtitle': f'Copy {count:,} {label} to the clipboard'}},
    }]}


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--generate':
        count, unit = parse(' '.join(sys.argv[2:]))
        for chunk in chunks(count, unit):
            sys.stdout.write(chunk)
    else:
        print(json.dumps(preview(' '.join(sys.argv[1:]))))


if __name__ == '__main__':
    main()
