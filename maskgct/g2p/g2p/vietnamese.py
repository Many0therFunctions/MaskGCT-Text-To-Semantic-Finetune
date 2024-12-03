# Copyright (c) 2024 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import re

"""
    Vietnamese Text Cleaner
"""

# List of (regular expression, replacement) pairs for abbreviations in Vietnamese:
_abbreviations = [
    (re.compile(r"\b%s\b" % x[0], re.IGNORECASE), x[1])
    for x in [
        ("TP", "thành phố"),
        ("Q", "quận"),
        ("P", "phường"),
        ("TT", "thị trấn"),
        ("H", "huyện"),
        ("ĐC", "địa chỉ"),
        ("ĐT", "điện thoại"),
        ("KH", "khách hàng"),
        ("NV", "nhân viên"),
        ("CN", "chi nhánh"),
        ("TNHH", "trách nhiệm hữu hạn"),
        ("CP", "cổ phần"),
        ("TN&MT", "tài nguyên và môi trường"),
        ("UBND", "ủy ban nhân dân"),
        ("GDP", "tổng sản phẩm quốc nội"),
        ("CN", "chủ nhật"),
        ("T2", "thứ hai"),
        ("T3", "thứ ba"),
        ("T4", "thứ tư"),
        ("T5", "thứ năm"),
        ("T6", "thứ sáu"),
        ("T7", "thứ bảy"),
        # Add more abbreviations as needed
    ]
]

# Mapping of special characters and punctuation marks to be replaced
_rep_map = {
    "“": "",
    "”": "",
    "‘": "",
    "’": "",
    "–": "-",
    "—": "-",
    "…": "...",
    "•": "",
    "«": "",
    "»": "",
    "≤": " nhỏ hơn hoặc bằng ",
    "≥": " lớn hơn hoặc bằng ",
    "≠": " khác ",
    "→": " dẫn đến ",
    "←": " bắt nguồn từ ",
    "×": " nhân ",
    "÷": " chia ",
    "±": " cộng trừ ",
    "%": " phần trăm ",
    "&": " và ",
    "@": " a còng ",
    "#": " thăng ",
    "$": " đô la ",
    "€": " euro ",
    "₫": " đồng ",
    "¥": " yên ",
    "£": " bảng ",
    "^": "",
    "*": "",
    "_": " ",
    "~": "",
    "`": "",
    "|": "",
    "\\": "",
    "/": " trên ",
    "\n": ". ",
    "\t": " ",
    # Vietnamese punctuation
    "“": "",
    "”": "",
    "‘": "",
    "’": "",
    "„": "",
    "”": "",
    "–": "-",
    "—": "-",
    # Common punctuation
    ".": ".",
    ",": ",",
    "!": "!",
    "?": "?",
    ":": ":",
    ";": ";",
    "(": "",
    ")": "",
    "[": "",
    "]": "",
    "{": "",
    "}": "",
    "<": "",
    ">": "",
    # Remove extra spaces around punctuation
    " .": ".",
    " ,": ",",
    " !": "!",
    " ?": "?",
    " :": ":",
    " ;": ";",
}

# Regular expression patterns for numbers
_decimal_number_re = re.compile(r"([0-9]+(?:\.[0-9]+)?)")
_ordinal_re = re.compile(r"([0-9]+)(?:st|nd|rd|th)")
_fraction_re = re.compile(r"([0-9]+)/([0-9]+)")
_percent_re = re.compile(r"([0-9]+)%")
_currency_re = re.compile(r"([0-9]+)(₫|\$|€|£|¥)")
_number_re = re.compile(r"[0-9]+")

# Function to expand abbreviations
def expand_abbreviations(text):
    for regex, replacement in _abbreviations:
        text = re.sub(regex, replacement, text)
    return text

# Function to replace special symbols and punctuation
def replace_punctuation(text):
    pattern = re.compile("|".join(re.escape(key) for key in _rep_map.keys()))
    return pattern.sub(lambda m: _rep_map[m.group()], text)

# Function to normalize whitespace
def collapse_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()

# Function to remove unnecessary punctuation at the beginning and end
def remove_unnecessary_punctuation(text):
    text = re.sub(r"^[,\.!\?:;\-]+", "", text)
    text = re.sub(r"[,\.!\?:;\-]+$", "", text)
    return text

