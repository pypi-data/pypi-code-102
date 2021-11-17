import sys

from tomwer.app.canvas_launcher.launcher import OMain


def main(argv=None):
    return OMain().run(argv)


if __name__ == "__main__":
    sys.exit(main())
