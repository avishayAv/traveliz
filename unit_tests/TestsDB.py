import datetime
from copy import deepcopy


class Test:
    def __init__(self, post_time, text, start_date, end_date, price, location):
        self.post_time: datetime = post_time
        self.text: str = text
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.price: list(int) = price
        self.location: str = location


class Tests:
    def __init__(self):
        self.tests = [test1, test2, test3, test4, test5, test6, test7, test8, test9, test10,
                      test11, test12, test13, test14, test15, test16, test17, test18, test19, test20,
                      test21]

    def dump_dates_to_test(self):
        dates_tests = deepcopy(self.tests)
        dates_tests.pop(20)  # TODO [AA] : add test after filtering out "1.5 rooms"
        dates_tests.pop(17)  # TODO [AA] : add test after figuring out context
        dates_tests.pop(6)  # TODO [AA] : add test after figuring out context
        return [(test.text, test.start_date, test.end_date, test.post_time) for test in dates_tests]


test1 = Test(
    post_time=datetime.date(2021, 11, 14),
    text="סאבלט בשדה אליעזר 😊\nמסבלטים את הסטודיו שלנו.\nלמחפשים לטייל, לנוח או סתם להיות במקום שקט צמוד לטבע.\n"
         "בתאריך שבין v 15/11עד ה 28/11, הדירה שלנו פנויה..\n"
         "דירת סטודיו גדולה(52 מ') עם מרפסת מקורה שצופה על עמק החולה ורמת הגולן. מלא טבע וירוק.\n"
         "5 דק' הליכה מנחל דישון ונקודת יציאה למסלולי טיול מרהיבים שיוצאים מהמושב .\nמתאימה ליחיד או זוג.\n"
         "עלות 300 ללילה. מינימום 2 לילות.\nזמינים בטלפון/ וואטסאפ.\nמשה- 052-6780696",
    start_date=datetime.date(2021, 11, 15),
    end_date=datetime.date(2021, 11, 28),
    price=[300],
    location='שדה אליעזר')

test2 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='וילה לסאבלט בחנוכה בין התאריכים 30.11-5.12 במושב שדה-אילן(2 דקות מצומת גולני)\n'
         'יפה מאוד! נקייה מאוד! מטבח כשר! חצר מטופחת עם פינות ישיבה..\n052-8316179',
    start_date=datetime.date(2021, 11, 30),
    end_date=datetime.date(2021, 12, 5),
    price=[],
    location='שדה אילן')

test3 = Test(
    post_time=datetime.date(2021, 8, 28),
    text='מירית אמיר\n\u200f28 באוגוסט\u200f ב-\u200f9:08\u200f ·\n\n'
         'מקומות פנויים החל מה14 לנובמבר עד ה-29/11,מהרו להזמין מקומות אחרונים,יחידת נופש מהממת לזוג באילת.מחיר שווה .עם חצר פרטית.'
         '\nלפרטים 053-6576136.\n050-9939973',
    start_date=datetime.date(2021, 11, 14),
    end_date=datetime.date(2021, 11, 29),
    price=[],
    location='אילת')

test4 = Test(
    post_time=datetime.date(2021, 11, 10),
    text='אופק בגולן\n-בית קסום שהוא פינוק אמיתי-\nלזוגות בלבד\nבית קרקע באזור פסטורלי במושב רמות, עם חצר\n'
         'ענקית, פינת ישיבה בחוץ מתחת לפרגולה\nשני חדרי שינה וסלון עם ספה נפתחת, טלוויזיה בכל חדר'
         ', מטבח מאובזר כהלכה, מזגן בכל חדר שירותים, ומקלחת מפנקת ומדהימה.\nטל:0542545614\nhttps://oasraf.wixsite.com/ofekhouse'
         '\n\nמחיר לזוג:\nיום חול 450\nסופ״ש 600\n(המחיר משתנה לפי מספר הלילות ותאריכים😀)',
    start_date=None,
    end_date=None,
    price=[450, 600],
    location='רמות')

