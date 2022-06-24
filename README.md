# Open-Pipe

[![license](https://img.shields.io/github/license/vvzen/open-pipe)](https://github.com/vvzen/open-pipe/blob/main/LICENSE) [![codecov](https://codecov.io/gh/vvzen/open-pipe/branch/main/graph/badge.svg?token=JW6UY6ZFFP)](https://codecov.io/gh/vvzen/open-pipe) ![Generic badge](https://img.shields.io/badge/status-wip-yellow.svg)
[![Run tests on Pull Request](https://github.com/vvzen/open-pipe/actions/workflows/run-tests-on-mrs.yaml/badge.svg)](https://github.com/vvzen/open-pipe/actions/workflows/run-tests-on-mrs.yaml)

## TL;DR

`OpenPipe` offers a python library and minimalistic command line utilities for dealing with cg/vfx pipelines.

It's currently in early development stage.

### Longer read

OpenPipe is a personal project born from a simple question:

> If I had to redo the pipeline at my studio from the core, how would I design it?

It's an experiment (but a concrete, usable one) to understand what didn't work and why.
It has already offered me plenty of insights, and made me realize how hard it is to write good flexible code.

Together with the `openpipe` python library, it offers `op` , a small cli that resembles `go` (not the programming language, but the `goat` utility) and can be used to navigate the filesystem and set the appropriate pipeline context.

`op` is built on top of `fish`, the shell for people that love elegance (and shells!).
The `fi` stands for `Friendly Interactive`: what more do you want?
For more info on how to install `fish`, please see: https://fishshell.com

The reason for choosing fish is that it's a joy to write scripts in fish, plus its autocompletion and ease of use makes it incredibly user friendly. Since `fish` is not POSIX compliant, my goal is mostly to use it for user facing tools.

For more info on the other CLIs offered, see https://github.com/vvzen/open-pipe/blob/main/bin/README.md


## Requirements

Poetry, for installing the dependencies: https://github.com/python-poetry/poetry

Install instructions: https://python-poetry.org/docs/master/#installing-with-the-official-installer


Fish, the shell: https://fishshell.com

## Getting started

Clone the repo, install fish, install the dependencies via poetry, and finally run `source openpipe/source_me.fish`.
Now you'll have `openpipe` in your `PYTHONPATH`, and the other CLIs in your `PATH`.

Add `alias op='source /path/to/where/you/have/downloaded/openpipe/bin/op/op.fish'` to your fish config to be able to do run commands like `op go`, etc.

Example commands for macOS:
```bash
# Install fish and poetry
$ brew install fish
$ curl -sSL https://install.python-poetry.org | python3 -
$ poetry completions fish > ~/.config/fish/completions/poetry.fish

# Clone the repo
$ git clone git@github.com:vvzen/open-pipe.git

# Install the dependencies via poetry
$ poetry install -vv

# Then, to have openpipe available:
$ cd open-pipe
$ source openpipe/source_me.fish

# Set your custom alias
# (replace DOWNLOADED_FILE with the proper path)
$ set DOWNLOADED_FILE bin/op/op.fish
$ echo "# OpenPipe" >> ~/.config/fish/config.fish
$ echo "alias op='source $DOWNLOADED_FILE'" >> ~/.config/fish/config.fish

# Check if everything is working fine
$ op go .
$ op-show --help
```

Customize the `./configs/*.toml` files to your needs, and put them in a directory under the `OPENPIPE_CONFIG_PATH`.
For more info, see the section on environment variables.

### Try it out!

Now try to create a project using `op-show create`.
Create a shot using `op-shot create`.

For each CLI, check the `--help` for more info and examples.

## Design goals

TL;DR: Be easy to refactor and test. Try functional first, OOP later. Be flexible and minimal. Be modular, like UNIX tools.
For more, see [DESIGN.md](https://github.com/vvzen/open-pipe/blob/main/DESIGN.md)


## Environment variables

All of the environment variables used by OpenPipe are prefixed with `OPENPIPE`, so that one can easily inspect them by doing something like:

```bash
$ env | grep OPENPIPE
```

## OPENPIPE_LOG

By default, it's not set.
Set it to "DEBUG" to enable additional debugging.
Set it to something like `DEBUG %(asctime)s-%(filename)s:` to specify a custom string for the logging formatter used by OpenPipe.

Example command (fish):
```bash
set --global --export OPENPIPE_LOG "DEBUG %(asctime)s-%(filename)s:"
```

## OPENPIPE_CONFIG_PATH

Search path of the configuration files (.toml) used by OpenPipe.

> Why `toml` and not JSON, yaml, ini, etc.. ? See the [ROADMAP.md](https://github.com/vvzen/open-pipe/blob/main/ROADMAP.md)

By default, when doing a `op go` to any directory, if there's a `openpipe/etc/config` directory below your current directory, it will be prepended to your `OPENPIPE_CONFIG_PATH`.
If there is none above, `op go` will start walking up from your cwd tries to set one.