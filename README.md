# Open-Pipe

[![license](https://img.shields.io/github/license/vvzen/open-pipe)](https://github.com/vvzen/open-pipe/blob/main/LICENSE) [![coverage](https://img.shields.io/codecov/c/github/vvzen/open-pipe)](https://app.codecov.io/gh/vvzen/open-pipe) ![Generic badge](https://img.shields.io/badge/status-wip-yellow.svg)

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
For more info on how to install `fish`, please see: https://fishshell.com

The reason for choosing fish is that it's a joy to write scripts in fish, plus its autocompletion and ease of use makes it incredibly user friendly. Since `fish` is not POSIX compliant, my goal is mostly to use it for user facing tools.

Fore more info on the other CLI offered, see https://github.com/vvzen/open-pipe/blob/main/bin/README.md

## Getting started

NB: Install and use the `fish` shell (https://fishshell.com) if you want to use the CLIs.

If using fish: `source openpipe/source_me.fish`.
If using bash: `source openpipe/source_me.fish`.

Now you'll have openpipe in your pythonpath.
Customize the `./configs/*.toml` files to your needs, and put them in a directory under the `OPENPIPE_CONFIG_PATH`.

Create a project using `op-show create`. Check the `op-show create --help` for more info.

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

## OPENPIPE_CONFIG_PATH

Search path of the configuration files (.toml) used by OpenPipe.

> Why `toml` and not JSON, yaml, ini, etc.. ? See the [ROADMAP.md](https://github.com/vvzen/open-pipe/blob/main/ROADMAP.md)

By default, when doing a `op go` to any directory, if there's a `etc/config` directory above your current directory, it will be prepended to your `OPENPIPE_CONFIG_PATH`.