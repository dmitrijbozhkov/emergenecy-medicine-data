"""List of bots that deal with js applications"""
from lib.utils import parse_params
from diagnosis_online_bot.bot import run

if __name__ == "__main__":
    args = parse_params()
    run(args)
