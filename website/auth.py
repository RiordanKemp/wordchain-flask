from flask import Flask, redirect, url_for, render_template, request, Blueprint, jsonify

auth = Blueprint('auth', __name__)

openingStr = """Welcome to NAME PENDING (word chain??)!"""
difficultyDetails = "\nHard Mode requires child words to be +-1 in length relative to their parent."
hardmodeEnabled = "\nYou've chosen to play on Hard Mode.  Hard Mode requires child words to be +-1 in length relative to their parent."
exitMessage = "Thanks for playing! Exiting now..."
reset_message = "Resetting the round now.."
input_str = ""

difficultyOnGLOB = False
wordchainGLOB = []
last_wordGLOB = ""

directory_str = "website/dict_directory"

alphabet_dict = {}
words_dict = {}
numb_dict = {}
starting_words_set = set()
already_used_words_set = set()
valid_letters_dict = {}

parent_wordGLOB = ""

import os
import os.path
import re
import csv
import random

@auth.route('/login')
def login():
    return render_template("login.html", passText="Testing", passText2="other", bool = False)

@auth.route('/sign-up')
def signup():
    return render_template("signup.html")

@auth.route('/input', methods=["POST", "GET"])
def input():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("auth.user", usr=user))
    else:
        return render_template("input.html")
    
@auth.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"

@auth.route('/process', methods=['POST'])
def process():
    data = request.form.get('data')
    # process the data using Python code
    result = data.upper()
    return result

@auth.route('/setdifficulty', methods=['POST'])
def difficulty():
    hardmode = request.form.get('hardmode')
    global difficultyOnGLOB
    # process the data using Python code
    if hardmode == "Enabled":
        difficultyOnGLOB = True
    elif hardmode == "Disabled":
        difficultyOnGLOB = False
    return difficultyOnGLOB

@auth.route('/checkdiff', methods=['POST'])
def checkdiff():
    if (difficultyOnGLOB):
        return "T"
    else:
        return "F"
    
@auth.route('/checkchain', methods=['POST'])
def checkchain():
    wordchain = "⫘⫘⫘".join(wordchainGLOB)
    wordchain = f"<b> {wordchain} </b>"
    return wordchain
    

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

@auth.route("/first_word", methods=["POST"])
def first_word():
    input_str = request.form.get('input_str')

    global last_wordGLOB
    global wordchainGLOB

    parent_word = parent_wordGLOB
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nINITIAL WORD\nParent: {}".format(parent_word))

    difficultyOn = difficultyOnGLOB

    input_str = input_str.capitalize()
    print("input str:", input_str)

    if input_str not in words_dict:
        return f"\"{input_str}\"  does not exist."

    if input_str in already_used_words_set:
        print("You already used this word.")
        return ("You already used this word.")

    letter_use_dict = {}
    character_limit_exceeded = False
    invalid_character_used = False
    overused_letter = ""
    invalid_character = ""

    for letter in valid_letters_dict:
        letter_use_dict[letter] = valid_letters_dict[letter]

    for character in input_str:
        character = character.lower()
        print("character:", character, "valid letters dict:", valid_letters_dict)
        if character not in valid_letters_dict:
            invalid_character_used = True
            invalid_character = character
            break
        letter_use_dict[character] -= 1
        print("letter use char:", letter_use_dict[character])
        if (letter_use_dict[character] < 0):
            character_limit_exceeded = True
            overused_letter = character


    if (invalid_character_used):
            print("You used letter \"{}\", which is not part of the parent word.".format(invalid_character.capitalize()))
            return f"You used the letter \"{invalid_character.capitalize()}\", which is not part of the parent word." #+ "| ERROR"

    if (character_limit_exceeded):
            overuse_count = 0
            for letter in input_str:
                if letter.lower() == overused_letter.lower():
                    overuse_count += 1
            print("You used the letter {} {} times, but the maximum is {}.".format(overused_letter, overuse_count, valid_letters_dict[overused_letter]))
            return "You used the letter \"{}\" {} times, but the maximum is {}.".format(overused_letter.capitalize(), overuse_count, valid_letters_dict[overused_letter])

    parent_length = len(parent_word)
    parent_min = str(parent_length - 3)
    parent_max = str(parent_length + 3)

    already_used_words_set.add(input_str)

    wordchainGLOB.append(input_str)
    last_wordGLOB = input_str
    wordchain = "⫘⫘⫘".join(wordchainGLOB)
    wordchain = f"<b> {wordchain} </b>"
    return input_str + "|NOERROR|" + wordchain + "|" + parent_min + "|" + parent_max


