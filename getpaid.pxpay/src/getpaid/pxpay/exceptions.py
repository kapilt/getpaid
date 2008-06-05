import os

class PXPayException(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        if type(self.err) is dict:
            return os.linesep.join([' : '.join(x) \
                                    for x in self.err.items()])
        else:
            return repr(self.err)


class PXPayInvalidMessageException(PXPayException):
    pass

