class FacebookGroups:
    def __init__(self):
        # in comment - groups that are waiting for approval
        self.groups = [FacebookGroup("סאבלט בישראל sublet in israel", "461136684495769", False),
                       FacebookGroup("סאבלט גליל עליון ורמת הגולן - Sublet in northern Israel", "Notrthensublet", True),
                       FacebookGroup("סאבלט ביפו", "321832879616768", True, 'יפו'),
                       FacebookGroup("סאבלט בצפון הארץ Sublet north Israel", "1276882039335274", True),
                       FacebookGroup("סאבלט ארוך וקצר בתל אביב | long and short term sublet in TLV", "lesublet", True,
                                     'תל אביב'),
                       FacebookGroup("דירות ריקות בין חברים בחיפה - סאבלט", "553686734681522", True, 'חיפה'),
                       FacebookGroup("סבלטים ודירות לתקופות קצרות בתל אביב", "456319007826317", True, 'תל אביב'),
                       FacebookGroup("סאבלט, דירות נופש והחלפת דירות בכל הארץ", "1716949808517825", True),
                       # FacebookGroup("Sublet - סאבלט - חדרים/ דירות", 272615512803976, False),
                       # FacebookGroup("דירות מפה לאוזן בירושלים סאבלט", "464476390293839", False),
                       # FacebookGroup("השכרה/סאבלט בתל אביב- TLV Apartment Rent/Sublet", "155519307908737", False),
                       FacebookGroup("סאבלט ישראל - Sublet Israel", "576660686025477", True),
                       FacebookGroup("סאבלטים שווים בגליל העליון!!✨", "287386316236384", True),
                       FacebookGroup('סאבלטים וסופ"ש ♣ נחלאות רחביה והסביבה', "812498172191403", True, 'ירושלים'),
                       FacebookGroup("סבלט ומגורים לתקופות קצרות טבעון והסביבה", "129090154470531", True),
                       FacebookGroup("דירות סאבלט בלבד !!! בעמק חפר", "283598432243110", True),
                       FacebookGroup("Short term/sublet In tel aviv סבלט וטווח קצר בתל אביב", "296857008348221", True,
                                     'תל אביב'),
                       FacebookGroup("דירות airbnb מרוהטות לסאבלט ונופש.Меблированные квартиры для аренды и отдых",
                                     "512739526298733", True),
                       FacebookGroup("דירות סאבלט או שותפים רמת גן גבעתיים", "273671296314569", True),
                       FacebookGroup("דירות מפה לאוזן בחיפה סאבלט", "1452527638328191", True),
                       FacebookGroup("סאבלט ירושלים | Sublet Jerusalem", "JLMsublet", True),
                       FacebookGroup("סאבלט ירושלים Sublet Jerusalem", "subletjerusalem", True),
                       FacebookGroup('דירות מפה לאוזן בת"א סאבלט', "332081620194305", True),
                       FacebookGroup("סאבלט באר שבע ( sublet beer sheva )", "545127305541778", True),
                       FacebookGroup("סאבלט 'מפה לאוזן' דתיים - ירושלים", "207372892747805", True),
                       FacebookGroup('סאבלט כפ"ס רעננה הוד"ש הרצליה רמה"ש - רר', "rr.Sublet", True),
                       FacebookGroup("סאבלט אילת והערבה - Sublet Eilat & arava", "2884188151655198", True),
                       FacebookGroup("סאבלטים בירושלים ♣ sublet in jerusalem", "193362684128420", True),
                       FacebookGroup("סבלט סאבלט בדרום הארץ", "2619739568103394", True),
                       FacebookGroup("סבלט סאבלט צפון מרכז תקופות קצרות", "660162897741493", True),
                       FacebookGroup("סאבלט סבלט רחובות והסביבה", "848649135217504", True),
                       FacebookGroup("סבלט ומגורים לתקופות קצרות טבעון והסביבה", "129090154470531", True),
                       FacebookGroup("לוח סבלט והשכרה בעין הוד, כרם מהרל והאיזור", "1427983830602374", True),
                       FacebookGroup("מצפה רמון סאבלט, סבלט, להשכרה.", "414707243121295", True),
                       FacebookGroup('דירות סאבלט בת-ים,חולון, יפו, ראשל"צ,אזור', "201553787117259", True)
                       ]


class FacebookGroup:
    def __init__(self, group_name, group_id, is_public, location=None):
        self.group_name = group_name
        self.group_id = group_id
        self.is_public = is_public
        self.location = location
