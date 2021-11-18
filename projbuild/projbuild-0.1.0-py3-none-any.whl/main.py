import time
import json
import click
import pkg_resources
from .runner import exec_goal
from colored import fg, bg, attr

version = pkg_resources.require("projbuild")[0].version

@click.group()
@click.version_option("1.0.0")
def main():
    """a build system for c/c++ projects written in python"""

    # ooo fancy
    s = f"* PROJBUILD build system version {version} *"

    print("*" * len(s))
    print(f"*{' ' * (len(s) - 2)}*")
    print(s)
    print(f"*{' ' * (len(s) - 2)}*")
    print("*" * len(s))
    pass

@main.command()
@click.argument("goal", required=True)
def build(**kwargs):
    """build a goal specified by the project file"""
    start = time.time()

    project = {}

    with open("project.json", "r") as f:
        project = json.load(f)
    
    try:
        name = project["name"]
        echo = True

        if "echo" in project:
            echo = project["echo"]

        exec_goal(project, name, echo, kwargs["goal"])

    except KeyError as e:
        print(f"{fg(1)}Invalid project.json! Aborting.")
        print(f"Missing key: {e}.{attr('reset')}")

    end = time.time()
    print(f"Finished! Took {round(end - start, 2)} seconds.")
    pass

@main.command()
def goals(**kwargs):
    """display all goals in the current project"""
    project = {}

    with open("project.json", "r") as f:
        project = json.load(f)
    
    try:
        name = project["name"]

        print(f"Available goals for project \"{name}\":")

        for x in project["goals"]:
            print(f"- {x}")

    except KeyError as e:
        print(f"{fg(1)}Invalid project.json! Aborting.")
        print(f"Missing key: {e}.{attr('reset')}")
    pass

if __name__ == '__main__':
    main()
