# TODO

## General
### Implement a 'deactivate' type of script for source_me.fish & source_me.bash

This should remove any changes that the sourcing of these files brought to the environment.
The is similar to how a `conda deactivate` works, or a `module unload` (for tcl modules)


### Understand if yaml is a good choice for configs

In Framestore we use yaml since it provides better readability compared to JSON.
However, support for parsing `yaml` doesn't ship with the standard library of python, which means that to use `op` one would first need to install `pyyaml` for the current python, which is not optimal.

I want to reduce the burden and chaos introduced by vendoring third-party libraries as much as possible, and as such, I mostly see 2 options:

- Use a config format that is supported by python's standard library

- Don't use python for parsing the configs that `op` relies on, and instead compile and ship a binary (say, in Rust). So `get-context` would need to be rewritten in Rust.

Currently, I'm leaning more towards adopting TOML in python.
The TL;DR is that TOML will be part of the standard library in python3.11 (which means it's future-proof) and also, in case I ever need it, it ships in RUST without any other dependencies, since cargo uses it.


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

## Binaries
### op

#### Implement op show
It should show the environment of the current directory.