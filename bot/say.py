from db import enums

already_registered = "There is already an account for user with this TelegramID.\n"

begin_legend = "Now choose one of the suggested modes. Find the instructions inside modes or use /help."

completed = "You can completed an exercise. If you've done it well - congrats:)"

choose_a_pack = "Choose a pack from a list below. Enter a number of a pack."

choose_general_goal = "Let's start with choosing a general goal for your learning." \
    "That will help me to suggest you entering different groups."

choose_learn_notifications = "I can remind you to look through your cards if you are off for a while." \
                             "Please, choose how often you wish to receive these notifications."

choose_mode = "Please, choose one of suggested modes. You can type /modes_help to find out more about them."

choose_pack = "List of your active packs. Choose one to show or edit."

choose_pack_name = "Choose name for a new pack."

choose_pack_privacy = "Choose pack privacy level: private or public"

choose_stats_notifications = "I can also tell you how much you've learned to give you some extra" \
                             "motivation. Now you can choose a way to get this kind of messages."

choose_type_of_review = "Choose type of review. Type /review_help for help."

choose_username = "Our system will remember you by your TelegramID and nickname. First of all, choose the latter!"

choose_weekly_goal = "Your weekly goal is a number of cards to learn in a week. I recommend at least 50" \
                     "cards, but you may go for more! Enter a number to continue."

hello = "Hey, you're back! Time to make some progress, isn't it?"

help = "/menu - head menu\n" \
       "/begin - choose exercise\n" \
       "/packs - edit your packs and cards\n" \
       "/groups - edit or admin your groups\n" \
       "\n" \
       "/review mode. Go through the pack and remember cards\n" \
       "/test mode\n" \
       "/learn mode - see the cards all together\n" \
       "/quit mode\n" \
       " \n" \
       "/new_pack - add new pack with some cards \n" \
       " \n" \
       " \n" \
       " \n" \
       " \n" \


incorrect_input = "Seems that you have enter something I hadn't expected. Please, read my previous" \
                  "instructions carefully, try again or type /help."

incorrect_weekly_goal = "Please, enter a positive integer not exceeding 1000."

invalid_pack = 'Pack file is invalid (line {})'

last_answer = "Your last answer was:"

learning_mode_legend = "Enter a number of a card to see the other side. You can /shuffle the cards," \
                    "/change_language or /quit."

menu_legend = "You are in the main menu. Choose a command from below list to begin."

no_packs_available = "No packs to show. You can add some with /new or activate with /update."

not_implemented = "Not implemented yet, stay tuned for updates."

not_recognized = "Your message wasn't recognized by bot\n" + \
    "Use /help for list of all commands"

pack_created = 'Pack {} successfully created'

pack_is_empty = "Oops, there are no cards in this pack. You can add some using /edit."

registration_completed = "Congrats, you've completed the registration and are able to use all available functions."

right = "OK."

start_mode_learning = "start_mode_learning"

upload_pack_file = "Please send .pack file\nIt should contain cards as 'front side' - 'back side'"

username_taken = "Oops. Our usernames are unique and this one seems to be taken. Please, try another one."

welcome = "Welcome to CardKeeper bot! ... Before you start, please, pass a quick registration procedure."

GEN_GOAL_TYPE = [v.value for k, v in enums.GenGoalType.__members__.items()]
NOTIFICATION_TYPE = [v.value for k, v in enums.NotificationType.__members__.items()]
# [v for k, v in enums.NotificationType.__members__.items()]


def choose_language(card):
    res = "choose_language"
    return str(res) + "\n" + "front - as " + card[1] + "\n" + "back - as " + card[2]


def enumerated(items):
    res = ""
    for i in enumerate(items):
        res = res + str(i[0] + 1) + ". " + i[1][1] + "\n"
    return res


def inter_results(a, b=None):
    return str(a) + " / " + str(b)


def wrong(ans):
    return "Wrong. Right answer - " + ans + ".\n"
