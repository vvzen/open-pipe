# README

## op: A no frills filesystem navigation script written in fish

### How to use

From a terminal where `$SHELL` is `fish`, simply create an alias called 'op', that sources the `op.fish` file, like this:
```
alias op="source /whereever/you/installed/open-pipe/openpipe/bin/op.fish"
```

### Why fish?

'Cause fish is exactly what it says it is: a Friendly Interactive SHell.
Fish makes the scripting a pleasure, and it's incredibly user-friendly thanks to its built-in autocompletions.
Customizing fish is as easy as typing `fish_config` in your terminal.
The hope is to give a easy to use and inclusive shell that the consumers of OpenPipe will love.

While any more 'serious' script that has to be portable/POSIX-compliant will be written in bash, the filesystem navigation is a simple enough task that can be achieved in a more adventerous and user-friendly way thanks to fish.

Fish also has good support for variable scoping.

The intention of OpenPipe currently is to use bash for heavy lifting back-end stuff, and fish for anything that is user-facing.

Further reading:
- https://betterprogramming.pub/fish-vs-zsh-vs-bash-reasons-why-you-need-to-switch-to-fish-4e63a66687eb
- https://arstechnica.com/information-technology/2005/12/linux-20051218/3/


## get-context: A simple CLI for retrieving contexts from paths written in python

The aim of `get-context` is to make it incredibly easy to programmatically understand which show, sequence and shot and path belongs to.

The most basic usage would be something like this:
```bash
$ echo "/some/path/sc010/sc010_0010" | get-context
OPENPIPE_SHOW=path,OPENPIPE_SEQUENCE=sc010,OPENPIPE_SHOT=sc010_0010
```

However, `get-context` was designed so that it plays well with other UNIX tools, which means that you can do things like:

```bash
$ echo -e "/some/path/sc010/sc010_0010" | ./bin/get-context | tr "," "\n" | grep OPENPIPE_SHOT | sed 's/OPENPIPE_SHOT=//g'
sc010_0010
```

in order to extract the shot name from a path.

This approach works well also for multiple paths:

```bash
$ echo -e "/some/path/sc010/sc010_0010\n/some/path/sc010/sc010_0020" | get-context | tr "," "\n" | grep OPENPIPE_SHOT | sed 's/OPENPIPE_SHOT=//g'
sc010_0010
sc010_0020
```
