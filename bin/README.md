# README

## op: A no-frills filesystem navigation script written in fish

#### Prerequisites

Op is built on top of `fish`, the shell for people that love elegance and shells.

For more info on how to install `fish`, please see: https://fishshell.com

The TL;DR for installing is:

On Mac, using brew:
```bash
$ brew install fish
```

On Ubuntu:
```bash
$ sudo apt-add-repository ppa:fish-shell/release-3
$ sudo apt update
$ sudo apt install fish
```

On Centos 7:
```bash
$ cd /etc/yum.repos.d/
$ wget https://download.opensuse.org/repositories/shells:fish:release:3/CentOS_7/shells:fish:release:3.repo
$ yum install fish
```

On Debian 10:
```bash
$ echo 'deb http://download.opensuse.org/repositories/shells:/fish:/release:/3/Debian_10/ /' | sudo tee /etc/apt/sources.list.d/shells:fish:release:3.list
$ curl -fsSL https://download.opensuse.org/repositories/shells:fish:release:3/Debian_10/Release.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/shells_fish_release_3.gpg > /dev/null
$ sudo apt update
$ sudo apt install fish
```

On Windows, using WSL, just follow the instructions for the relevant linux distro you installed.

### How to use

From a terminal where `$SHELL` is `fish`, simply create an alias called 'op', that sources the `op.fish` file, like this:
```
alias op="source /whereever/you/installed/open-pipe/openpipe/bin/op/op.fish"
```

To remove the alias, type:
```
functions --erase name op
```

### Example commands

```fish
# Go to a shot
$ op go sc010/sc010_0010

# Show info on the environment
$ op show
```

### Why fish?

'Cause fish is exactly what it says it is: a Friendly Interactive SHell.

Fish makes the scripting a pleasure, and it's incredibly user-friendly thanks to its built-in autocompletions.
Customizing fish is as easy as typing `fish_config` in your terminal.
The hope is to give a easy to use and inclusive shell that the consumers of OpenPipe will love.

While any more 'serious' script that has to be portable/POSIX-compliant will be written in bash, the filesystem navigation is a simple enough task that can be achieved in a more adventurous and user-friendly way thanks to fish.

Fish also has good support for variable scoping.

The intention of OpenPipe currently is to use `bash` for heavy lifting back-end stuff that needs to be POSIX compliant, and `fish` for anything that is user-facing.

Further reading:
- https://betterprogramming.pub/fish-vs-zsh-vs-bash-reasons-why-you-need-to-switch-to-fish-4e63a66687eb
- https://arstechnica.com/information-technology/2005/12/linux-20051218/3/
- https://mvolkmann.github.io/fish-article/


## get-context: A simple CLI for retrieving contexts from paths (python)

The aim of `get-context` is to make it incredibly easy to programmatically understand which show, sequence and shot a given path belongs to.
`get-context` uses the `show_naming.toml` config file, which means that you can define your custom regexes to tell `get-context` what constitutes a sequence or a shot.

The most basic usage would be something like this:
```bash
$ echo "/some/path/sc010/sc010_0010" | get-context
OPENPIPE_SHOW=path,OPENPIPE_SEQUENCE=sc010,OPENPIPE_SHOT=sc010_0010
```

However, `get-context` was designed so that it plays well with other UNIX tools, which means that you can do things like:

```bash
$ echo "/some/path/sc010/sc010_0010" | ./bin/get-context | tr "," "\n" | grep OPENPIPE_SHOT | sed 's/OPENPIPE_SHOT=//g'
sc010_0010
```

in order to extract the shot name (in this case, `sc010_0010`) from a path.

This approach works well also for multiple paths separated by a newline character:

```bash
$ echo -e "/some/path/sc010/sc010_0010\n/some/path/sc010/sc010_0020" | get-context | tr "," "\n" | grep OPENPIPE_SHOT | sed 's/OPENPIPE_SHOT=//g'
sc010_0010
sc010_0020
```
