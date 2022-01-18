import torch
from transformers import BertTokenizerFast, AutoModelForTokenClassification

from NER.labels_list import inversed_label_encoding_dict

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
