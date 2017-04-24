dot_string = "." * 40


def card_back(s):
    print(" -", s)


def card_front(n, s):
    print(n, ". ", s, sep="", end=" ")


def card_shifted(s):
    print(dot_string, s)


def choose_answer():
    print("Answer: ")


def choose_language(a,  b):
    print("Choose the language")
    print("1. as", b)
    print("2. as", a)


def choose_mode():
    print("Choose the mode.")
    print("1. Reviewing")
    print("2. Learning")
    print("3. Test")
    print("4. Constructing")
    print("5. Retelling")
    print("6. Find out more...")


def choose_range(a, b):
    print("Choose range within", a, "-", b)


def enter_the_file():
    print("""Enter the file name. Please, make sure that the file contains only UTF-8
        symbols, otherwise it may be displayed incorrectly. TXT and DOC files are available.""")
    print("Enter '0' to quit.")
    print("Enter 'f1' to get more details.")


def file_is_empty(s):
    print("File '", s, "' is empty!")


def file_not_found(s):
    print("File '", s, "' is missing in the directory. Enter another name")


def goodbye():
    print("Thanks for using AndrewCards4.0! Keep learning the language:)")


def helpmsg():
    print("""Unfortunately, there is no information available now. Please, contact the
         "developers on andrewsgolman@gmail.com to get more details.""")


def incorrect_command():
    print("Incorrect_instruction!")


def learn_mode_intro():
    print("Learn mode selected")


def learn_mode_legend():
    print("0. Default")
    print("-1. Switch the language.")
    print("-2. Mix the cards.")
    print("-3. Show all translations.")
    print("-9. Quit.\n")


def menu():
    print("\n\nMENU")


def noans_mode_intro():
    print("Constructing mode selected")


def new_line():
    print()


def pack_completed():
    print("The pack is completed!")


def previous_answer():
    print("\t\t prev:", end=" ")


def review_mode_intro():
    print("Review mode selected")


def review_mode_legend():
    print("1. Right answer")
    print("2. Wrong answer")
    print("-1. Quit")
    print("-2. Change the language")


def right():
    print("Right")


def right_answers_number(a, b):
    print("Right answers: ", a, " / ", b)


def scanned_successfully(a, s):
    print(a, " words from ", s, " are scanned.")


def test_mode():
    print("-1. Quit")
    print("-2. Switch the language")
    print("Enter Your answer")


def try_again():
    print("Do it once again?")


def welcome():
    print("Welcome to AndrewCards4.3! With this application You can learn and review\nforeign words and phases!")


def wrong(a):
    print("Wrong. Right variant - ", a)
