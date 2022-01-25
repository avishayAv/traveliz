import torch
from transformers import BertTokenizerFast, AutoModelForTokenClassification

from NER.labels_list import inversed_label_encoding_dict, label_list

tokenizer = BertTokenizerFast.from_pretrained("onlplab/alephbert-base")

paragraph = '''הבית הצבעוני באניעם פתוח לחנוכה!!!
אנחנו מפנים את הבית המפנק שלנו, שממוקם במרכז הגולן המושב אניעם, ל 12 יום רצוף!! החל מסוף השבוע ב 25 לנובמבר עד ל 6 בדצמבר נר שמיני.
*פנוי עדיין 25-29 לנובמבר ו 4-6 לדצמבר למי שרוצה לטייל בגולן בימי החופשה.
בית גדול שמתאים לשתיים שלוש משפחות ומותאם לילדים! ניתן להלין ברווחה 12 איש ואנחנו גמישים לקבל גם יותר במידת הצורך.
יש שלושה חדרי שינה, ועוד מרחבים משותפים נוספים בהם ניתן לשים מזרנים במידת הצורך.
מאות כבר התארחו אצלנו וכולם רצו עוד....
מטבח גדול ,מאובזר ומפנק.
סלון ופינת אוכל.
חדר משחקים לקטנטנים וחדר נינג'ה לילדים גדולים יותר.
חצר גדולה, שתי מרפסות, פינת מדורה, לול תרנגולות (אפשר להוציא ביצה אורגנית לחביתה בבוקר).
המיקום אידאלי לטיולים, מקורות מים מגוונים במרחק קצר וגם בטווח הליכה.
המחיר ללילה 1400 ש"ח (מינימום 2 לילות), הנחה למי שיקח 3 לילות ומעלה
לתמונות נוספות, פרטים ושאלות
גיא שקד
0528544318
בבקשה להתקשר או לשלוח וואטסאפ. המסנג'ר לא מתקשר איתי בצורה מיטבית.
'''
paragraph2 = '''מסאבלטת את דירתי בקיבוץ דפנה, הקיבוץ הכי יפה בצפון
דירת שני חדרים משופצת, נקיה ויפה. דקת הליכה מהנחל.
בתאריכים 11-14.11
0509100671 שני

זורמת גם עם החלפת דירות בתל אביב'''
paragraph3 = '''מי רוצה לגור בבית פרטי ישן וטוב, ב... תל אביב!!! (דרום יד אליהו),
מה 15/11 עד ל 08/12?
תהיה גם חתולה מהממת שדי שומרת על עצמה... חיזרו אלי בפרטי'''
for par in [paragraph, paragraph2, paragraph3]:
    tokens = tokenizer(par)
    torch.tensor(tokens['input_ids']).unsqueeze(0).size()

    model = AutoModelForTokenClassification.from_pretrained('/home/dsi/shaya/traveliz/hebrew-sublet.model',
                                                            num_labels=len(label_list))
    predictions = model.forward(input_ids=torch.tensor(tokens['input_ids']).unsqueeze(0),
                                attention_mask=torch.tensor(tokens['attention_mask']).unsqueeze(0))
    predictions = torch.argmax(predictions.logits.squeeze(), axis=1)
    predictions = [inversed_label_encoding_dict[i.item()] for i in predictions]

    words = tokenizer.batch_decode(tokens['input_ids'])
    for w, p in zip(words, predictions):
        print(f"word {w}, prediction {p}")
# print(tokens['input_ids'])
# print(words)
# print(predictions)
# pd.DataFrame({'ner': predictions, 'words': words}).to_csv('hebrew_ner.csv')