test5 = Test(
    post_time=datetime.date(2021, 11, 11),
    text='#סאבלט_חנוכה 💫\n\nבהר הכי יפה בגליל-\nהר כמון ביישוב כמון 🌳\n\nמיום חמישי 2.12 עד יום ראשון 5.12\n\n'
         'כמה פרטים חשובים:\n💫 המטבח כשר\n💫 בבית גר חתול שנכנס ויוצא לסירוגין\n💫 יש כל מה שצריך לדתיים: פלטה ומיחם.\n'
         '💫 הבית יכול להכיל עד 8 אנשים\n💫 המיקום הכי שווה בצפון!\n\nלפרטים נוספים ומחירים-\nרק בוואטסאפ:\n052-3437718\n\nיום טוב 😊',
    start_date=datetime.date(2021, 12, 2),
    end_date=datetime.date(2021, 12, 5),
    price=[],
    location='כמון')

test6 = Test(
    post_time=datetime.date(2021, 11, 10),
    text='היי חברים\nמי שרוצה *סאבלט*\nבדירה מהממת בשכונת שפירא המפתחת,\n\nדירה מדהימה ברחוב בן אשר 7 ,\n'
         'במרחק הליכה מכם תוכלו ליהנות מפלורנטין ושוק לוינסקי'
         '!\n\nדירת סטודיו 20 מ"ר בערך.\n\nבדירה יש הכל !!\nהיא מרוהטת לגמרי עם אינטרנט, טלוויזיה חכמה וכל דבר שתצטרכו כדי שיהיה לכם הכי כיף בעולם'
         '.\n\n3,800 כולל הכל - לא צריך להביא כלום לדירה חוץ מבגדים.\n\nדברו איתי - 0505290072',
    start_date=None,
    end_date=None,
    price=[3800],
    location='תל אביב')

test7 = Test(
    post_time=datetime.date(2021, 11, 11),
    text="מסאבלט את דירתי 🏠 המתוקה בטבעון ל-3 חודשים. כניסה מיידית."
         " 🧙מרפסת שווה, פרקט, מטבח מאובזר, מיקום מרכזי, שקט ומלא טבע פתוח לטייל בו במרחק הליכה(5-10 ד'). ממליץ בחום.",

    start_date=datetime.date(2021, 11, 24),  # TODO [AA] : grep כניסה מיידית
    end_date=datetime.date(2021, 2, 24),
    price=[],
    location='קריית טבעון')

test8 = Test(
    post_time=datetime.date(2021, 11, 11),
    text='להשכרה סאבלט ל3 חודשים, מתאריך 22 .31.12.21-31.03, יפו ג, 7'
         ' דקות הליכה מחוף הסי פאלס, דקה הליכה ממרכז קניות ותחבורה ציבורית, איזור שקט, הדירה מרוהטת קומפלט, 50 מ"ר, מכונת כביסה, '
         'מחיר לחודש 3,700 שח כולל כל החשבונות ואינטרנט חוץ מחשמל, מתאים לדייר או דיירת, בלי בעלי חיים, פרטים בפרטי :)',
    start_date=datetime.date(2021, 12, 31),
    end_date=datetime.date(2022, 3, 31),
    price=[3700],
    location='יפו')

test9 = Test(
    post_time=datetime.date(2021, 11, 12),
    text="SUBLET FOR 3 MONTHS \\\\ 1.5 ROOMS FLAT \\\\CITY CENTER 🌈☀🌷\n\n14\\ 11 \\21 - 09 \\ 02 \\ 22\n\n"
         "Spacious 1.5 rooms basement apartment with lots of good vibes.\nFully furnished - comfortable double bed"
         ", SMART TV '55, WIFI, AC, equipped kitchen 😎\n\nA minute walk from Gan Meir, King George, Dizengoff square"
         ", Carmel Market, the Kerem and the beach.\nlocated on Zalman Shneur street.\nA quiet cozy place full of privacy"
         " 🙉🙉\n\nThere is everything, you can come with a suitcase✈️\nAlso suitable for a couple 👩\u200d❤️"
         "\u200d💋\u200d👨\nAvailable immidiatly.\n5000 NIS per month included everything except electricity.\n\n"
         "***********************************************************************\n\nסאבלט ל- 3 חודשים \\\\"
         " 1.5 חדרים דירה \\\\ מרכז עיר 🌈☀🌷\n\n14\\\\ 11 \\\\21 - 09 \\\\ 02 \\\\ 22\n\nדירת מרתף מרווחת"
         " 1.5 חדרים מלאה באנרגיות טובות.\nריהוט מלא - מיטה זוגית נוחה, טלוויזיה חכמה 55 ', WIFI, "
         "מיזוג אוויר, מטבח מאובזר 😎\n\nדקה הליכה מגן מאיר, קינג ג'ורג ', כיכר דיזנגוף, שוק הכרמל, הכרם וחוף הים.\n"
         "ממוקם ברחוב זלמן שניאור.\nמקום שקט ונעים מלא בפרטיות.🙉🙉\n\nיש הכל, אפשר להגיע עם מזוודה✈️\nמתאים גם לזוג"
         "👩\u200d❤️\u200d💋\u200d👨\nכניסה מיידית.\n5000 ₪ לחודש כולל כל החשבונות למעט חשמל.",
    start_date=datetime.date(2021, 11, 14),
    end_date=datetime.date(2022, 2, 9),
    price=[5000],
    location='תל אביב')

