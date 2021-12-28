import re


def allow_multiple_string_options(keywords):
    return "(" + '|'.join(keywords) + ")"


def remove_time_stamp_from_text(text):
    return '\n'.join([line for line in text.split('\n') if
                      '\u200f' not in line])  # remove RLM (used in facebook for hebrew timestamp)


def remove_url_from_text(text):
    return re.sub("(?P<url>https?://[^\s]+)", '', text)


# Hebrew -> hex unicode
def get_hex_unicode(reg_str):
    uni_str = ''
    for letter in reg_str:
        if letter == ' ':
            uni_str += letter
        else:
            uni_str += r'\u0'
            uni_str += f'{hex(ord(letter)).split("x")[1]}'
    return uni_str


def get_hebrew_to_real_number():
    conversion = {"שני": 2, "שלושה": 3, "ארבעה": 4, "חמישה": 5, "שישה": 6, "שבעה": 7, "שמונה": 8, "תשעה": 9, "עשרה": 10,
                  "שתי": 2, "שלוש": 3, "ארבע": 4, "חמש": 5, "שש": 6, "שבע": 7, "תשע": 9, "עשר": 10,
                  "שניים": 2, "שתיים": 2}
    return conversion


def get_time_keywords_to_time_delta():
    return {'היום': 0, 'מחר': 1, 'מחרתיים': 2, 'הלילה': 0}


whatsapp_group_to_location = {'סאבלט בדפנה': 'דפנה'}
