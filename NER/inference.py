import torch
from transformers import BertTokenizerFast, AutoModelForTokenClassification

label_list = ['I-DATE', 'S-DATE', 'B-DATE', 'E-DATE', 'I-LOC', 'S-LOC', 'B-LOC', 'E-LOC', 'I-MONEY', 'S-MONEY',
              'B-MONEY', 'E-MONEY', 'I-ORG', 'S-ORG', 'B-ORG', 'E-ORG', 'I-PER', 'S-PER', 'B-PER', 'E-PER', 'I-PERCENT',
              'S-PERCENT', 'B-PERCENT', 'E-PERCENT', 'I-TIME', 'S-TIME', 'B-TIME', 'E-TIME', 'O']
label_encoding_dict = {'O': 0, 'I-DATE': 1, 'S-DATE': 2, 'B-DATE': 3, 'E-DATE': 4, 'I-LOC': 5, 'S-LOC': 6, 'B-LOC': 7,
                       'E-LOC': 8, 'I-MONEY': 9, 'S-MONEY': 10, 'B-MONEY': 11, 'E-MONEY': 12, 'I-ORG': 13, 'S-ORG': 14,
                       'B-ORG': 15, 'E-ORG': 16, 'I-PER': 17, 'S-PER': 18, 'B-PER': 19, 'E-PER': 20, 'I-PERCENT': 21,
                       'S-PERCENT': 22, 'B-PERCENT': 23, 'E-PERCENT': 24, 'I-TIME': 25, 'S-TIME': 26, 'B-TIME': 27,
                       'E-TIME': 28}
inversed_label_encoding_dict = {v: k for k, v in label_encoding_dict.items()}
tokenizer = BertTokenizerFast.from_pretrained("onlplab/alephbert-base")

paragraph = '''בת-ים, קרוב מאוד לחוף הים ולתל-אביב, סטודיו משופצת ומצוידת בכל,
2900 ₪ כולל כל ההוצאות לתקופה ארוכה
לתקופות קצרות:
400 ₪ ליומיים, 1200 ₪ לשבוע, 3500 ₪ לחודש כולל הוצאות . 3 מקומות לינה – זוגי ומיטת גלריה'''
tokens = tokenizer(paragraph)
torch.tensor(tokens['input_ids']).unsqueeze(0).size()

model = AutoModelForTokenClassification.from_pretrained('hebrew-ner.model', num_labels=len(label_list))
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
