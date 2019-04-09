import re
import importlib

import yaml

ENV_VAR_MATCHER = re.compile(r"\$\{([^}]+)?([^}]+)?\}")

IMPLICIT_ENV_VAR_MATCHER = re.compile(r".*\$\{.*\}.*")


def _evaluate_env_var(match):
    env_var, default = match.groups()
    value = str(eval(env_var))
    if value is None:
        if default is None:
            default = ''
        value = default
        while IMPLICIT_ENV_VAR_MATCHER.match(value):  # pragma: no cover
            value = ENV_VAR_MATCHER.sub(_evaluate_env_var, value)
    return value


def parse(obj, libs=None):
    if libs and isinstance(libs, (list, tuple)):
        for lib in libs:
            try:
                module, module_name = lib.split(':')
            except ValueError:
                module = module_name = lib
            globals()[module_name] = importlib.import_module(module)

    def _parse(obj):
        if isinstance(obj, list):
            return [_parse(v) for v in obj]
        elif isinstance(obj, dict):
            return {k: _parse(v) for k, v in obj.items()}
        elif isinstance(obj, str):
            return ENV_VAR_MATCHER.sub(_evaluate_env_var, obj)
        else:
            return obj

    return _parse(obj)


def load(text):
    libs = None
    try:
        libs = eval(re.match(r'^#libs:(.*)', text.split('\n', 1)[0].replace(' ', '')).group(1))
    except Exception:
        pass
    return parse(yaml.safe_load(text), libs)
