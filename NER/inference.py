import torch
from transformers import BertTokenizerFast, AutoModelForTokenClassification

label_list = ['O', 'I-DATE', 'S-DATE', 'B-DATE', 'E-DATE', 'I-LOC', 'S-LOC', 'B-LOC', 'E-LOC', 'I-MONEY', 'S-MONEY',
              'B-MONEY', 'E-MONEY', 'I-ORG', 'S-ORG', 'B-ORG', 'E-ORG', 'I-PER', 'S-PER', 'B-PER', 'E-PER', 'I-PERCENT',
              'S-PERCENT', 'B-PERCENT', 'E-PERCENT', 'I-TIME', 'S-TIME', 'B-TIME', 'E-TIME', 'I-WOA', 'S-WOA', 'B-WOA',
              'E-WOA', 'I-EVE', 'S-EVE', 'B-EVE', 'E-EVE', 'I-FAC', 'S-FAC', 'B-FAC', 'E-FAC', 'I-DUC', 'S-DUC',
              'B-DUC', 'E-DUC', 'I-ANG', 'S-ANG', 'B-ANG', 'E-ANG']
label_encoding_dict = {'O': 0, 'I-DATE': 1, 'S-DATE': 2, 'B-DATE': 3, 'E-DATE': 4, 'I-LOC': 5, 'S-LOC': 6, 'B-LOC': 7,
                       'E-LOC': 8, 'I-MONEY': 9, 'S-MONEY': 10, 'B-MONEY': 11, 'E-MONEY': 12, 'I-ORG': 13, 'S-ORG': 14,
                       'B-ORG': 15, 'E-ORG': 16, 'I-PER': 17, 'S-PER': 18, 'B-PER': 19, 'E-PER': 20, 'I-PERCENT': 21,
                       'S-PERCENT': 22, 'B-PERCENT': 23, 'E-PERCENT': 24, 'I-TIME': 25, 'S-TIME': 26, 'B-TIME': 27,
                       'E-TIME': 28, 'I-WOA': 29, 'S-WOA': 30, 'B-WOA': 31, 'E-WOA': 32, 'I-EVE': 33, 'S-EVE': 34,
                       'B-EVE': 35, 'E-EVE': 36, 'I-FAC': 37, 'S-FAC': 38, 'B-FAC': 39, 'E-FAC': 40, 'I-DUC': 41,
                       'S-DUC': 42, 'B-DUC': 43, 'E-DUC': 44, 'I-ANG': 45, 'S-ANG': 46, 'B-ANG': 47, 'E-ANG': 48}
inversed_label_encoding_dict = {v: k for k, v in label_encoding_dict.items()}
tokenizer = BertTokenizerFast.from_pretrained("onlplab/alephbert-base")

paragraph = '''אנחנו מפנים את הבית המפנק שלנו, שממוקם במרכז הגולן המושב אניעם, ל 12 יום רצוף!! החל מסוף השבוע ב 25 לנובמבר עד ל 6 בדצמבר נר שמיני.
'''
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