# Function to normalize numbers
def normalize_numbers(text):
    # Expand percentages
    text = re.sub(_percent_re, lambda m: m.group(1) + " phần trăm ", text)
    # Expand fractions
    text = re.sub(_fraction_re, lambda m: m.group(1) + " trên " + m.group(2), text)
    # Expand ordinals (Vietnamese ordinals are formed differently)
    text = re.sub(_ordinal_re, lambda m: m.group(1) + " ", text)
    # Expand decimal numbers
    text = re.sub(_decimal_number_re, lambda m: number_to_vietnamese(m.group(1)), text)
    # Expand currency
    text = re.sub(_currency_re, lambda m: number_to_vietnamese(m.group(1)) + " " + currency_to_text(m.group(2)), text)
    # Expand standalone numbers
    text = re.sub(_number_re, lambda m: number_to_vietnamese(m.group(0)), text)
    return text

# Function to convert currency symbols to text
def currency_to_text(symbol):
    return {
        "₫": "đồng",
        "$": "đô la",
        "€": "euro",
        "£": "bảng Anh",
        "¥": "yên",
    }.get(symbol, "")

# Function to convert numbers to Vietnamese words
def number_to_vietnamese(number_str):
    try:
        number = float(number_str.replace(",", "."))
    except ValueError:
        return number_str

    # Handle integer and decimal parts separately
    integer_part = int(number)
    decimal_part = number - integer_part

    result = integer_to_vietnamese(integer_part)

    if decimal_part > 0:
        decimal_str = str(decimal_part)[2:]  # Remove '0.'
        decimal_words = "phẩy " + " ".join([digit_to_word(int(d)) for d in decimal_str])
        result = result + " " + decimal_words

    return result

# Function to convert integer numbers to Vietnamese words
def integer_to_vietnamese(number):
    units = ["", "mốt", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    teens = ["mười", "mười một", "mười hai", "mười ba", "mười bốn", "mười lăm", "mười sáu", "mười bảy", "mười tám", "mười chín"]
    tens = ["", "", "hai mươi", "ba mươi", "bốn mươi", "năm mươi", "sáu mươi", "bảy mươi", "tám mươi", "chín mươi"]
    thousands = ["", "nghìn", "triệu", "tỷ"]

    if number == 0:
        return "không"

    words = []
    if number < 0:
        words.append("âm")
        number = -number

    num_str = str(number)
    num_len = len(num_str)
    num_groups = (num_len + 2) // 3

    num_str = num_str.zfill(num_groups * 3)
    for i in range(0, num_groups * 3, 3):
        h, t, u = int(num_str[i]), int(num_str[i + 1]), int(num_str[i + 2])
        group_words = []
        if h > 0:
            group_words.append(units[h] + " trăm")
        else:
            if any([t, u]) and len(words) > 0:
                group_words.append("không trăm")

        if t > 1:
            group_words.append(tens[t])
            if u > 0:
                if u == 5:
                    group_words.append("lăm")
                elif u == 1:
                    group_words.append("mốt")
                else:
                    group_words.append(units[u])
        elif t == 1:
            group_words.append(teens[u])
        else:
            if u > 0:
                if h > 0 or len(words) > 0:
                    group_words.append("linh")
                if u == 5 and (len(words) == 0 or words[-1] != "lăm"):
                    group_words.append("năm")
                else:
                    group_words.append(units[u])

        if group_words:
            group_words.append(thousands[(num_groups - i // 3 - 1)])
            words.extend(group_words)

    return " ".join(words).strip()

# Function to convert single digit to Vietnamese word
def digit_to_word(digit):
    units = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    return units[digit]

# Main text normalization function
def text_normalize(text):
    text = expand_abbreviations(text)
    text = replace_punctuation(text)
    text = remove_unnecessary_punctuation(text)
    text = normalize_numbers(text)
    text = collapse_whitespace(text)
    return text

import re
def map_tones(text):
    tone_map = {
        '1': '→',  # Mid-level tone
        '2': '↑',  # Rising tone
        '3': '',  # Falling tone
        '4': '↓↑', # Dipping tone
        '5': '↓', # Creaky rising tone
        '6': ''  # Glottalized falling tone
    }
    # Replace tone numbers with symbols
    text = re.sub(r'([a-zɪʊɛɔəɜɑːɒʌæœø̃ɯ]+)([1-6])', lambda m: m.group(1) + tone_map.get(m.group(2), ''), text)
    return text
    

# Function to prepare text for phonemization
def vn_to_ipa(text, text_tokenizer):
    if isinstance(text, str):
        text = text_normalize(text)
        #phonemes = map_tones(text_tokenizer(text))
        phonemes = text_tokenizer(text)
        return phonemes
    else:
        normalized_texts = [text_normalize(t) for t in text]
        #phonemes = map_tones(text_tokenizer(normalized_texts))
        phonemes = text_tokenizer(normalized_texts)
        return phonemes