test10 = Test(
    post_time=datetime.date(2021, 11, 13),
    text='מוזמנים אלינו לקיבוץ בית השיטה,\nליחידת אירוח מקסימה.\n'
         'במרכז עמק המעיינות ליד הסחנה, נחל האסי בסמיכות לנחל הקיבוצים.\nיחידת נופש נקיה ומסודרת\n'
         '✅ מתאימה לזוג/זוג+ילד\n✅ מיטה זוגית.\n✅ טלוויזיה ממיר פרטנר.\n✅ אינטרנט.\n✅ ממוזגת.\n'
         '✅ שירוקלחת.\n✅ מטבחון מאובזר.\n✅ מכונת כביסה.\n✅ פינת ישיבה.\n✅ חצר עם פינת ישיבה.\n'
         'לפרטים נוספים בטלפון :\nדודו - 050-6279384',
    start_date=None,
    end_date=None,
    price=[],
    location='בית השיטה')

test11 = Test(
    post_time=datetime.date(2021, 11, 13),
    text='הוילה המפנקת שלנו ביישוב פסטוראלי בגלבוע פנויה בחנוכה בין ה 29-1 ו 5-6/12 פינת מנגל,טאבון ופינת מדורה, נופים קסומים. לפרטים 0523777810',
    start_date=datetime.date(2021, 12, 5),
    end_date=datetime.date(2021, 12, 6),
    price=[],
    location='')

test12 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='היי מה שלומכם? :)\nמי שרוצה *סאבלט*\nבדירה מהממת ליד שוק התקווה,\n\nדירה מדהימה ברחוב ברכיה 22 ,\n'
         'במרחק הליכה מכם תוכלו ליהנות מהשוק המהמם, '
         'מבתי קפה ומסעדה מעולים במחירים מסובסדים, וכמובן לטייל וליהנות ברחוב האצ״ל, שידוע בתור רחוב מלא מקומות בילוי.\n\n'
         'דירת 2 חדרים (חדר שינה וסלון) 28-30 מ"ר בערך ומרפסת.\n\nבדירה יש הכל !!\n'
         'היא מרוהטת לגמרי עם אינטרנט, טלוויזיה חכמה וכל דבר שתצטרכו כדי שיהיה לכם הכי כיף בעולם.\n\n'
         '4,500 כולל הכל - לא צריך להביא כלום לדירה חוץ מבגדים.\n\nדברו איתי - 0505290072',
    start_date=None,
    end_date=None,
    price=[4500],
    location='תל אביב')

