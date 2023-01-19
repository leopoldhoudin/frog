from functools import partial


def styled(text: str, style: int):
    return f'\033[{style}m{text}\033[0m'


bold = partial(styled, style=1)
red = partial(styled, style=31)
green = partial(styled, style=32)


class Terminal:
    def fatal(self, text: str):
        print(f'🌶  {red(text)}')
        exit(1)

    def done(self, text: str):
        print(f'✔️  {green(text)}')

    def head(self, text: str):
        print(text)

    def info(self, text: str):
        print(f'   {text}')


term = Terminal()
