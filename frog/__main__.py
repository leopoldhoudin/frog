from argparse import ArgumentParser
from datetime import date
from collections import namedtuple
from functools import partial


Commit = namedtuple('Commit', 'hash, date, auth, subj')


def colored(text: str, color: int):
    return f'\033[{color}m{text}\033[0m'


red = partial(colored, color=31)


def fatal(text: str):
    print(f'🌶  {red(text)}')
    exit(1)


def info(text: str):
    print(f'   {text}')


def main():
    parser = ArgumentParser('frog')
    args = parser.parse_args()

    from os import getcwd
    from os.path import join
    from os.path import isdir

    from subprocess import PIPE
    from subprocess import Popen

    from re import compile as compile_regex

    git_path = join(getcwd(), '.git')
    if not isdir(git_path):
        fatal('Current directory is not a git repository!')

    info('Scanning history...')

    proc = Popen(
        ['git', '--no-pager', 'log', '--full-history', '--reverse', '--format="%H:%as:%ae:%s"'],
        stdout=PIPE,
    )

    commit_regex = compile_regex(r'([0-9a-f]{40}):(\d{4}-\d{2}-\d{2}):(.*?):(.*)')

    commits = []
    # print('-----')
    while True:
        line = proc.stdout.readline()
        if not line: break
        line = line.decode().rstrip('\n').strip('"')

        commit_match = commit_regex.match(line)

        if commit_match:
            # print('HASH:', commit_match.group(1))
            # print('DATE:', commit_match.group(2))
            # print('AUTH:', commit_match.group(3))
            # print('SUBJ:', commit_match.group(4))
            # print('-----')

            commits.append(Commit(
                commit_match.group(1),
                date.fromisoformat(commit_match.group(2)),
                commit_match.group(3),
                commit_match.group(4),
            ))
            # print(commits[-1])

    proc.stdout.close()
    proc.wait()

    from time import sleep
    from progress.bar import ChargingBar

    bar = ChargingBar('   Scanning commits...', max=len(commits), suffix='%(percent)d%% (%(index)d/%(max)d)')
    for commit in commits:
        # Do some work
        sleep(0.01)
        bar.next()
    bar.finish()

    # run(['git', '--no-pager', 'log', '--full-history', '--reverse', '--format="%H:%as:%ae:%s"'])


"""
6a1ec1d90a7e5bdbd08247277ea4edef180e96a5

git --no-pager log --full-history --reverse --format="%H:%as:%ae:%s"

git --no-pager log --pretty=oneline --full-history --reverse
--date=iso-strict

"""

if __name__ == '__main__':
    main()
