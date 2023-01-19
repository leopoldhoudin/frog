from argparse import ArgumentParser
from os import getcwd
from os.path import join
from os.path import isdir

from frog.scanner import scan_project
from frog.terminal import term
from frog.terminal import bold


FORMAT_TERM = 'term'
FORMAT_JSON = 'json'
FORMAT_CSV  = 'csv'
FORMAT_IMG  = 'image'
FORMAT_ALL  = [FORMAT_TERM, FORMAT_JSON, FORMAT_CSV, FORMAT_IMG]


def main():
    parser = ArgumentParser('frog')

    parser.add_argument('-f', '--format', type=str, choices=FORMAT_ALL, default=FORMAT_TERM)

    # -o/--output ${path}
    # -c/--config ${path}

    # Find some good name over here...
    # -w/--weight $[
    #     uniform,              each commit has the same weight
    #     time-linear,          older commits are weighted less
    #     time-quad,            same as time-linear, but using a quadratic
    #     time-rev-linear,      same as time-linear, but recent are weighted less
    #     time-rev-quad         same as time-linear, but recent are weighted less and using x2
    #     lines-linear,         commits with more lines changes are weighted more
    #     lines-quad,           same as lines-linear, but using quadratic
    #     files-linear,         commits with more files changes are weighted more
    #     files-quad,           same as files-linear, but using quadratic
    #   ]

    args = parser.parse_args()

    git_path = join(getcwd(), '.git')
    if not isdir(git_path):
        term.fatal('Current directory is not a git repository!')

    project = scan_project()

    term.head(f'👷 {bold("Contributors")}:')
    for contrib in project.contributors:
        term.info(f'• {contrib.name}')


if __name__ == '__main__':
    main()
