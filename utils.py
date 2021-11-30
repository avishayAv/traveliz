def remove_time_stamp_from_text(text):
    return '\n'.join([line for line in text.split('\n') if '\u200f' not in line]) # remove RLM (used in facebook for hebrew timestamp)