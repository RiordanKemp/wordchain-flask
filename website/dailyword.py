import random
import os
import os.path
import re
import csv

already_used_set = set()

daily_word = ""
alphabet_dict = {}
words_dict = {}
numb_dict = {}
starting_words_set = set()
valid_letters_dict = {}

directory_str = "website/dict_directory"


test_int = 0
def random_int():
    test_int = random.randrange(1, 10)
    return test_int
test_int = random_int()


def open_files():
    readers_list = []

    for file in os.listdir(directory_str):
        filename = os.fsdecode(file)

        file_path = os.path.join(directory_str, filename)
        file_reader = open(file_path, 'r')
        csv_reader = csv.reader(file_reader)
        readers_list.append(csv_reader)

    return readers_list

def organize_dictionary(filereader_list):


    for reader in filereader_list:
        line_count = 0
        for line in reader:
            line_count += 1

            if (line_count == 1):
                line_str = ' '.join(line)
                letter_key = line_str[0]
                #print("line str:", line_str, "line:", line)
                #print("line_str[0]:", line_str[0])
                #print("letter key:", letter_key)

            if (line_count % 2 == 1 and line_count != 1):
                line_str = ' '.join(line)
                split_line = line_str.split()
                word_key = split_line[0]
                word_key = re.sub(r'[^a-zA-Z0-9]', '', word_key)
                word_def = ' '.join(split_line[1::])
                word_addition(word_key, word_def, letter_key)

def word_addition(word_key, word_def, letter_key):
    vowels = "a", "e", "i", "o", "u", 
    if len(word_key) < 3:
        return

    if letter_key not in alphabet_dict:
        alphabet_dict[letter_key] = words_dict

    if word_key not in alphabet_dict[letter_key]:
        alphabet_dict[letter_key][word_key] = word_def

    else:
        marked_def = "1581199358571" + word_def
        alphabet_dict[letter_key][word_key] += marked_def
        numb_dict[word_key] = 1

    if len(word_key) > 8:
        unique_vowel = ""
        uv_count = 0
        for letter in word_key:
            if letter.lower() in vowels and letter.lower() not in unique_vowel:
                unique_vowel += letter.lower()
                uv_count += 1

        if (uv_count > 1):
            starting_words_set.add(word_key)

def org_files():
    readers_list = open_files()
    organize_dictionary(readers_list)
    daily_words_set = starting_words_set.difference(already_used_set)
    parent_word = random.choice(list(daily_words_set))
    already_used_set.add(parent_word)

    letter = parent_word[0]
    definition = alphabet_dict[letter][parent_word]

    if parent_word in numb_dict.keys():
        definition = definition.split('1581199358571')
        definition = '<br> '.join(definition)
        word_str = f"This word has multiple definitions:<br>{definition}"

    else:
        word_str = f"This word has one definition:<br>{definition}"
    return parent_word, word_str

def create_valid_letters_dict(word):
    valid_letters_dict = {}
    for character in word:
        character = character.lower()
        if character not in valid_letters_dict:
            valid_letters_dict[character] = 0
        valid_letters_dict[character] += 1
        
    return valid_letters_dict

daily_word, definition = org_files()
valid_letters_dict = create_valid_letters_dict(daily_word)






