# ................................dictionary..............................
import os
import numpy as np
import random
from sacremoses import MosesTokenizer
#https://github.com/wanchichen/GA-Text-Summarization/blob/main/src/vocab_1000.txt

# read from txt
# and create dictionary

def read_vocab(num):
    dictionary = list()
    with open(f"{num}.txt", "r", encoding='utf-8') as in_file:
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
def gen_example(tag , event, malicous):
    return tags[0]+" "+event[0]+malicous[0]+">"

# build_vocab()
event = read_vocab("event")
tags= read_vocab("tag")
malicous = read_vocab("malicous")
# print(event)
# print(tags)
# print(malicous)

# print(gen_example(tags,event, malicous))


class grammer:
     def __init__(self):
        self.texts = "abc"
        self.spaces = ' ' 
        self.events = read_vocab("event")
        self.asigns =  ['=']
        self.payloads = read_vocab("malicous")
        self.closers = ['>','">',"'>","/>"]
        self.tags = read_vocab("tag")
        self.data = [self.texts,self.spaces,self.events,self.payloads,self.tags,self.closers]

     def get_simple_payload(self):
        # print(type(self.tags))
        payload = random.choice(self.tags) +self.spaces+ random.choice(self.events)+random.choice(self.payloads)+random.choice(self.closers)
        return payload
     
# p = grammer()
# print(p.events)