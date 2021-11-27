import click
import yaml
import readline
import os
import watchgod
from ardlib.fs import read_file, write_file, is_file_exist

dump = yaml.SafeDumper
load = yaml.load

def is_project_created():
    if is_file_exist("nvn.yaml"):
        return True
    return False

@click.group()
def cli():
    """ nvn command line interface """

@cli.command()
def init():
    if is_project_created():
        print("Error: Configuration already exist")
        exit(1)

    config = {
        "name": input("name: "),
        "version": input("version: "),
        "license": input("license: "),
    }
    write_file("nvn.yaml", dump(config, sort_keys=False))


@cli.command()
@click.argument("command_name")
def run(command_name: str):
    if not is_project_created():
        print("Error: Configuration don't exist")
        exit(1)
    
    content = load(read_file("nvn.yaml"), Loader=yaml.SafeLoader)
    if command_name in content["command"]:
        os.system(content["command"][command_name])
    else:
        print(f"Error: No command called {command_name} found")


@cli.command()
@click.argument("watch_path")
@click.argument("command")
def watch(watch_path: str, command: str):
    for _ in watchgod.watch(watch_path):
            os.system(command)

if __name__ == "__main__":
    cli()