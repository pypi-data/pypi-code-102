import argparse
import flavuer
from flavuer import utils

def add_sp(sub_p, action, func, help=None):
  """Add an action to the main parser

  :param sub_p: The sub parser
  :param action: The action name
  :param func: The function to perform for this action
  :param help: The help to show for this action
  :rtype: The parser that is generated
  """
  p = sub_p.add_parser(action, help=help)
  p.set_defaults(func=func)
  return p

def main():
  parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description = 'Flask / VueJS')
  sub_p = parser.add_subparsers(title='Actions',
                                help='%(prog)s <action> -h for more info')

  # Create Application
  p_create_app = add_sp(sub_p, "create-app", utils.create)
  p_create_app.add_argument('name', help="Name of the application")

  # Run dev environment
  p_dev = add_sp(sub_p, "dev", utils.run_dev)

  args = parser.parse_args()
  print("\nflavue - v{}".format(flavuer.__version__))

  args.func(args)

if __name__ == "__main__":
  main()

