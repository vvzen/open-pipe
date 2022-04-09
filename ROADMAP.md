# ROADMAP

A list of development goals and tasks which I want to address in the future.
Items under the DONE section have been completed.
This file also works as a developer diary.

# Done

### Understand if yaml is a good choice for configs

In Framestore we use yaml since it provides better readability compared to JSON.
However, support for parsing `yaml` doesn't ship with the standard library of python, which means that to use `op` one would first need to install `pyyaml` for their current python, which is not optimal.

I want to reduce the burden and chaos introduced by vendoring third-party libraries as much as possible, and as such, I mostly see 2 options:

- Use a config format that is supported by python's standard library

- Use a config format that _will_ be supported by python's standard library

- Don't use python for parsing the configs that `op` relies on, and instead compile and ship a binary (say, in Rust). So `get-context` would need to be rewritten in Rust.

**Short read**
Currently, I'm leaning more towards adopting TOML in python.
While it's not part of python yet, it will be part of the standard library in python3.11 (which means it's future-proof) and also, in case I ever need it, it ships in RUST without any other dependencies, since cargo uses it.
TOML is definitely simpler to parse than yaml, and is in line with the minimalistic approach of `OpenPipe`.

**Long read**:

TOML is another config language alternative worth exploring. It doesn't ship with python, but will in the future (Python 3.11+) since [PEP-680](https://peps.python.org/pep-0680/) has been accepted.

Further reading:
- https://noyaml.com/
- https://toml.io/en/
- https://github.com/hukkin/tomli
- https://discuss.python.org/t/pep-680-tomllib-support-for-parsing-toml-in-the-standard-library/13040/22
- https://github.com/pypa/pip/pull/8045


Reading Toml (using tomli)
```python
with open(config_path, "rb") as f:
    data_from_toml = tomli.load(f)
```

Reading YAML (using pyyaml)
```python
with open(config_path, "r") as f:
    data_from_yaml = yaml.safe_load(f.read())
```

> Result: TOML is a more future-proof, and less prone to misconfiguration by human-error. Implemented support in c7f5aca

### Implement 'op show'

<del>It should show the environment of the current directory</del>.
<del>Probably equivalent to something like `pwd | get-context`.</del>

This was implemented `Fri Mar 18 17:40:15 GMT 2022` under `op show-env`.

It will show the environment where you `go`ed to last.

> Result: implemented in 2742c1b

> In b34b3b0, renamed to `op display-env` to avoid ambiguities between a 'show' as in 'project/job' and 'show' as in 'to showcase/display'.

## Implement project creation

Create a CLI that is capable of generating the directory structure on disk, based on the `show_scheme`.

> First implementation of the libs in d563632

> Expose the functionality in a CLI. Done in b5de2ff

#### Implement support for setting OCIO env var

Just like we automatically set the `OPENPIPE_CONFIG_PATH` when users do a `op go some_dir`, we should allow `op go` to set other useful env var, like the `OCIO` one for targeting custom OCIO configs.

To make the mechanism generic, the logic for setting this path should be customizable (via hooks), with a default implementation provided.

> Implemented in d2d6912 by letting the user define a `env_vars.py` file that prints to stdout the vars they want to set on each go.


# TODO

## General
### Implement a 'deactivate' type of script for source_me.fish & source_me.bash

This should remove any changes that the sourcing of these files brought to the environment.
The is similar to how a `conda deactivate` works, or a `module unload` (for tcl modules)

## Implement validation of configs via JSONschema

Right now there's no programmatic validation of the config files.

If a required entry is missing, it's up to the implementation of the single function relying on that config file to properly handle this exception.
Instead, the `get_config(name)` call should automatically validate all of the entries based on the JSONschema of that config.
