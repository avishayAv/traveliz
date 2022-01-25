import itertools
import json
import os

import nltk
import pandas as pd
from datasets import Dataset

from NER.labels_list import label_list

nltk.download('punkt')

def get_tokens_and_ner_tags(filename):
    if filename.endswith('bmes'):
        with open(filename, 'r', encoding="utf8") as f:
            lines = f.readlines()
            split_list = [list(y) for x, y in itertools.groupby(lines, lambda z: z == '\n') if not x]
            tokens = [[x.split()[0] for x in y] for y in split_list]
            entities = [[x.split()[1].replace(',', '') for x in y] for y in split_list]
        return pd.DataFrame({'tokens': tokens, 'ner_tags': entities, 'intents': [None for _ in tokens]})
    elif filename.endswith('json'):
        data = json.load(open(filename, 'rb'))['rasa_nlu_data']['common_examples']
        if 'eliya' in filename:  # TODO [YG]: remove
            data = data[7:]
        all_tokens = []
        all_entities = []
        intents = []

        for sample in data:
            offset = 0
            tokens = nltk.word_tokenize(sample['text'])
            entities = []
            for entity in sample['entities']:

                if 'B-' + entity['entity'] not in label_list:
                    raise Exception(f'entity not supported {entity["entity"]} {sample["text"]}')
                entity_len = len(nltk.word_tokenize(entity['value']))
                entity['prefixes'] = ['B']
                if entity_len > 2:
                    entity['prefixes'] += ['I'] * (entity_len - 2)
                if entity_len > 1:
                    entity['prefixes'] += ['E']
                entity['start'] -= 1
                entity['end'] -= 1
            for token in tokens:
                start = sample['text'].find(token, offset)
                end = start + len(token)
                offset = end
                flag = False
                for entity in sorted(sample['entities'], key=lambda x: x['start']):
                    if not (end <= entity['start'] or start >= entity['end']):
                        if entity['prefixes']:
                            entities.append(entity['prefixes'].pop(0) + '-' + entity['entity'])
                            flag = True
                            break
                if not flag:
                    entities.append('O')
            intents.append(sample['intent'])
            all_tokens.append(tokens)
            all_entities.append(entities)
        return pd.DataFrame({'tokens': all_tokens, 'ner_tags': all_entities, 'intents': intents})
    else:
        raise Exception('unsupported tagging format')


def get_all_tokens_and_ner_tags(directory):
    return pd.concat([get_tokens_and_ner_tags(os.path.join(directory, filename)) for filename in
                      os.listdir(directory)]).reset_index().drop('index', axis=1)


def get_un_token_dataset(train_directory, test_directory):
    train_df = get_all_tokens_and_ner_tags(train_directory)
    test_df = get_all_tokens_and_ner_tags(test_directory)
    train_dataset = Dataset.from_pandas(train_df)
    test_dataset = Dataset.from_pandas(test_df)

    return (train_dataset, test_dataset)
