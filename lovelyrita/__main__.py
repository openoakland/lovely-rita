from __future__ import print_function
import argparse

from lovelyrita.clean import clean
from lovelyrita.data import read_data, summarize, write_shapefile, to_geodataframe


def parse_arguments():
    # Commands are called with `lovelyrita <subcommand> <args>`
    parser = argparse.ArgumentParser(prog="lovelyrita")
    subcommand = parser.add_subparsers(title="subcommand", dest="subcommand")

    clean = subcommand.add_parser('clean', help="""Clean raw data file""")
    clean.set_defaults(command_name='clean')
    clean.add_argument('in_path', help="""File path to the raw data""")
    clean.add_argument('out_path', help="""Output path""")

    summarize = subcommand.add_parser('summarize', help=("""Generate a column summarize from 
                                                            raw data file"""))
    summarize.set_defaults(command_name='summarize')
    summarize.add_argument('in_path', help="""Location of the raw data.""")

    preprocess = subcommand.add_parser('convert', help=("""Convert between two file types"""))
    preprocess.set_defaults(command_name='convert')
    preprocess.add_argument('in_path', help="""Location of the raw data.""")
    preprocess.add_argument('out_path', help="""Where to store the output data""")
    preprocess.add_argument('--clean', action='store_true',
                            help="""Clean the input data before conversion""")

    args = parser.parse_args()
    return args


def main(args=None):
    args = parse_arguments()

    if args.subcommand == 'clean':
        print('... Loading data from {}'.format(args.in_path))
        df = read_data(args.in_path)
        print('... Cleaning data')
        df = clean(df)
        print('... Writing output to {}'.format(args.out_path))
        df.to_csv(args.out_path)

    elif args.subcommand == 'summarize':
        print('... Loading data from {}'.format(args.in_path))
        df = read_data(args.in_path)
        print(summarize(df))

    elif args.subcommand == 'convert':
        from lovelyrita.data import column_map
        column_map['[latitude]'] = 'latitude'
        column_map['[longitude]'] = 'longitude'

        print('... Loading data from {}'.format(args.in_path))
        df = read_data(args.in_path, column_map, clean=args.clean)

        out_path = args.out_path
        if out_path.endswith('.shp'):
            print('... Converting to GeoDataFrame')
            df = to_geodataframe(df)
            print('... Writing output to {}'.format(out_path))
            write_shapefile(df, out_path)
        else:
            raise NotImplementedError('Output file type not supported.')


if __name__ == "__main__":
    main()
