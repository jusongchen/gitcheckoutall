
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import subprocess
import os
import logging

import argparse

log = logging.getLogger(__name__)


def eprint(*args, **kwargs):
    # print  to stderr
    print(*args, file=sys.stderr, **kwargs)


class UnknowSubCommand(Exception):
    pass


def cmd_line_parser():
    '''
    setup cmd_line options
    return a instance of argparse.ArgumentParser
    '''
    parser = argparse.ArgumentParser(prog='gitcheckout', description='run git checkout recursive on all sub directory')
    parser.add_argument('-d', '--dir', dest="dir", help='which directory to start with')
    parser.add_argument('-b', '--branch', dest="branch", help='which git branch to checkout')
    parser.add_argument('-x', '--exec', dest="execute", action='store_true', help='execute the run. If not given, list directories only')
    return parser


def main():
    parser = cmd_line_parser()

    args = parser.parse_args()

    target_branches = ["integration", "master"]
    if args.branch not in target_branches:
        print("branch must be one of ", target_branches)
        parser.print_help()
        return

    if not args.dir:
        print("destination dir must be given")
        parser.print_help()
        return

    subdirs = [x[0] for x in os.walk(args.dir)]

    cmd = "git checkout "+args.branch
    print("cmd to run:{} \nTarget directories:".format(cmd))

    print(args)

    for subdir in subdirs:
        if not os.path.exists(os.path.join(subdir, '.git')):
            continue
        if args.execute:
            # if args.exec:
            print(subprocess.check_output([cmd], cwd=subdir, shell=True))
        else:
            print(subprocess.check_output(["printf `pwd`"], cwd=subdir, shell=True))

    print("\nuse flag '--exec' to actually run git checkout")


if __name__ == '__main__':
    main_file_dir = os.path.dirname(__file__)

    try:
        main()
    except Exception as e:
        log.exception(e)
        # write error message to stderr
        eprint("cmd '{}' failed:\n{}".format(' '.join(sys.argv), e))
        sys.exit(1)
