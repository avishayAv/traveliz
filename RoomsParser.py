from utils import get_hex_unicode, get_hebrew_to_real_number

def allow_multiple_string_options(keywords):
    return "(" + '|'.join(keywords) + ")"

class RoomsParser:
    def __init__(self):
        # TODO [AA] : CHANGE d.d to d.5
        # TODO [AA] : make sure that after חדרי, there is no letter
        self.total_rooms = "(\d*\.\d+|\d+)\s+" + self.get_total_rooms_keywords()
        self.hebrew_total_rooms = self.get_hebrew_number_of_rooms() + "\s+" + self.get_total_rooms_keywords()
        self.hebrew_total_rooms_w_half = self.get_hebrew_number_of_rooms() + "\s+" + self.get_half_room_keywords() + "\s+" + self.get_total_rooms_keywords()
        self.bed_rooms = "(\d*\.\d+|\d+)\s+" + self.get_rooms_without_livingroom_keywords()
        self.hebrew_bed_rooms = self.get_hebrew_number_of_rooms() + "\s+" + self.get_rooms_without_livingroom_keywords()
        self.single_bed_room = self.get_single_bedroom_keywords()
        self.living_room = self.get_living_room_keywords()
        self.one_room_apt = self.get_one_room_apt_keywords()
        self.shared_apt = self.get_shared_apt_keywords()
        self.shared_apt_w_rooms = "\d+\s+" + self.get_roommates()
        self.shared_apt_w_rooms_hebrew = self.get_hebrew_number_of_rooms() + "\s+" + self.get_roommates()

    @staticmethod
    def get_total_rooms_keywords():
        keywords = ['rooms', 'ROOMS', 'Rooms', get_hex_unicode("חדרים")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_rooms_without_livingroom_keywords():
        keywords = ['bedroom', 'bedrooms', get_hex_unicode("חדרי שינה")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_single_bedroom_keywords():
        keywords = ['bedroom', get_hex_unicode('חדר שינה')]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_living_room_keywords():
        keywords = ['living room', get_hex_unicode("סלון")]
        return allow_multiple_string_options(keywords)

    # TODO [AA] : add "חדרי" but before check why it fails test_35
    # TODO [AA] : seperate 1 room apt from room in a shared apt - how?
    @staticmethod
    def get_one_room_apt_keywords():
        keywords = ['studio', get_hex_unicode("סטודיו"), get_hex_unicode("יחידת נופש"), get_hex_unicode("יחידת הנופש"), get_hex_unicode("גלריה"), get_hex_unicode("היחידה"), get_hex_unicode("דירת חדר")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_shared_apt_keywords():
        keywords = [get_hex_unicode("חדר בדירה"), get_hex_unicode("חדר בדירת שותפים")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_roommates():
        keywords = ['roomates', get_hex_unicode("שותפים"), get_hex_unicode("שותפות")]
        return allow_multiple_string_options(keywords)

    @staticmethod
    def get_half_room_keywords():
        return get_hex_unicode("וחצי")

    @staticmethod
    def get_hebrew_number_of_rooms():
        keywords = [get_hex_unicode("שני"), get_hex_unicode("שלושה"), get_hex_unicode("ארבעה"), get_hex_unicode("חמישה"),
                    get_hex_unicode("שישה"), get_hex_unicode("שבעה"), get_hex_unicode("שמונה"), get_hex_unicode("תשעה"),
                    get_hex_unicode("עשרה"),
                    get_hex_unicode("שתי"), get_hex_unicode("שלוש"), get_hex_unicode("ארבע"), get_hex_unicode("חמש"),
                    get_hex_unicode("שש"), get_hex_unicode("שבע"), get_hex_unicode("תשע"), get_hex_unicode("עשר"),
                    get_hex_unicode("שניים"), get_hex_unicode("שתיים")]
        return allow_multiple_string_options(keywords)


