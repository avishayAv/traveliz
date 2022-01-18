import numpy as np
import torch
from datasets import load_metric
from transformers import AutoModelForTokenClassification, TrainingArguments, Trainer
from transformers import BertTokenizerFast
from transformers import DataCollatorForTokenClassification

import NER.ner_tokens as get_tokens
from NER.labels_list import label_encoding_dict, intent_to_encoding, label_list

print(torch.cuda.is_available())

pretraining = True
task = "ner"
model_checkpoint = "onlplab/alephbert-base"
batch_size = 16

tokenizer = BertTokenizerFast.from_pretrained(model_checkpoint)


def tokenize_and_align_labels(examples):
    label_all_tokens = True
    tokenized_inputs = tokenizer(list(examples["tokens"]), truncation=True, is_split_into_words=True)

    labels = []
    for i, (label, intent) in enumerate(zip(examples[f"{task}_tags"], examples['intents'])):
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
        if intent is not None:
            label_ids[0] = intent_to_encoding[intent]
        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


train_dataset, test_dataset = get_tokens.get_un_token_dataset('NER/splits/sublet_train/',
                                                              'NER/splits/dev/')

train_tokenized_datasets = train_dataset.map(tokenize_and_align_labels, batched=True)
test_tokenized_datasets = test_dataset.map(tokenize_and_align_labels, batched=True)
if pretraining:
    model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=len(label_list))
else:
    model = AutoModelForTokenClassification.from_pretrained('hebrew-ner.model', num_labels=len(label_list))

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
if pretraining:
    trainer.save_model(f'hebrew-ner.model')
else:
    trainer.save_model(f'hebrew-sublet.model')
