from crosspress import (tap, shortcuts, CP_NOISY, CP_ERROR, CP_SILENT, CP_DELAY)
import argparse


def crosspress():
    ap = argparse.ArgumentParser(
        description="Cross-platform lightweight keyboard simulator\n\n"
                    + "Sequence and combitantion example: crosspress -t \"h, e, l, l, o, left ctrl + enter\"\n\n"
                    + "Available keys: " + ", ".join(sorted([*shortcuts])),
        formatter_class=argparse.RawTextHelpFormatter)

    ap.add_argument("-t", "--tap", type=str, help="keyboard sequence", required=True)

    group = ap.add_mutually_exclusive_group(required=False)
    group.add_argument("-n", "--noisy", action="store_true", help="log all")
    group.add_argument("-e", "--error", action="store_true", help="crash when something went wrong")

    ap.add_argument("-d", "--delay", type=float, help="delay between taps in seconds", default=CP_DELAY)

    args = ap.parse_args()

    if args.tap:
        behavior = CP_SILENT
        if args.noisy:
            behavior = CP_NOISY
        elif args.error:
            behavior = CP_ERROR
        tap(args.tap, args.delay, behavior)


if __name__ == "__main__":
    crosspress()
