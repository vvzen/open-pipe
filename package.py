name = "openpipe"
version = "0.1.0"
description = "Reusable tools for VFX/CG pipelines"
authors = ["Valerio Viperino"]

requires = ["python-3"]
build_command = "{root}/rezbuild"

def commands():
    import os
    env.PATH.prepend(os.path.join(root, "bin"))
    env.PYTHONPATH.append(os.path.join(root, "openpipe"))
