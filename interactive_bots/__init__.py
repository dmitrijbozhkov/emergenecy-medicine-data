""" Bot that deals with js applications """
from argparse import ArgumentParser
from interactive_bots.commons.utils import parse_args
from interactive_bots.diagnosis_online_bot.reactive_bot import run as diagnosis_online_run

if __name__ == "__main__":
    args = parse_args(ArgumentParser())
    if args.bot == "diagnosis_online":
        diagnosis_online_run(args)
    else:
        print("Bot not found")
