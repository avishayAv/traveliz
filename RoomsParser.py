from utils import get_hex_unicode, get_hebrew_to_real_number

def allow_multiple_string_options(keywords):
    return "(" + '|'.join(keywords) + ")"

class RoomsParser:
    def __init__(self):
        # TODO [AA] : CHANGE d.d to d.5
        # TODO [AA] : make sure that after חדרי, there is no letter
        self.total_rooms = "(\d*\.\d+|\d+)\s+" + self.get_total_rooms_keywords()
        self.hebrew_total_rooms = self.get_hebrew_number_of_rooms() + "\s+" + self.get_total_rooms_keywords()
        self.bed_rooms = "(\d*\.\d+|\d+)\s+" + self.get_rooms_without_livingroom_keywords()
        self.hebrew_bed_rooms = self.get_hebrew_number_of_rooms() + "\s+" + self.get_rooms_without_livingroom_keywords()
        self.living_room = self.get_living_room_keywords()
        self.one_room_apt = self.get_one_room_apt_keywords()

    @staticmethod
    def get_total_rooms_keywords():
        keywords = ['rooms', 'ROOMS', 'Rooms', get_hex_unicode("חדרים")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_rooms_without_livingroom_keywords():
        keywords = ['bedroom', 'bedrooms', get_hex_unicode("חדרי שינה")] #
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_living_room_keywords():
        keywords = ['living room', get_hex_unicode("סלון")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_one_room_apt_keywords():
        keywords = ['studio', get_hex_unicode("סטודיו"), get_hex_unicode("יחידת נופש"), get_hex_unicode("יחידת הנופש")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_hebrew_number_of_rooms():
        keywords = [get_hex_unicode("שני"), get_hex_unicode("שלושה"), get_hex_unicode("ארבעה"), get_hex_unicode("חמישה"),
                    get_hex_unicode("שישה"), get_hex_unicode("שבעה"), get_hex_unicode("שמונה"), get_hex_unicode("תשעה"),
                    get_hex_unicode("עשרה"),
                    get_hex_unicode("שתי"), get_hex_unicode("שלוש"), get_hex_unicode("ארבע"), get_hex_unicode("חמש"),
                    get_hex_unicode("שש"), get_hex_unicode("שבע"), get_hex_unicode("תשע"), get_hex_unicode("עשר")]
        return allow_multiple_string_options(keywords)


