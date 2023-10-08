import json

import openai
import tiktoken
import pandas as pd
import numpy as np

from config import OPENAI_API_KEY, MAX_TOKENS

openai.api_key = OPENAI_API_KEY


def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


with open('../files_for_model_training/input_faq.json', encoding="utf-8") as input_faq:
    file_contents = input_faq.read()

column_names = {
    "question": [
        "Question_short",
        "Question_original",
        "Keywords",
        "Question_original_alternatives",
        "Question_short_alternatives",
    ],
    "answer": ["Answer_plain_text", "Answer_original", "Notes"],
}


parsed_json = json.loads(file_contents)

texts = []

for item in parsed_json:
    row = ()
    for column_name in column_names.keys():
        value = ""
        for field_name in column_names[column_name]:
            item_value = item[field_name]
            if type(item_value) == list:
                value += ". ".join(item_value)
            else:
                value += item_value
        row += (value, )

    texts.append(row)

df = pd.DataFrame(texts, columns=['title', 'text'])
df['text'] = df.title + ". " + remove_newlines(df.text)
df.to_csv('../files_for_model_training/scraped.csv')
df.head()

tokenizer = tiktoken.get_encoding("cl100k_base")

df = pd.read_csv('../files_for_model_training/scraped.csv', index_col=0)
df.columns = ['title', 'text']

df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))


def split_into_many(text, max_tokens=MAX_TOKENS):
    sentences = text.split('. ')

    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        if token > max_tokens:
            continue

        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


shortened = []

for row in df.iterrows():
    if row[1]['n_tokens'] > MAX_TOKENS:
        shortened += split_into_many(row[1]['text'])
    else:
        shortened.append(row[1]['text'])

df = pd.DataFrame(shortened, columns=['text'])
df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

df['embeddings'] = df.text.apply(
    lambda x: openai.Embedding.create(input=x, engine="text-embedding-ada-002")['data'][0]['embedding']
)

df.to_csv('../files_for_model_training/embeddings.csv')
df.head()


df = pd.read_csv('../files_for_model_training/embeddings.csv', index_col=0)
df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)
df.head()
