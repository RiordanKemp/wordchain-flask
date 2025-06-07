from flask import Flask, redirect, url_for, render_template, request, Blueprint, jsonify
import website.dailyword as daily_word

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

parent_wordGLOB = ""

already_used_words_set = set()
valid_letters_dict = daily_word.valid_letters_dict
words_dict = daily_word.words_dict


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

@auth.route('/setdifficulty', methods=['POST', 'GET'])
def difficulty():
    hardmode = request.form.get('hardmode')
    global difficultyOnGLOB
    # process the data using Python code
    if hardmode == "Enabled":
        difficultyOnGLOB = True
    elif hardmode == "Disabled":
        difficultyOnGLOB = False

@auth.route('/checkdiff', methods=['POST'])
def checkdiff():
    if (difficultyOnGLOB):
        return "T"
    else:
        return "F"
    
@auth.route('/checkint', methods=['GET'])
def checkint():
    return daily_word.daily_word
    pass
    
@auth.route('/checkchain', methods=['POST'])
def checkchain():
    wordchain = "⫘⫘".join(wordchainGLOB)
    wordchain = f"<b> {wordchain} </b>"
    return wordchain

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
    wordchain = "⫘⫘".join(wordchainGLOB)
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
    wordchain = "⫘⫘".join(wordchainGLOB)
    wordchain = f"<b> {wordchain} </b>"
    return input_str + "|NOERROR|" + wordchain + "|" + parent_min + "|" + parent_max




@auth.route("/main", methods=["POST"])
def main(): 

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


    parent_word = daily_word.daily_word #this is the daily word
    parent_wordGLOB = parent_word

    word_str = daily_word.definition


    
    return parent_word + "|" + word_str
    

    


