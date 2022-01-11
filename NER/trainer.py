import numpy as np
import torch
from datasets import load_metric
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
from transformers import BertTokenizerFast
from transformers import DataCollatorForTokenClassification

import NER.ner_tokens as get_tokens

#
print(torch.cuda.is_available())
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
assert len(label_list) == len(label_encoding_dict)
task = "ner"
model_checkpoint = "onlplab/alephbert-base"
batch_size = 16

tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)


def tokenize_and_align_labels(examples):
    label_all_tokens = True
    tokenized_inputs = tokenizer(list(examples["tokens"]), truncation=True, is_split_into_words=True)

    labels = []
    for i, label in enumerate(examples[f"{task}_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            # Special tokens have a word id that is None. We set the label to -100 so they are automatically
            # ignored in the loss function.
            if word_idx is None:
                label_ids.append(-100)
            elif label[word_idx] == '0':
                label_ids.append(0)
            # We set the label for the first token of each word.
            elif word_idx != previous_word_idx:
                label_ids.append(label_encoding_dict[label[word_idx]])
            # For the other tokens in a word, we set the label to either the current label or -100, depending on
            # the label_all_tokens flag.
            else:
                label_ids.append(label_encoding_dict[label[word_idx]] if label_all_tokens else -100)
            previous_word_idx = word_idx

        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


train_dataset, test_dataset = get_tokens.get_un_token_dataset('NER/splits/train/',
                                                              'NER/splits/dev/')

train_tokenized_datasets = train_dataset.map(tokenize_and_align_labels, batched=True)
test_tokenized_datasets = test_dataset.map(tokenize_and_align_labels, batched=True)
model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=len(label_list))

args = TrainingArguments(
    f"test-{task}",
    evaluation_strategy="steps",
    eval_steps=400,
    learning_rate=1e-4,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=3,
    weight_decay=0.00001,
)

data_collator = DataCollatorForTokenClassification(tokenizer)
metric = load_metric("seqeval")


def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    # Remove ignored index (special tokens)
    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }


trainer = Trainer(
    model,
    args,
    train_dataset=train_tokenized_datasets,
    eval_dataset=test_tokenized_datasets,
    data_collator=data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

trainer.train()

trainer.evaluate()

trainer.save_model('hebrew-ner.model')
