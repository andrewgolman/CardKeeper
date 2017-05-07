already_registered = "already registered"
begin_legend = "begin_legend"
begin_menu = "Choose a pack"
begin_options = "say.begin_options"
choose_a_pack = "choose_a_pack"
choose_general_goal = "choose_general_goal"
choose_language = "choose_language"
choose_learn_notifications = "choose_learn_notifications"
choose_mode = "choose_mode"
choose_stats_notifications = "choose_stats_notifications"
choose_type_of_review = "choose_type_of_review"
choose_username = "choose_username"
choose_weekly_goal = "choose_weekly_goal"
hello = "hello"
incorrect_input = "incorrect_input"
learning_mode_legend = "learning_mode_legend"
menu_legend = "menu_legend"
no_packs_available = "No packs to show. You can add some with /new or activate with /update."
pack_is_empty = "pack_is_empty"
register_to_access = "register_to_access"
registration_completed = "registration_completed"
start_mode_learning = "start_mode_learning"
username_taken = "username_taken"
welcome = "welcome"

GEN_GOAL_TYPE = ['Speech', 'Belletristic', 'Science']
NOTIFICATION_TYPE = ['Daily', 'Weekly', 'Never']


def enumerated(items):
    res = ""
    for i in enumerate(items):
        res = res + str(i[0] + 1) + ". " + i[1][1] + "\n"
    return res
