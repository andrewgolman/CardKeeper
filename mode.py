import message
import random


def setmode(cards):
    while True:
        message.choose_mode()
        mode = input().strip()
        if mode in ["1", "r", "review"]:
            review(cards)
        elif mode in ["2", "l", "learn"]:
            learn(cards)
        elif mode in ["3", "t", "test"]:
            test(cards)
        elif mode in ["4", "c", "constructing", "na", "noans"]:
            noans(cards)
        else:
            message.incorrect_command()
            continue
        break
    message.pack_completed()


def review(cards):
    message.review_mode_intro()
    message.choose_language(cards[0].front, cards[0].back)
    while True:
        lang = input().split(" ")[0].strip()
        if lang in ["1", "9", "first"]:
            lang = True
        elif lang in ["2", "0", "second"]:
            lang = False
        else:
            continue
        break
    message.review_mode_legend()

    i = 1
    right_answers = 0
    packsz = len(cards)
    random.shuffle(cards)

    for card in cards:
        message.card_front(i, card.side(lang))
        message.previous_answer()
        user = input().strip()
        message.card_shifted(card.side(not lang))
        quit = False
        while True:
            try:
                if user in ["-1", "exit", "end"]:
                    quit = True
                elif user in ["-2", "lang"]:
                    lang = not lang
                    cards.append(card)
                elif int(user) % 2:
                    right_answers += 1
                elif not (int(user) % 2):
                    cards.append(card)
                i += 1
                if i == packsz:
                    message.right_answers_number(right_answers, packsz)
            except ValueError:
                message.incorrect_command()
                message.review_mode_legend()
                user = input().strip()
            else:
                break
        if quit:
            break


def learn(cards):
    message.learn_mode_intro()
    message.choose_range(1, len(cards))
    while True:
        try:
            begin = int(input())
            if begin:
                end = int(input())
        except ValueError:
            message.incorrect_command()
            for card in cards:
                print(card.front, "-", card.back)
        else:
            break
    if begin:
        cards = cards[begin-1:end]
    show = []
    message.learn_mode_legend()
    lang = True
    while True:
        for i in enumerate(cards):
            message.card_front(i[0]+1, i[1].side(lang))
            if i[0] in show:
                message.card_back(i[1].side(not lang))
            else:
                print()
        while True:
            user = input().strip()
            try:
                if user in ["-9", "exit", "quit"]:
                    break
                elif user in ["-1", "lang"]:
                    lang = not lang
                elif user in ["-2", "rand"]:
                    random.shuffle(cards)
                    show = []
                elif user in ["-3", "all"]:
                    show = list(range(len(cards)))
                else:
                    show = [int(user) - 1]
            except ValueError:
                message.incorrect_command()
            else:
                break
        if user in ["-9", "exit", "quit"]:
            break


def test(cards):
    message.test_mode()


def noans(cards):
    while True:
        message.choose_language(cards[0].front, cards[0].back)
        while True:
            lang = input().split(" ")[0].strip()
            if lang in ["1", "9", "first"]:
                lang = False
            elif lang in ["2", "0", "second"]:
                lang = True
            else:
                continue
            break
        random.shuffle(cards)
        message.noans_mode_intro()
        i = 1
        for card in cards:
            message.card_front(i, card.side(lang))
            user = input().strip()
            if user in ["lang"]:
                lang = not lang
            elif user in ["answer"]:
                message.card_shifted(card.side(not lang))
            elif user in ["quit"]:
                break
            i += 1
        i = 1
        for card in cards:
            print()
            message.card_front(i, card.front)
            message.card_back(card.back)
            i += 1
        message.try_again()
        user = input()
        if user[0] not in ["y", "1", "9"]:
            break
