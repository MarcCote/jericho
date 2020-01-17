import os
from termcolor import colored

import argparse
import jericho


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("filenames", nargs="+",
                        help="Path to a Z-Machine game(s).")
    parser.add_argument("--debug", action="store_true",
                        help="Launch ipdb on FAIL.")

    return parser.parse_args()

args = parse_args()

filename_max_length = max(map(len, args.filenames))
for filename in sorted(args.filenames):
    print(filename.ljust(filename_max_length), end=" ")
    bindings = jericho.load_bindings(filename)
    if "walkthrough" not in bindings:
        print(colored("SKIP", 'yellow'))
        continue

    env = jericho.FrotzEnv(filename, seed=bindings['seed'])
    env.reset()

    walkthrough = bindings['walkthrough'].split('/')
    for cmd in walkthrough:
        obs, rew, done, info = env.step(cmd)

    if not done:
        print(colored("FAIL", 'red'))
        if args.debug:
            from ipdb import set_trace; set_trace()
    elif info["score"] != env.get_max_score():
        msg = "FAIL\tDone but score {}/{}".format(info["score"], env.get_max_score())
        print(colored(msg, 'red'))
        if args.debug:
            from ipdb import set_trace; set_trace()
    else:
        print(colored("PASS", 'green'))
