import scipy, os, re
import numpy as np
import pickle as pkl
from langNode import LangNode

# Parses each word from the pertinent text file
def extract_words(text):
    words = [word[word.rfind(' ') + 1:] for word in re.split(r'/\w\w', text)]
    words = [word[word.rfind('\n') + 1:] for word in words]
    words = [word[word.rfind('\t') + 1:] for word in words]
    return words

# Main function
def word_map2(dir='corpus', targets='abcdefghijklmnopqrstuvwxyz1234567890'):
    try:
        char_map = scipy.io.loadmat('model.mat')
        return char_map
    except:
        pass
    try:
        file = open("wordmap2_model",'rb')
        char_map = pkl.load(file)
        file.close()
        return char_map
    except Exception as e:
        print('No map.mat file found. Creating file')
        char_map = {}
        files = [file for file in os.listdir(dir) if file[0] == 'c']
        szFile = {}

        for i in range(len(files)):
            string = dir + '/' + str(files[i][:])
            szFile[str(i)] = string.strip()

        for i in range(len(szFile)):
            if re.search(r'c\w\d\d', files[i]):
                fid = open(szFile[str(i)])
                text = fid.read()
                words = extract_words(text)

                for j in range(len(words)):
                    word = words[j]
                    p = ''
                    index = 0
                    for k in range(len(word)):
                        char = word[k]
                        if char in targets:
                            index += 1
                            if index == 1:
                                try:
                                    char_map[''] += 1
                                except:
                                    char_map[''] = 1
                        p = p + char
                        try:
                            char_map[p] += 1
                        except:
                            char_map[p] = 1
    model_file = open('wordmap2_model', 'ab')
    pkl.dump(char_map, model_file)
    model_file.close()

    model = create_model(targets, char_map)

    return model

def find_where_last_char_in_targets(targets, x):
    if len(x) == 0:
        return -1
    for i in range(len(targets)):
        if targets[i] == x[-1]:
            return i
    return -1

def find_if_last_char_in_targets(targets, x):
    return len(x) > 0 and x[-1] in targets

def create_model(targets, model):

    si = targets.index('a')

    root = LangNode(l=si,n=len(targets))

    keySet = list(model.keys())

    keySet = keySet[1:]

    parentKeys = [x[:-1] for x in keySet]

    letters = [find_where_last_char_in_targets(targets, x) for x in keySet]

    nodes = [LangNode(l=letter, n=len(targets)) for letter in letters]

    for i in range(len(nodes)):
        if letters[i] == si:
            nodes[i] = root

    langNodes = {}

    for i in range(len(letters)):
        letter = letters[i]
        #print(letter, si)
        if letter != si:
            langNodes[str(keySet[i])] = nodes[i]

    langNodes[''] = root

    parentNodes = []

    for key in parentKeys:
        try:
            parentNodes.append(langNodes[key])
        except:
            continue

    valid = [find_if_last_char_in_targets(targets, x) for x in keySet]

    for i in range(len(valid)):
        case = valid[i]
        if case:
            try:
                key = keySet[i]
                letter = letters[i]
                parentNode = parentNodes[i]
                node = nodes[i]
                parentNode.totalWeight = parentNode.totalWeight + model[key]
                parentNode.weights[letter] = parentNode.weights[letter] + model[key]
                parentNode.children[letter] = node
            except:
                continue
    model = langNodes
    return model
