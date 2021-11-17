import secrets
from contextlib import suppress
from hashlib import sha512
from sys import argv

import nacl.bindings as sodium
from zxcvbn import zxcvbn
from zxcvbn.time_estimates import display_time

from covert import util
from covert.tty import fullscreen
from covert.wordlist import words

MINLEN = 8  # Bytes, not characters


def generate(n=4, sep=""):
  """Generate a password of random words without repeating any word."""
  # Reject if zxcvbn thinks it is much worse than expected, e.g. the random
  # words formed a common expression, about 1 % of all that are generated.
  # This improves security against password crackers that use other wordlists
  # and does not hurt with ones who use ours (who can't afford zxcvbn anyway).
  while True:
    wl = list(words)
    pw = sep.join(wl.pop(secrets.randbelow(len(wl))) for i in range(n))
    if 4 * zxcvbn(pw)["guesses"] > len(words)**n:
      return pw
    print(pw)


def costfactor(pwd: bytes):
  """Returns a factor of time cost increase for short passwords."""
  return 1 << max(0, 22 - 2 * len(pwd))


def argon2(password: str, nonce: bytes):
  """Encode, prehash and argon2 hash a password."""
  password = util.encode(password)
  if len(password) < MINLEN:
    raise ValueError("Too short password")
  prehash = sha512(b"covert:" + password).digest()
  return _argon2(prehash, nonce, 8 * costfactor(password))


def _argon2(prehash: bytes, nonce: bytes, cost: int):
  return sodium.crypto_pwhash_alg(
    outlen=32,
    passwd=prehash,
    salt=nonce + bytes(4),
    opslimit=cost,
    memlimit=200 << 20,
    alg=sodium.crypto_pwhash_ALG_ARGON2ID13,
  )


def autocomplete(pwd, pos):
  head, p, tail = '', pwd[:pos], pwd[pos:]
  # Skip already completed words
  while p:
    for w in words:
      wl = len(w)
      if p[:wl] == w:
        head += p[:wl]
        p = p[wl:]
        break
    else:
      break
  hint = 'enter a few letters of a word first'
  if p:
    hint = ''
    matches = [w[len(p):] for w in words if w.startswith(p)]
    # Find the longest matching prefix of all candidates
    common = ''
    for letter, *others in zip(*matches):
      if others.count(letter) < len(others):
        break
      common += letter
    if not common:
      if not matches:
        hint = 'no matches'
      elif len(matches) <= 10:
        hint = " ".join(f'…{m}' for m in matches)
      else:
        hint = "too many matches"
    pwd = head + p + common + tail
    pos = len(pwd) - len(tail)
  return pwd, pos, hint


def ask(prompt, create=False):
  with fullscreen() as term:
    autohint = ''
    pwd = ''  # nosec
    pos = 0
    visible = False
    while True:
      if create:
        pwhint, valid = pwhints(pwd)
        pwhint += '\n' * max(0, 4 - pwhint.count('\n'))
        pwtitle, pwrest = pwhint.split('\n', 1)
      else:
        pwtitle, pwrest, valid = 'Covert decryption', '\n', True
      out = f"\x1B[1;1H\x1B[1;37;44m{pwtitle:56}\x1B[0m\n{pwrest}{prompt}: "
      pwdisp = pwd if visible else len(pwd) * '·'
      out += f"{pwdisp[:pos]}\x1B7{pwdisp[pos:]}"
      help = ''
      if pwd or not create:
        help += "\n  \x1B[1;34mtab  \x1B[0;34m"
        help += autohint or "autocomplete words"
        autohint = ''
        if valid:
          help += "\n\x1B[1;34menter  \x1B[0;34muse this password"
      else:
        help += "\n  \x1B[1;34mtab  \x1B[0;34msuggest a strong password\n\x1B[1;34menter  \x1B[0;34mgenerate and use a strong password"
      help += "\n \x1B[1;34mdown  \x1B[0;34mhide input" if visible else "\n   \x1B[1;34mup  \x1B[0;34mshow input"
      out += f'\n{help}\n\x1B[0m\x1B[K\x1B8'
      out = out.replace('\n', '\x1B[K\n')
      term.write(out)
      for ch in term.reader():
        if len(ch) == 1:  # Text input
          pwd = pwd[:pos] + ch + pwd[pos:]
          pos += 1
        if ch == "UP": visible = True
        if ch == "DOWN": visible = False
        elif ch == 'LEFT': pos = max(0, pos - 1)
        elif ch == 'RIGHT': pos = min(len(pwd), pos + 1)
        elif ch == 'HOME': pos = 0
        elif ch == 'END': pos = len(pwd)
        elif ch == "ENTER":
          if valid: return pwd, visible
          if create:
            pwd = generate()
            return pwd, True
        elif ch == "ESC":
          visible = not visible
        elif ch == "TAB":
          if create and not pwd:
            pwd = generate()
            pos = len(pwd)
            visible = True
          else:
            pwd, pos, autohint = autocomplete(pwd, pos)
        elif ch in ("BACKSPACE", "DEL"):
          if ch == "BACKSPACE":
            if pos == 0: continue
            pos -= 1
          pwd = pwd[:pos] + pwd[pos + 1:]


def pwhints(pwd):
  maxlen = 20  # zxcvbn gets slow with long passwords
  z = zxcvbn(pwd[:maxlen], user_inputs=argv)
  fb = z["feedback"]
  warn = fb["warning"]
  sugg = fb["suggestions"]
  guesses = float(z["guesses"])
  if len(pwd) > maxlen:
    # Account for characters we didn't let zxcvbn process
    guesses *= len(set(pwd))**(len(pwd) - maxlen)
    del sugg[:]
  # Estimate the time for our strong hashing (400 ms, 100 cores, 20 GB)
  t = .4 / 100 * guesses
  # Even stronger hashing of short passwords
  factor = 1 << max(0, 22 - 2 * len(pwd))
  t *= factor
  out = f"Estimated time to hack: {display_time(t)}\n"
  valid = True
  enclen = len(pwd.encode())
  if enclen < 8 or t < 600:
    out = "Choose a passphrase you don't use elsewhere.\n"
    valid = False
  elif factor != 1:
    with suppress(ValueError):
      sugg.remove('Add another word or two. Uncommon words are better.')
    sugg.append(f"Add some more and we can hash it {factor} times faster.")
  elif not sugg:
    sugg.append("Seems long enough, using the fastest hashing!")
  if warn:
    out += f" ⚠️   {warn}\n"
  for sugg in sugg[:3 - bool(warn)]:
    out += f" ▶️   {sugg}\n"
  return out, valid