@auth.route("/child_word", methods=["POST"])
def child_word():
    input_str = request.form.get('input_str')

    global last_wordGLOB
    global wordchainGLOB

    difficultyOn = difficultyOnGLOB
    parent_word = parent_wordGLOB
    previous_word = last_wordGLOB

    starting_letter = previous_word[-1].capitalize()
    input_str = input_str.capitalize()
    print("input str:", input_str)

    if input_str not in words_dict:
        return f"\"{input_str}\"  does not exist."

    if input_str in already_used_words_set:
        print("You already used this word.")
        return "You already used this word."

    letter_use_dict = {}
    character_limit_exceeded = False
    invalid_character_used = False
    overused_letter = ""
    invalid_character = ""

    for letter in valid_letters_dict:
        letter_use_dict[letter] = valid_letters_dict[letter]

    for character in input_str:
        character = character.lower()
        print("character:", character, "valid letters dict:", valid_letters_dict)
        if character not in valid_letters_dict:
            invalid_character_used = True
            invalid_character = character
            break
        letter_use_dict[character] -= 1
        print("letter use char:", letter_use_dict[character])
        if (letter_use_dict[character] < 0):
            character_limit_exceeded = True
            overused_letter = character
            overuse_count = input_str.replace(character, "")


    if (invalid_character_used):
            print("You used letter \"{}\", which is not part of the parent word.".format(invalid_character.capitalize))
            return f"You used letter {invalid_character}, which is not part of the parent word." #+ "| ERROR"

    if (character_limit_exceeded):
            overuse_count = 0
            for letter in input_str:
                if letter.lower() == overused_letter.lower():
                    overuse_count += 1
            print("Valid letters dict #: {} {}".format(letter, valid_letters_dict[overused_letter]))

            print("You used the letter {} {} times, but the maximum is {}.".format(overused_letter, overuse_count, valid_letters_dict[overused_letter]))
            return ("You used the letter \"{}\" {} times, but the maximum is {}.".format(overused_letter.capitalize(), overuse_count, valid_letters_dict[overused_letter]))

    input_length = len(input_str)
    parent_length = len(parent_word)
    different_length = parent_length - input_length
    print("difficulty on:", difficultyOn, "diff length:", different_length, "input:", input_length)
    if (different_length > 3 or different_length < -3) and difficultyOn:
        print("This word should have {} to {} characters, but it has {} instead.".format(parent_length - 3, parent_length + 3, input_length))
        return "This word should have {} to {} characters, but it has {} instead.".format(parent_length - 3, parent_length + 3, input_length)

    if (input_str[0] != starting_letter):
        print("This word should start with {}, but it starts with {} instead.".format(starting_letter, input_str[0]))
        return "This word should start with {}, but it starts with {} instead.".format(starting_letter, input_str[0])


    already_used_words_set.add(input_str)
    parent_length = len(parent_word)
    parent_min = str(parent_length - 3)
    parent_max = str(parent_length + 3)

    wordchainGLOB.append(input_str)
    last_wordGLOB = input_str
    wordchain = "⫘⫘⫘".join(wordchainGLOB)
    wordchain = f"<b> {wordchain} </b>"
    return input_str + "|NOERROR|" + wordchain + "|" + parent_min + "|" + parent_max




@auth.route("/main", methods=["POST"])
def main(): 
    starting_words_set.clear()
    valid_letters_dict.clear()
    already_used_words_set.clear()

    alphabet_dict.clear()
    words_dict.clear()
    numb_dict.clear()

    difficultyOn = difficultyOnGLOB 
    global last_wordGLOB
    global wordchainGLOB
    global parent_wordGLOB

    wordchainGLOB = []
    last_wordGLOB = ""

    if (difficultyOn):
        difficultyText = "Difficulty: <font color=red><b>HARD</b></font>"
    else:
        difficultyText = "Difficulty: <font color=green><b>NORMAL</b></font>"


    readers_list = open_files()

    organize_dictionary(readers_list)

    parent_word = random.choice(list(starting_words_set))

    parent_wordGLOB = parent_word

    #print("\n~~~~~~~~~~~~~~~~~~~~~~~~~\nThis round's PARENT WORD will be: {}.".format(parent_word))
    for character in parent_word:
        character = character.lower()
        if character not in valid_letters_dict:
            valid_letters_dict[character] = 0
        valid_letters_dict[character] += 1

    already_used_words_set.add(parent_word)

    letter = parent_word[0]
    definition = alphabet_dict[letter][parent_word]

    if parent_word in numb_dict.keys():
        definition = definition.split('1581199358571')
        definition = '<br> '.join(definition)
        word_str = f"This word has multiple definitions:<br>{definition}"

    else:
        word_str = f"This word has one definition:<br>{definition}"
    
    return parent_word + "|" + word_str
    

    


