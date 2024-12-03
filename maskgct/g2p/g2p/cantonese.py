import re
import jieba
import cn2an
from typing import List

# List of (Latin alphabet, Jyutping) pairs:
_latin_to_jyutping = [
    (re.compile("%s" % x[0], re.IGNORECASE), x[1])
    for x in [
        ("a", "aa"),
        ("b", "bei"),
        ("c", "si"),
        ("d", "dei"),
        ("e", "ji"),
        ("f", "ef"),
        ("g", "gei"),
        ("h", "eit"),
        ("i", "ai"),
        ("j", "je"),
        ("k", "kei"),
        ("l", "el"),
        ("m", "em"),
        ("n", "en"),
        ("o", "ou"),
        ("p", "pi"),
        ("q", "kiu"),
        ("r", "aa"),
        ("s", "es"),
        ("t", "ti"),
        ("u", "ju"),
        ("v", "vi"),
        ("w", "deblju"),
        ("x", "eks"),
        ("y", "wai"),
        ("z", "zi"),
    ]
]

# List of (Jyutping, IPA) pairs based on the available IPA in the vocab
_jyutping_to_ipa = [
    (re.compile("%s" % x[0]), x[1])
    for x in [
        ("aa", "ɑː"),  # Cantonese long "a"
        ("a", "æ"),    # Cantonese short "a"
        ("e", "ɛ"),    # Cantonese "e"
        ("i", "i"),    # Cantonese "i"
        ("o", "ɔ"),    # Cantonese "o"
        ("u", "u"),    # Cantonese "u"
        ("yu", "y"),   # Cantonese "yu"
        ("m", "m"),    # Cantonese "m" (nasal)
        ("ng", "ŋ"),   # Cantonese "ng" (nasal)
        # Consonants
        ("b", "p"),    # Cantonese unaspirated "b"
        ("d", "t"),    # Cantonese unaspirated "d"
        ("g", "k"),    # Cantonese unaspirated "g"
        ("gw", "kw"),  # Cantonese "gw"
        ("p", "pʰ"),   # Cantonese aspirated "p"
        ("t", "tʰ"),   # Cantonese aspirated "t"
        ("k", "kʰ"),   # Cantonese aspirated "k"
        ("f", "f"),    # Cantonese "f"
        ("s", "s"),    # Cantonese "s"
        ("z", "ts"),   # Cantonese unaspirated "z"
        ("c", "tsʰ"),  # Cantonese aspirated "c"
        ("h", "h"),    # Cantonese "h"
        ("l", "l"),    # Cantonese "l"
        ("j", "j"),    # Cantonese "j"
        ("w", "w"),    # Cantonese "w"
        # Tone markers
        ("1", "→"),    # High-level tone
        ("2", "↑"),    # High-rising tone
        ("3", "˧"),    # Mid-level tone
        ("4", "↓"),    # Low-falling tone
        ("5", "↓↑"),   # Low-rising tone
        ("6", "˨"),    # Low-level tone
    ]
]

def jyutping_to_ipa(text):
    # Convert Jyutping to IPA
    for regex, replacement in _jyutping_to_ipa:
        text = re.sub(regex, replacement, text)
    return text

def number_to_chinese(text):
    # Convert numbers to Chinese words
    text = cn2an.transform(text, "an2cn")
    return text

def normalization(text):
    # Normalize punctuation and remove unnecessary characters
    text = text.replace("，", ",")
    text = text.replace("。", ".")
    text = text.replace("！", "!")
    text = text.replace("？", "?")
    text = text.replace("；", ";")
    text = text.replace("：", ":")
    text = text.replace("、", ",")
    text = text.replace("‘", "'")
    text = text.replace("’", "'")
    text = text.replace("⋯", "…")
    text = re.sub(r"\s+", "", text)
    text = re.sub(r"[^\u4e00-\u9fff\s_,\.\?!;:\'…]", "", text)
    text = re.sub(r"\s*([,\.\?!;:\'…])\s*", r"\1", text)
    return text

def jyutping_conversion(text, sentence):
    # Simulated Jyutping conversion; in practice, use a proper Jyutping converter
    words = jieba.lcut(text, cut_all=False)
    jyutping_text = " ".join(words)  # This would be converted to actual Jyutping
    return jyutping_text

def latin_to_jyutping(text):
    # Convert Latin characters to Jyutping
    for regex, replacement in _latin_to_jyutping:
        text = re.sub(regex, replacement, text)
    return text

def cantonese_to_ipa(text, sentence):
    # Step 1: Normalize the text and convert numbers to Chinese characters
    text = number_to_chinese(text.strip())
    text = normalization(text)
    
    # Step 2: Convert text to Jyutping phonetic transcription
    text = jyutping_conversion(text, sentence)
    
    # Step 3: Convert any Latin characters to Jyutping
    text = latin_to_jyutping(text)
    
    # Step 4: Map Jyutping to IPA symbols using provided mappings
    text = jyutping_to_ipa(text)
    
    # Step 5: Final cleaning and formatting
    text = re.sub(r"[^\w\s_,\.\?!;:\'…|→↓↑]", "", text)
    text = re.sub(r"([,\.\?!;:\'…])", r"|\1|", text)
    text = re.sub(r"\|+", "|", text)
    text = text.rstrip("|")
    return text
