"""
This module provides a @concurrent decorator primitive to
offload computations from mitmproxy's main master thread.
"""

from eavesdropper.mitmproxy import eventsequence
from eavesdropper.mitmproxy.coretypes import basethread


class ScriptThread(basethread.BaseThread):
    name = "ScriptThread"


def concurrent(fn):
    if fn.__name__ not in eventsequence.Events - {"load", "configure"}:
        raise NotImplementedError(
            "Concurrent decorator not supported for '%s' method." % fn.__name__
        )

    def _concurrent(*args):
        # When annotating classmethods, "self" is passed as the first argument.
        # To support both class and static methods, we accept a variable number of arguments
        # and take the last one as our actual hook object.
        obj = args[-1]

        def run():
            fn(*args)
            if obj.reply.state == "taken":
                if not obj.reply.has_message:
                    obj.reply.ack()
                obj.reply.commit()
        obj.reply.take()
        ScriptThread(
            "script.concurrent (%s)" % fn.__name__,
            target=run
        ).start()

    return _concurrent
