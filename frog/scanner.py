from datetime import date
from collections import namedtuple
from collections import defaultdict
from re import compile as compile_regex
from subprocess import PIPE
from subprocess import Popen
from typing import List

from progress.bar import ChargingBar

from frog.core import Project
from frog.core import Commit
from frog.core import Contributor
from frog.core import File
from frog.terminal import term


RawCommit = namedtuple('RawCommit', 'hash, date, auth, subj')


regex_commit = compile_regex(r'([0-9a-f]{40}):(\d{4}-\d{2}-\d{2}):(.*?):(.*)')
# regex_change = compile_regex(r'(\w)\s+(.*?)$')
regex_change = compile_regex(r'(\d+)\s+(\d+)\s+(.*)$')


def scan_project() -> Project:
    term.head('🔎 Scanning project...')

    raw_commits = _scan_history()
    project = _scan_commits(raw_commits)

    term.done('Completed\n')

    return project


def _scan_history() -> List[RawCommit]:
    term.info('Scanning history...')
    commits = []

    proc = Popen(_make_gitcmd_logs(), stdout=PIPE)
    while True:
        line = proc.stdout.readline()
        if not line: break

        match_commit = regex_commit.match(_clean_raw_line(line))
        if match_commit:
            commit = RawCommit(
                match_commit.group(1),
                date.fromisoformat(match_commit.group(2)),
                match_commit.group(3),
                match_commit.group(4),
            )

            commits.append(commit)

    proc.stdout.close()
    proc.wait()

    return commits


def _make_gitcmd_logs() -> List[str]:
    return ['git', '--no-pager', 'log', '--full-history', '--reverse', '--format="%H:%as:%ae:%s"']


def _scan_commits(raw_commits: List[RawCommit]) -> Project:
    bar = ChargingBar(
        '   Scanning commits...',
        max=len(raw_commits),
        suffix='%(percent)d%% (%(index)d/%(max)d)',
    )

    commits = []
    contribs = defaultdict(list)
    files = defaultdict(list)
    for raw_commit in raw_commits:
        adds, dels = 0, 0
        paths = []

        proc = Popen(_make_gitcmd_show(raw_commit.hash), stdout=PIPE)
        while True:
            line = proc.stdout.readline()
            if not line: break

            match_change = regex_change.match(_clean_raw_line(line))
            if match_change:
                adds += int(match_change.group(1))
                dels += int(match_change.group(2))
                paths.append(match_change.group(3))

        commit = Commit(
            raw_commit.hash,
            raw_commit.date,
            raw_commit.subj,
            len(paths),
            adds,
            dels,
        )

        commits.append(commit)
        contribs[raw_commit.auth].append(commit)
        for path in paths:
            files[path].append(commit)

        proc.stdout.close()
        proc.wait()

        bar.next()
    bar.finish()

    return Project(
        commits,
        [Contributor(*contrib) for contrib in contribs.items()],
        [File(*file) for file in files.items()],
    )


def _make_gitcmd_show(commit_hash: str) -> List[str]:
    return ['git', '--no-pager', 'show', '--format=', commit_hash, '--numstat']


def _clean_raw_line(raw_line: bytes) -> str:
    return raw_line.decode().rstrip('\n').strip('"')