test13 = Test(
    post_time=datetime.date(2021, 11, 13),
    text='סאבלט – דירה מדהימה בתל אביב על חוף הים!\nBeautiful apartment in Tel-Aviv on the beach!\n\n'
         'מסאבלט דירת 2 חדרים במתחם בית מנדרין (בית מלון לשעבר), קומה 8, צפון ת"א, רח\' יוניצמן 21,\n'
         'בתאריכים 20/11 - 16/11\n- מרפסת שמש ענקית לאורך כל הדירה עם נוף לים עוצר נשימה\n- חדר אמבטיה נפרד\n'
         '- מיטה זוגית בחדר שינה + ספה נפתחת למיטה זוגית בסלון + שני מזרנים עבים ונוחים נוספים\n'
         '- מיזוג מרכזי מפוצל לכל חדר בנפרד\n- חניה בשפע\n- חוף ים מתחת לבית, אחד היפים בארץ עם בתי קפה פתוחים עד הלילה\n'
         '- במתחם בית קולנוע "לב"\n- שומר בלובי הכניסה\n- מסעדה ומיני קניון בקומת קרקע\n'
         '- המחיר ללילה 350 ש"ח, בתנאי הזמנת כל התקופה (4 לילות)\n- המחיר הרגיל 490 ש"ח ללילה\n'
         'לפרטים נוספים נא לפנות בפרטי, או בנייד 054-4514010, או במייל mr.chechel@gmail.com\n\n'
         'Subletting my 1 bedroom + living room apartment in the Mandarin building (used to be a hotel), '
         '8-th floor, Yonizman st. 21,\nbetween 16/11 - 20/11.\nIn the flat:\n- huge balcony with sea view\n'
         '- bathroom\n- double bed in the bedroom + sofa bed for a double bed in the living room + two more comfortable mattresses\n-'
         ' central air condition\n- parking for free\n- beach under the house, one of the most beautiful with cafes open until night\n'
         'In the building:\n- cinema, restaurants, and a small mall.\nThe price:\n- The price per night is 350 NIS'
         ', provided you book the entire period (5 nights).\n- The normal price - 490 NIS per night.\n'
         'Michael +972-54-4514010, mr.chechel@gmail.com',
    start_date=datetime.date(2021, 11, 16),
    end_date=datetime.date(2021, 11, 20),
    price=[350, 490],
    location='תל אביב')

test14 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='דופלקס על הים בעכו\nפנוי חמשושים(חמישי שישי שבת)\nבחנוכה פנוי מה2/12 עד ה10/12\nמתאים לזוג משפחה או קבוצה קטנה',
    start_date=datetime.date(2021, 12, 2),
    end_date=datetime.date(2021, 12, 10),
    price=[],
    location='עכו')

test15 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='רעות פרג\'ון\n\u200f8 בנובמבר\u200f ב-\u200f22:23\u200f ·\n\nמפרסמת עבור חברים שלנו.\n\n'
         'חופשת חנוכה בעמק הכי יפה בעולם! עמק המעיינות- בית שאן'
         '.\n\nבתאריכים: כ"ז-ל\' כסליו (1-4/12/21)\n\nבית קו אחרון לנוף משגע! הליכה ברגל מהמפלים הלבנים! מרחק של דק\' '
         'נסיעה מהאסי, עין הנציב, נחל הקיבוצים ועוד.. 25 דק\' מהכינרת!\n\nבית מרווח: 7 חדרים, 3 שירותים, 3 מקלחות, '
         'חצר ענקית עם אטרקציות לילדים, פינת מנגל ועוד.\n\nלפרטים- 050-7998852',
    start_date=datetime.date(2021, 12, 1),
    end_date=datetime.date(2021, 12, 4),
    price=[],
    location='בית שאן')

test16 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='הבית הצבעוני באניעם פתוח לחנוכה!!!\nאנחנו מפנים את הבית המפנק שלנו, שממוקם במרכז הגולן המושב אניעם, '
         'ל 12 יום רצוף!! החל מסוף השבוע ב 25 לנובמבר עד ל 6 בדצמבר נר שמיני.\n*פנוי עדיין 25-29 לנובמבר ו 4-6 לדצמבר '
         'למי שרוצה לטייל בגולן בימי החופשה.\nבית גדול שמתאים לשתיים שלוש משפחות ומותאם'
         ' לילדים! ניתן להלין ברווחה 12 איש ואנחנו גמישים לקבל גם יותר במידת הצורך.\nיש שלושה חדרי שינה, ועוד מרחבים משותפים נוספים'
         ' בהם ניתן לשים מזרנים במידת הצורך.\nמאות כבר התארחו אצלנו וכולם רצו עוד....\nמטבח גדול ,מאובזר ומפנק.\nסלון ופינת אוכל'
         '.\nחדר משחקים לקטנטנים וחדר נינג\'ה לילדים גדולים יותר.\nחצר גדולה, שתי מרפסות, פינת מדורה, '
         'לול תרנגולות (אפשר להוציא ביצה אורגנית לחביתה בבוקר).\nהמיקום אידאלי '
         'לטיולים, מקורות מים מגוונים במרחק קצר וגם בטווח הליכה.\n'
         'המחיר ללילה 1400 ש"ח (מינימום 2 לילות), הנחה למי שיקח 3 לילות ומעלה\n'
         'לתמונות נוספות, פרטים ושאלות\nגיא שקד\n0528544318\nבבקשה להתקשר או לשלוח וואטסאפ. המסנג\'ר לא מתקשר איתי בצורה מיטבית.',
    start_date=datetime.date(2021, 11, 25),
    end_date=datetime.date(2021, 11, 29),  # TODO [AA] : add 4-6.12 when changing start,end date into list
    price=[1400],
    location='אניעם')

