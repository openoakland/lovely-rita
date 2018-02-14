from __future__ import print_function
import argparse
import pandas as pd

from lovelyrita.clean import clean
from lovelyrita.utils import read_data

def preprocess(input_path, output_path, column_dtype, column_map, delimiter):
    df = read_data([input_path,], column_dtype, column_map, delimiter)
    df.to_csv(output_path)

def column_report(file_path):
    df = pd.read_csv(file_path)
    print(get_column_report(df))

def parse_arguments():
    # Commands are called with `lovelyrita <subcommand> <args>`
    parser = argparse.ArgumentParser(prog="lovelyrita")
    subcommand = parser.add_subparsers(title="subcommand", dest="subcommand")

    clean = subcommand.add_parser('clean', help="""Clean raw data file.""")
    clean.set_defaults(command_name='clean')
    clean.add_argument('file_path', help="""File path to the raw data.""")

    column_report = subcommand.add_parser('column_report', help=("""Generate a column report from 
                                                                    raw data file."""))
    column_report.set_defaults(command_name='column_report')
    column_report.add_argument('file_path', help="""Location of the raw data.""")

    preprocess = subcommand.add_parser('preprocess', help=("""Preprocess a raw data file and save 
                                                              to an output file."""))
    preprocess.set_defaults(command_name='preprocess')
    preprocess.add_argument('input_path', help="""Location of the raw data.""")
    preprocess.add_argument('output_path', help="""Where to store the output data""")
    preprocess.add_argument('column_type', help=("""Integer indicating how to interpret the columns 
                                                    of the raw data file."""))
    preprocess.add_argument('delimiter', default=',', help=("""String that separates adjacent 
                                                               values in the raw data"""))

    args = parser.parse_args()
    return args

def main(args=None):
    args = parse_arguments()

    if args.subcommand == 'clean':
        clean(args.file_path)
    elif args.subcommand == 'column_report':
        column_report(args.file_path)
    elif args.subcommand == 'preprocess':
        from lovelyrita.column_dtypes import column_dtypes
        from lovelyrita.column_maps import column_maps

        preprocess(args.input_path, args.output_path,
                   column_dtypes[args.column_type],
                   column_maps[args.column_type],
                   delimiter=args.delimiter)

if __name__ == "__main__":
    main()
