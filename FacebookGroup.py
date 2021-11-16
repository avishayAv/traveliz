class FacebookGroups:
    def __init__(self):
        # in comment - groups that are waiting for approval
        self.groups = [FacebookGroup("סאבלט בישראל sublet in israel", "461136684495769", False),
                       FacebookGroup("סאבלט גליל עליון ורמת הגולן - Sublet in northern Israel", "Notrthensublet", True),
                       FacebookGroup("סאבלט ביפו", "321832879616768", True,'יפו'),
                       FacebookGroup("סאבלט בצפון הארץ Sublet north Israel", "1276882039335274", True),
                       FacebookGroup("סאבלט ארוך וקצר בתל אביב | long and short term sublet in TLV", "lesublet", True,'תל אביב'),
                       FacebookGroup("דירות ריקות בין חברים בחיפה - סאבלט", "553686734681522", True,'חיפה'),
                       FacebookGroup("סבלטים ודירות לתקופות קצרות בתל אביב", "456319007826317", True,'תל אביב'),
                       # FacebookGroup("סאבלט, דירות נופש והחלפת דירות בכל הארץ", "1716949808517825", True),
                       # FacebookGroup("Sublet - סאבלט - חדרים/ דירות", 272615512803976, False),
                       # FacebookGroup("דירות מפה לאוזן בירושלים סאבלט", "464476390293839", False),
                       # FacebookGroup("השכרה/סאבלט בתל אביב- TLV Apartment Rent/Sublet", "155519307908737", False),
                       FacebookGroup("סאבלט ישראל - Sublet Israel", "576660686025477", True),
                       FacebookGroup("סאבלטים שווים בגליל העליון!!✨", "287386316236384", True),
                       FacebookGroup('סאבלטים וסופ"ש ♣ נחלאות רחביה והסביבה', "812498172191403", True,'ירושלים'),
                       FacebookGroup("סבלט ומגורים לתקופות קצרות טבעון והסביבה", "129090154470531", True),
                       # FacebookGroup("דירות סאבלט בלבד !!! בעמק חפר", "283598432243110", True),
                       FacebookGroup("Short term/sublet In tel aviv סבלט וטווח קצר בתל אביב", "296857008348221", True,'תל אביב'),
                       FacebookGroup("דירות airbnb מרוהטות לסאבלט ונופש.Меблированные квартиры для аренды и отдых",
                                     "512739526298733", True)
                       ]


class FacebookGroup:
    def __init__(self, group_name, group_id, is_public, location=None):
        self.group_name = group_name
        self.group_id = group_id
        self.is_public = is_public
        self.location = location
