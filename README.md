# Open-Pipe

[![license](https://img.shields.io/github/license/vvzen/open-pipe)](https://github.com/vvzen/open-pipe/blob/main/LICENSE) [![coverage](https://img.shields.io/codecov/c/github/vvzen/open-pipe)](https://app.codecov.io/gh/vvzen/open-pipe) ![Generic badge](https://img.shields.io/badge/status-wip-yellow.svg)

(Horribly WIP) Set of modular python tools meant to cover the most common operations needed when setting up a VFX / animation pipeline.


## Design goals

### OOP as latest resort

1. OOP is not bad, but it's easily abused.
Prefer a style inspired by functional programming (receive input, produce output, no side effects) when possible. This makes things really easy to unit test, and avoids keeping track of states.

2. Remember: exceptions are part of the interface of a function! Only add them when needed.

3. Prefer structs to classes. Prefer using `dataclass` containers to store data, don't add methods to them unless you feel you need to model something quite advanced. It's better to have a simple struct that is manipulated by a function, than a class that manipulates itself and has to keep track of internal properties (once again, favour a functional approach)

4. Avoid multiple inheritance like <del>the plague</del> covid. Use Mixins if needed (but only if reeaaally needed - like for Qt stuff)

5. If you're only accessing `self` a few times, it doesn't need to be a class.

6. If it looks simple, then probably it is simple. Don't be tempted to wrap things in a class just to make it look "professional" - always first write your implementation as a function.

### Tests are first class citizens

1. When choosing abstractions, pick the one that it's easier to test. The less boilerplate code is needed to test something, the better.

2. Use TDD when it makes sense. This helps keep a clean API and focuses on shipping useful features while providing an intuitive interface. TDD does not means lack of design – if used carefully, TDD works best to help you guide towards the most practical abstractions.

### Functions should be easily retriable

1. Try to make things [idempotent](https://en.wikipedia.org/wiki/Idempotence) when it's possible. This makes it easier to run tests in isolation while always keeping a clean state.

2. When things fail, try to make the failure as localized as possible. Tear down any potential change that you might have applied before the failure, in order to remove side effects.

### Use schemas to limit responsibilities

1. Applications should communicate using an agreed schema. Just like in UNIX, where so much can be achieved by simply piping the stdout of a program into stdin. Or, in a more elaborate way, like REST APIs. Nobody needs to know more than that what's expressed in an agreed schema – never make assumptions over the environment, etc.

2. When possible, make CLIs that feed from stdin instead of files. Favour `cat something.txt | my-app` rather than `my-app --input-file something.txt`, unless you have a very good reason not to.

3. Always version your schemas.

### Treat the consumer of your API with respect

1. "We're all condescending adults". Simplify when needed, but don't oversimplify and take decisions instead of your users - always leave them flexibility to act the way they want. Once again, receive and return from your programs using shared schemas instead.

2. When in doubt, always prefer flexibility. OpenPipe tries to offer sane defaults, but can be customized. Most of the functionality can be tweaked by either editing config files (the `.toml` ones under `configs`), environment variables or via code hooks.


## Environment variables

All of the environment variables used by OpenPipe are prefixed with `OPENPIPE`, so that one can easily inspect them by doing something like:

```bash
$ env | grep OPENPIPE
```

### OPENPIPE_LOG

By default, it's not set.
Set it to "DEBUG" to enable additional debugging.
Set it to something like `DEBUG %(asctime)s-%(filename)s:` to specify a custom string for the logging formatter used by OpenPipe.

### OPENPIPE_CONFIG_PATH

Search path of the configuration files (.toml) used by OpenPipe.
