from datetime import date
from typing import List


class Commit:
    def __init__(self, hash: str, date: date, author: 'Contributor', subject: str):
        self._hash = hash
        self._date = date
        self._auth = author
        self._subj = subject

    @property
    def hash(self) -> str:
        return self._hash

    @property
    def date(self) -> date:
        return self._date

    @property
    def author(self) -> 'Contributor':
        return self._auth

    @property
    def subject(self) -> str:
        return self._subj

    def __repr__(self) -> str:
        return self._hash


class Contributor:
    def __init__(self, name: str):
        self._name = name
        self._commits: List[Commit] = []

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name

    def _set_commits(self, commits: List[Commit]):
        self._commits.clear()
        self._commits = commits.copy()


class File:
    def __init__(self, path: str, commits: List[Commit]):
        self._path = path
        self._commits: List[Commit] = commits

    @property
    def path(self) -> str:
        return self._path


class Project:
    def __init__(self):
        self._commits: List[Commit] = []
        self._contribs: List[Contributor] = []
        self._files: List[File] = []

    @property
    def commits(self) -> List[Commit]:
        return self._commits

    @property
    def contributors(self) -> List[Contributor]:
        return self._contribs

    @property
    def files(self) -> List[File]:
        return self._files

    def _add_commit(self, commit: Commit):
        self._commits.append(commit)

    def _add_contrib(self, contrib: Contributor):
        self._contribs.append(contrib)

    def _add_file(self, file: File):
        self._files.append(file)
