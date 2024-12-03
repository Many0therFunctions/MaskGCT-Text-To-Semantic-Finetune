from janome.tokenizer import Tokenizer as JPTokenizer
import jaconv
import re
import fugashi



def isJaptxt(text):
    # Regular expression pattern for Japanese characters
    pattern = re.compile(r'[\u3040-\u30FF\u3400-\u4DBF\uF900-\uFAFF]')
    return bool(pattern.search(text))
    

def isViet(text):
    vietnamese_pattern = re.compile(r'[\u00C0-\u1EF9]')
    return bool(vietnamese_pattern.search(text))
    

def isHiraKata(text):
    for char in text:
        code_point = ord(char)
        # Check if the character is in the hiragana or katakana range
        if not ((0x3040 <= code_point <= 0x309F) or (0x30A0 <= code_point <= 0x30FF)):
            return False  # Found a character that is not hiragana or katakana
    return True  # All characters are hiragana or katakana


def isCN(text):
    for char in text:
        if '\u4e00' <= char <= '\u9fff':
            return True
    return False
 