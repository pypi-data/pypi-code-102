import os
import sys
import shutil

from colorama import init, Fore, Back, Style

def create(args):
  init(autoreset=True)
  print(Style.BRIGHT + f"Generating flavuer project in {args.name}")

  # Copy the template directory into the destination
  pkg_dir = os.path.dirname(__file__)
  template_dir = os.path.join(pkg_dir, "template")
  template_app = os.path.join(template_dir, "app")

  # Destination
  project_name = args.name

  # Create main directory
  os.makedirs(project_name, exist_ok=True)

  # Create subdirectory with project name
  project_subdir = os.path.join(project_name, "app")
  if not os.path.exists(project_subdir):
    shutil.copytree(template_app, project_subdir)

  # Create venv within the directory
  os.system(f"python3 -m venv {args.name}/venv")

  # Install 
  os.system(f"{args.name}/venv/bin/pip install Flask")

  print(f"Sucessfully created project {args.name}")
  print(Style.BRIGHT + f"Created flavuer project in {args.name}\n\n")

  print(Style.BRIGHT + f"Get running for development")
  print(Fore.BLUE + f"\tcd {args.name}")
  print(Fore.BLUE + f"\tflavuer dev")

def run_dev(args):
  print("Starting dev environment")
  os.system("export FLASK_DEBUG=1; export FLASK_APP=app; ./venv/bin/flask run")