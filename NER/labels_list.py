label_list = ['O', 'I-DATE', 'S-DATE', 'B-DATE', 'E-DATE', 'I-LOC', 'S-LOC', 'B-LOC', 'E-LOC', 'I-MONEY', 'S-MONEY',
              'B-MONEY', 'E-MONEY', 'I-ORG', 'S-ORG', 'B-ORG', 'E-ORG', 'I-PER', 'S-PER', 'B-PER', 'E-PER', 'I-PERCENT',
              'S-PERCENT', 'B-PERCENT', 'E-PERCENT', 'I-TIME', 'S-TIME', 'B-TIME', 'E-TIME', 'I-WOA', 'S-WOA', 'B-WOA',
              'E-WOA', 'I-EVE', 'S-EVE', 'B-EVE', 'E-EVE', 'I-FAC', 'S-FAC', 'B-FAC', 'E-FAC', 'I-DUC', 'S-DUC',
              'B-DUC', 'E-DUC', 'I-ANG', 'S-ANG', 'B-ANG', 'E-ANG', 'B-HLOC', 'I-HLOC', 'E-HLOC', 'B-NLOC', 'I-NLOC',
              'E-NLOC',
              'B-ROOMS', 'I-ROOMS', 'E-ROOMS', 'B-MONEY-TYPE', 'I-MONEY-TYPE', 'E-MONEY-TYPE', 'B-CAPACITY',
              'I-CAPACITY', 'E-CAPACITY',
              'B-DURATION', 'I-DURATION', 'E-DURATION']
label_encoding_dict = {'O': 0, 'I-DATE': 1, 'S-DATE': 2, 'B-DATE': 3, 'E-DATE': 4, 'I-LOC': 5, 'S-LOC': 6, 'B-LOC': 7,
                       'E-LOC': 8, 'I-MONEY': 9, 'S-MONEY': 10, 'B-MONEY': 11, 'E-MONEY': 12, 'I-ORG': 13, 'S-ORG': 14,
                       'B-ORG': 15, 'E-ORG': 16, 'I-PER': 17, 'S-PER': 18, 'B-PER': 19, 'E-PER': 20, 'I-PERCENT': 21,
                       'S-PERCENT': 22, 'B-PERCENT': 23, 'E-PERCENT': 24, 'I-TIME': 25, 'S-TIME': 26, 'B-TIME': 27,
                       'E-TIME': 28, 'I-WOA': 29, 'S-WOA': 30, 'B-WOA': 31, 'E-WOA': 32, 'I-EVE': 33, 'S-EVE': 34,
                       'B-EVE': 35, 'E-EVE': 36, 'I-FAC': 37, 'S-FAC': 38, 'B-FAC': 39, 'E-FAC': 40, 'I-DUC': 41,
                       'S-DUC': 42, 'B-DUC': 43, 'E-DUC': 44, 'I-ANG': 45, 'S-ANG': 46, 'B-ANG': 47, 'E-ANG': 48,
                       'B-HLOC': 49, 'I-HLOC': 50, 'E-HLOC': 51, 'B-NLOC': 52, 'I-NLOC': 53, 'E-NLOC': 54,
                       'B-ROOMS': 55, 'I-ROOMS': 56, 'E-ROOMS': 57, 'B-MONEY-TYPE': 58, 'I-MONEY-TYPE': 59,
                       'E-MONEY-TYPE': 60,
                       'B-CAPACITY': 61, 'I-CAPACITY': 62, 'E-CAPACITY': 63, 'B-DURATION': 64, 'I-DURATION': 65,
                       'E-DURATION': 66}
intent_to_encoding = {'renting': 0, 'looking': 1, 'replace': 2, 'JUNK': 3}

inversed_label_encoding_dict = {v: k for k, v in label_encoding_dict.items()}
