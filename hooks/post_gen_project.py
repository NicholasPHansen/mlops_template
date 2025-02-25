from keyword import iskeyword
from operator import ge, le

project_name = "{{cookiecutter.project_name}}"
python_version = "{{cookiecutter.python_version}}"


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


if not project_name.isidentifier() or not project_name.islower():
    raise ValueError(
        "\n"
        "Project name must be a valid project name, meaning that it must be a valid Python name and also be lowercase."
        " This means that it must not contain spaces or special characters, and must not start with a number."
        " In general it is best to use only lowercase letters and underscores."
        " You can read more about Python naming conventions for packages here:"
        " https://peps.python.org/pep-0008/#package-and-module-names"
        "\n",
    )
if iskeyword(project_name):
    raise ValueError(
        "Project name must not be a built-in keyword, as it will cause syntax errors.",
    )

min_version = "3.8"
max_version = "3.13"
if not (
    ge(versiontuple(python_version), versiontuple(min_version))
    and le(versiontuple(python_version), versiontuple(max_version))
):
    raise ValueError(
        f"Python version must be between {min_version} and {max_version}."
        " These are the versions that still receive support."
        " You can read more about Python versioning here: https://devguide.python.org/versions/",
    )
