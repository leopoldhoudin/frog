from datetime import date
from re import compile as compile_regex
from subprocess import PIPE
from subprocess import Popen

from progress.bar import ChargingBar

from frog.core import Project
from frog.core import Commit
from frog.core import Contributor
from frog.core import File
from frog.terminal import term


commit_regex = compile_regex(r'([0-9a-f]{40}):(\d{4}-\d{2}-\d{2}):(.*?):(.*)')
change_regex = compile_regex(r'(\w)\s+(.*?)$')


def scan_project() -> Project:
    term.head('🔎 Scanning project...')

    project = Project()

    _scan_history(project)
    _scan_commits(project)

    term.done('Completed\n')

    return project


def _scan_history(project: Project):
    term.info('Scanning history...')

    proc = Popen(
        ['git', '--no-pager', 'log', '--full-history', '--reverse', '--format="%H:%as:%ae:%s"'],
        stdout=PIPE,
    )

    contrib = {}

    while True:
        line = proc.stdout.readline()
        if not line: break
        line = line.decode().rstrip('\n').strip('"')

        commit_match = commit_regex.match(line)

        if commit_match:
            author_name = commit_match.group(3)
            author_info = contrib.get(author_name)
            if author_info is None:
                contrib[author_name] = author_info = (Contributor(author_name), [])

            commit = Commit(
                commit_match.group(1),
                date.fromisoformat(commit_match.group(2)),
                author_info[0],
                commit_match.group(4),
            )

            author_info[1].append(commit)
            project._add_commit(commit)

    proc.stdout.close()
    proc.wait()

    for contributor, commits in contrib.values():
        contributor._set_commits(commits)
        project._add_contrib(contributor)


def _scan_commits(project: Project):
    bar = ChargingBar(
        '   Scanning commits...',
        max=len(project.commits),
        suffix='%(percent)d%% (%(index)d/%(max)d)',
    )
    files_commits = {}
    for commit in project.commits:
        proc = Popen(
            ['git', 'diff-tree', '--no-commit-id', '--name-status', '-r', commit.hash],
            stdout=PIPE,
        )

        while True:
            line = proc.stdout.readline()
            if not line: break
            line = line.decode().rstrip('\n').strip('"')

            change_match = change_regex.match(line)
            if change_match:
                file_path = change_match.group(2)
                file_commits = files_commits.get(file_path)
                if file_commits is None:
                    files_commits[file_path] = file_commits = []

                file_commits.append(commit)

        for file_path, file_commits in files_commits.items():
            project._add_file(File(file_path, file_commits))

        bar.next()
    bar.finish()
