#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

PRODUCT_NAME = "cronrun.py"
RELEASE_VERSION = "0.1"


def main():
    parser = argparse.ArgumentParser(description="execute a command and output if abnormal exit")
    parser.add_argument("--logfile")
    parser.add_argument("--verbose", action='store_true', help="useful for debug")
    parser.add_argument("--version", action='store_true', help="print version")
    parser.add_argument("--use-tmpfile-prefix", default="/tmp/", help="directory path for temporary directory")
    parser.add_argument("commands", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if args.version:
        print("{}. Version: {}".format(PRODUCT_NAME, RELEASE_VERSION))
        return 0 # normal exit

    if len(args.commands) < 1:
        parser.print_help()
        return 128 # invalid argument

    # ########## ########## ########## ##########
    # execute a command
    out, err, ret_code = None, None, 1
    try:
        out, err = get_writer(args)
        verbose(args, "execute: {}".format(args.commands))
        ret_code = subprocess.call(args.commands, stdout=out, stderr=err)

    except FileNotFoundError as e:
        print("{} exec error: {}".format(PRODUCT_NAME, e), file=sys.stderr)
        ret_code = 127  # command not found

    except Exception as e:
        print("{} exec error: {}".format(PRODUCT_NAME, e), file=sys.stderr)
        ret_code = 126 # command invoked cannot execute

    finally:
        if out is not None:
            out.close()
        if err is not None:
            err.close()

    # ########## ########## ########## ##########
    # result evaluation
    if ret_code == 0:
        verbose(args, "command was successful.")
    else:
        verbose(args, "command was failed. exit code={}".format(ret_code))

        # write its output to stdout if abnormal exit
        with get_reader(args) as f:
            # if returns a file, it is temporary file
            for line in f:
                sys.stdout.write(line)

        verbose(args, "stdout and stderr was dumped to stdout")

    # ########## ########## ########## ##########
    # clean up
    fn = get_tmp_name(args)
    if fn is not None:
        os.remove(fn)
        verbose(args, "temporally file removed: {}".format(fn))

    return ret_code


def get_writer(args):
    return _file_pointer(args, "w")


def get_reader(args):
    return _file_pointer(args, "r")


def _file_pointer(args, mode):
    """
    create suitable file pointer.

    TODO: should return same type between mode=w and mode=r
    :param args:
    :param mode:
    :return:
    """
    if args.logfile:
        # outputs will goes to a log file
        verbose(args, "using log file: {}".format(args.logfile))
        f = open(args.logfile, mode)

        if mode != "w":
            return f

        return f, f

    # now outputs will goes to temporally file
    f_name_o = get_tmp_name(args)

    verbose(args, "using temporally output file: {}".format(f_name_o))
    f = open(f_name_o, mode)

    if mode != 'w':
        return f

    return f, f


def get_tmp_name(args):
    """
    returns a file name used for temporary.
    returns None when temporary file is not to be used. (eg. memory and logfile is used)

    TODO: should check file not to be exist before its creation.
    :param args:
    :return:
    """
    if args.logfile:
        return None

    return "{}cronlog.{}".format(args.use_tmpfile_prefix, os.getpid())


def verbose(args, message):
    if not args.verbose:
        return

    print(message, file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
