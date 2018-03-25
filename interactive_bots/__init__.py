""" Bot that deals with js applications """
from argparse import ArgumentParser
from interactive_bots.commons.utils import parse_args
from interactive_bots.diagnosis_online_bot.bot import run

if __name__ == "__main__":
    args = parse_args(ArgumentParser())
    run(args)
