"""List of bots that deal with js applications"""
from argparse import ArgumentParser
from commons.utils import parse_args
from diagnosis_online_bot.bot import run

if __name__ == "__main__":
    args = parse_args(ArgumentParser())
    run(args)
