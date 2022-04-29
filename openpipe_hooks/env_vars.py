#!/bin/env python

def main():
    """This file will be called by op-go in order to set up additional
    environment variables. Just print each line to stdout, separated by '\n'.
    Separate the key=values using the RS (Record Separator) ASCII character.
    In python this can be obtained by doing: chr(30)
    https://theasciicode.com.ar/ascii-control-characters/record-separator-ascii-code-30.html

    For example:
    >>> separator=chr(30)
    >>> print((f'YOUR_ENV_VAR{separator}YOUR_VALUE'))
    """
    separator=chr(30)
    print((f'YOUR_ENV_VAR{separator}YOUR_VALUE'))

if __name__ == "__main__":
    main()