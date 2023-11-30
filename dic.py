# ................................dictionary..............................
import os
import numpy as np
import random
from sacremoses import MosesTokenizer


# https://github.com/wanchichen/GA-Text-Summarization/blob/main/src/vocab_1000.txt

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


def gen_example(tag, event, malicous):
    return tags[0] + " " + event[0] + malicous[0] + ">"


# build_vocab()
event = read_vocab("event")
tags = read_vocab("tag")
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
        self.asigns = ['=']
        self.payloads = read_vocab("malicous")
        # self.closers = ['>','">',"'>","/>"]
        self.closers = ['>', '">', "'>"]
        self.tags = read_vocab("tag")
        self.data = [self.texts, self.spaces, self.events, self.payloads, self.tags, self.closers]

    def get_simple_payload(self):
        simple = self.spaces + random.choice(self.events) + random.choice(
            self.payloads) + random.choice(self.closers)
        rnd = random.randint(4, 8)
        rnd = rnd % 4
        if rnd == 1:
            payload = self.p1345textEC()
        elif rnd == 2:
            payload = random.choice(self.tags) + simple
        elif rnd == 3:
            payload=self.p51345()
        else:
            payload = self.nested_tag()

        return payload

    def end_tag(self, tag):

        pl = tag.split("<")
        return "</" + pl[-1] + ">"

    def get_random_txt(self):
        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
        templocal = random.sample(alphabet, random.randint(4, 10))
        templocal = ''.join(map(str, templocal))
        return templocal

    def p1345textEC(self):
        tg = random.choice(self.tags)
        payload = tg + ' ' + random.choice(self.events) + random.choice(
            self.payloads) + ">" + self.get_random_txt() + self.end_tag(tg)
        return payload

    def p51345(self):
        payload = random.choice(self.closers) + random.choice(self.tags) + self.spaces + random.choice(
            self.events) + random.choice(self.payloads) + random.choice(self.closers)
        return payload
    def nested_tag(self):
        tg = random.choice(self.tags)
        pl = tg +'>' +self.p1345textEC()+self.end_tag(tg)
        return pl


# p = grammer()
# print(p.get_simple_payload())
