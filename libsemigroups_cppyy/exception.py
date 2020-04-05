"""
This file contains an exception class for capturing LibsemigroupsException's
emitted by cppyy and presenting them in a concise way.
"""


class LibsemigroupsCppyyException(Exception):
    def __init__(self, e):
        if isinstance(e, Exception):
            self.full_msg = str(e)
            first = self.full_msg.find("LibsemigroupsException")
            if first == -1:
                self.short_msg = self.full_msg
            else:
                last = self.full_msg.find("\n", first)
                self.short_msg = self.full_msg[first:last]
                self.short_msg = self.short_msg[self.short_msg.rfind(":") + 2 :]
        elif isinstance(e, str):
            self.short_msg = e
            self.full_msg = e
        else:
            raise TypeError(
                "the argument must be an Exception or str, not " + type(e).__name__
            )

    def __str__(self):
        return self.short_msg
