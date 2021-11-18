import os
import threading
import subprocess
from pathlib import Path
from colored import fg, attr

threads = []

def run_cmd(echo, cmd):
    t = threading.Thread(target=_run_cmd0, args=[echo, cmd])
    t.start()

    threads.append(t)

def _run_cmd0(echo, cmd):
    if echo:
        print(f"{fg(240)}{cmd}{attr('reset')}")

    with subprocess.Popen(str.split(cmd, " "), stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
        for line in process.stdout:
            print(line.decode('utf8'), end='')

def exec_goal(project, name, echo, _goal):
    if not _goal in project["goals"]:
        print(f"{fg(11)}Unknown goal {_goal}.{attr('reset')}")
        return

    goal = project["goals"][_goal]

    print(f"Executing goal \"{_goal}\" of project \"{name}\".")

    if "sources" in goal:
        ccmd = "gcc -c %i% -o %o% %f%"
        sources = []

        for x in goal["sources"]:
            if "*" in x:
                for path in Path(".").glob(x):
                    sources.append(path)
            else:
                sources.append(x)

        output = goal["output"]
        compiler = "gcc"

        if "compiler" in goal:
            if isinstance(goal["compiler"], dict):
                compiler = goal["compiler"]["name"]
                ccmd = goal["compiler"]["cmd"]
            else:
                compiler = goal["compiler"]

                if compiler == "gcc":
                    pass
                elif compiler == "g++":
                    ccmd = "g++ -c %i% -o %o% %f%"
                else:
                    print(f"{fg(11)}Unknown compiler \"{compiler}\".{attr('reset')}")

        linker = goal["linker"]
        cflags = ""
        ldflags = ""

        if "cflags" in goal:
            cflags = goal["cflags"]
        
        if "ldflags" in goal:
            ldflags = goal["ldflags"]

        if "before" in goal:
            for x in goal["before"]:
                if x in project["goals"]:
                    exec_goal(project, name, echo, x)
                else:
                    run_cmd(echo, x)

        for t in threads:
            if t.is_alive():
                t.join()
        
        threads.clear()
        outs = []

        # compile
        for x in sources:
            out = os.path.join(output, os.path.splitext(x)[0] + ".o")
            os.makedirs(os.path.dirname(out), exist_ok=True)

            final = ccmd.replace("%f%", cflags).replace("%i%", x).replace("%o%", out)

            run_cmd(echo, final)
            outs.append(out)

        for t in threads:
            if t.is_alive():
                t.join()
        
        threads.clear()

        # link
        run_cmd(echo, f"ld -T {linker} {ldflags + ' ' if ldflags != '' else ''}-o {os.path.join(output, name)} {str.join(' ', outs)}")

        if "after" in goal:
            for x in goal["after"]:
                if x in project["goals"]:
                    exec_goal(project, name, echo, x)
                else:
                    run_cmd(echo, x)
        
        for t in threads:
            if t.is_alive():
                t.join()
        
        threads.clear()
    else:
        cmd = goal["cmd"]
        
        if isinstance(cmd, list):
            for x in cmd:
                run_cmd(echo, x)
        else:
            run_cmd(echo, cmd)
