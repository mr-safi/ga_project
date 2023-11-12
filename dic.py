# ................................dictionary..............................
import os
import numpy as np
from sacremoses import MosesTokenizer
#https://github.com/wanchichen/GA-Text-Summarization/blob/main/src/vocab_1000.txt

# read from txt
# and create dictionary

def read_vocab(num):
    dictionary = list()
    with open(f"vocab_{num}.txt", "r", encoding='utf-8') as in_file:
        vocab_lines = in_file.readlines()

        for line in vocab_lines:
            dictionary.append(line.rstrip())

    return dictionary


def build_vocab(num):
    vocab_file = f"vocab_{num}.txt"
    vocab_list = list()
    tokenizer = MosesTokenizer(lang='en')

    i = 0
    for file in os.listdir("dataset/train/body"):
        filename = os.fsdecode(file)

        with open(f"dataset/train/body/{filename}", 'r', encoding='utf-8') as in_file:
            corpus_lines = in_file.readlines()
            corpus_lines = tokenizer.tokenize(corpus_lines)

            for line in corpus_lines:
                for word in line.split():
                    if word.lower() not in vocab_list:
                        vocab_list.append(word.lower())

        i += 1
        if i >= 1000:
            break

    with open(vocab_file, 'w', encoding='utf-8') as out_file:
        for word in vocab_list:
            out_file.write(f"{word}\n")


def create_dictionary(words, weights):
    dictionary = {}
    for i in range(len(words)):
        dictionary[words[i]] = weights[i]

    return dictionary

# build_vocab()
# print(read_vocab(1000))