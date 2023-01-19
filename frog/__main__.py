from argparse import ArgumentParser
from os import getcwd
from os.path import join
from os.path import isdir

from frog.scanner import scan_project
from frog.terminal import term
from frog.terminal import bold


def main():
    parser = ArgumentParser('frog')
    # -c/--config ${path}
    # -o/--output $[json, csv, image]

    args = parser.parse_args()

    git_path = join(getcwd(), '.git')
    if not isdir(git_path):
        term.fatal('Current directory is not a git repository!')

    project = scan_project()

    print(f'👷 {bold("Contributors")}:')
    print('   •')


if __name__ == '__main__':
    main()
