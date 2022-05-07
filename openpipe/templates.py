import openpipe.show
from openpipe.config import get_config

def get_template(name):

    templates = get_config("templates")

    if name not in templates:
        raise ValueError("No template found with name='%s'" % name)
    return templates[name]


def analyze_template(template_str):

    "{shows_root}/{show_name}/{context}/work"
    "{$default_workfile}.mb"

    tokens = []
    partials = []

    current_token = []
    current_partial = []

    token_has_started = False
    partial_has_started = False

    for char in template_str:

        # Delimiter start
        if char == "{":
            token_has_started = True
            current_token = []
            continue

        # Delimiter end
        if char == "}":

            if current_partial and partial_has_started:
                partials.append("".join(current_partial))

            if current_token and token_has_started:
                tokens.append("".join(current_token))

            token_has_started = False
            partial_has_started = False
            continue

        if partial_has_started:
            current_partial.append(char)
            continue

        if token_has_started:
            if char == "$":
                partial_has_started = True
                continue
            else:
                current_token.append(char)
                continue

    return tokens, partials


def flatten_template(template):
    tokens, partials = analyze_template(template)

    for partial_name in partials:
        template_partial = get_template(partial_name)
        partial_token = "{$%s}" % (partial_name)
        template = template.replace(partial_token, template_partial)

    return template


def render_template(template_name, fields):

    template = get_template(template_name)

    all_fields = {
        "shows_root": openpipe.show.get_show_root(),
        "show_name": openpipe.show.get_current_show_name(),
    }
    all_fields.update(**fields)

    # Resolve nested partials
    while "$" in template:
        template = flatten_template(template)

    tokens, partials = analyze_template(template)

    for token in tokens:
        if token not in all_fields.keys():
            raise KeyError("Missing required field named '%s'" % token)

    #print(template)
    #print(partials)

    rendered = template.format(**all_fields)

    return rendered