test17 = Test(
    post_time=datetime.date(2021, 11, 9),
    text='לספונטניים ומהירי החלטה!!!\nמסבלטת את דירתי הקסומה שממוקמת בנהריה על חוף הים בחמשו"ש הקרוב, 11-13.11.\n'
         'הדירה מתאימה לזוגות או יחידים בלבד.\nלפרטים נוספים אנא פנו בפרטי (לא תמיד רואה תגובות עמכם הסליחה)!',
    start_date=datetime.date(2021, 11, 11),
    end_date=datetime.date(2021, 11, 13),
    price=[],
    location='נהריה')

test18 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='סאבלט , דירת שני חדרים מקסימה בזיכרון יעקב\nמסבלטת את ביתי בקצה זיכרון\n'
         'הדירה מעוצבת ומרוהטת לחלוטין עם מטבח מאובזר ומרפסת שמשקיפה לנוף יפיפיה של רמת הנדיב והים.\n'
         'פנויה מה 1 לדצמבר למינמום של ארבעה עד שישה חודשים עם אופציה להארכה\n'
         'מחיר ללא חשבונות : 2800 ש"ח + 500 לועד בית (בניין נקי, שקט ומאובטח עם מעלית)\nלפרטים ויצירת קשר\nאניטה : 0586694555',
    start_date=datetime.date(2021, 12, 1),
    end_date=datetime.date(2022, 6, 1),
    price=[2800],
    location='זכרון יעקב')

test19 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='אידיאלי לעובדים באיזור, למטיילי "ים אל ים", רוכבי אופניים ומשפחות מטיילים בגליל.\n'
         'בחיק הטבע בלב הגליל המערבי מעל שמורת נחל כזיב/עין חרדלית. לינה במבנה דום מיוחד בחורש טבעי. 400 ש"ח ללילה לעד 4 אורחים.'
         '\nהדום מתאים ללינה של עד 10 אורחים, בחלל התחתון ובגלריה.\n'
         'הדום ממוזג, יש בו שרותים/מקלחת מרווחים, מטבח עם כיריים גז, מקרר ופינת קפה. 2 מחבתות ו 2 סירים כוסות וכלי אוכל.\n\n'
         'דודו 050-5307753 https://www.facebook.com/TheDomeInManot\n\nהדום הגיאודזי במנות',
    start_date=None,
    end_date=None,
    price=[400],
    location='כזיב')

test20 = Test(
    post_time=datetime.date(2021, 11, 15),
    text='*בית בחנוכה עם בריכה חמה בשבילכם!*\nאז שעון חורף איתנו, ואנחנו מתחילים להרגיש את חנוכה ואת מסע החורף שלנו!\nמה שאומר שהבית שלנו מתפנה בשבילכם'
         '!\nהבית שלנו נמצא במושב שתולה שבגליל המערבי, באחד האזורים היפים בארץ!\n'
         '5 חדרי שינה (מתוכם 3 יחידות הורים עם שירותים ומקלחת), סלון ומטבח מרווחים, חצר גדולה עם טרמפולינה.\n'
         'והכי חשוב - בריכה חמה פנימית מתחת לבית!\nתאריכים אפשריים - החל מיום חמישי כ"א כסלו 25/11, ועד מוצ"ש ז\' טבת 11/12 (מינימום 2 לילות)\n'
         '1500-2200 ש"ח ללילה (מחיר גמיש לפי מספר הלילות)\nלפרטים נוספים בלינק בתגובה הראשונה או בטלפון 054-3286986',
    start_date=datetime.date(2021, 11, 25),
    end_date=datetime.date(2021, 12, 11),
    price=[1500, 2200],
    location='שתולה')

test21 = Test(
    post_time=datetime.date(2021, 11, 15),
    text="SUBLET FOR 3 MONTHS \\\\ 1.5 ROOMS FLAT \\\\CITY CENTER",
    start_date=None,
    end_date=None,
    price=None,
    location='תל אביב')
