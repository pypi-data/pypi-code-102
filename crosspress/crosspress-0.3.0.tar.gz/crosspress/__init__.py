import sys
from platform import system
from .dict import kdict

CP_SILENT = 0x00
CP_NOISY = 0x01
CP_ERROR = 0x02
CP_DELAY = 0.05

PLATFORM = system()

if PLATFORM == "Windows":
    from ._windows import sequence as _sequence
    from .dict import windows_kdict as _kdict
elif PLATFORM == "Linux":
    from ._linux import sequence as _sequence
    from .dict import linux_kdict as _kdict
elif PLATFORM == "Darwin":
    from ._darwin import sequence as _sequence
    from .dict import darwin_kdict as _kdict
else:
    raise OSError(f"Unsupported platform «{PLATFORM}»")

shortcuts = _kdict(kdict)


def log(message, behavior):
    if behavior == CP_NOISY:
        print(message)
    elif behavior == CP_ERROR:
        sys.exit(message)
    return


def vk(key, behavior):
    key = str.strip(key)
    if key not in shortcuts:
        log(f"Unknown key «{key}»", behavior)
        key = None
    return key


def vc(combination, behavior):
    combination = map(lambda x: vk(x, behavior), combination.split("+"))
    combination = list(filter(None, combination))
    return combination if len(combination) > 0 else None


def vs(sequence, behavior):
    sequence = map(str.strip, sequence.split(","))
    sequence = [vc(combination, behavior) for combination in sequence]
    sequence = list(filter(None, sequence))
    return sequence


def tap(sequence: str, delay: int = CP_DELAY, behavior: (CP_NOISY, CP_SILENT, CP_ERROR) = CP_SILENT) -> None:
    sequence = vs(sequence, behavior)
    if len(sequence) > 0:
        for combination in sequence:
            codes = []
            if behavior == CP_NOISY:
                print("Tap «" + " + ".join([*combination]) + "»")
            for shortcut in combination:
                codes.append(shortcuts.get(shortcut))
            _sequence(codes, delay)
    else:
        log("Nothing to tap", behavior)
    return
