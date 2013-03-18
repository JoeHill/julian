import traceback

class SentinelValue:
    pass

UNDEFINED = SentinelValue()

def print_errors_and_exit(errors):
    if errors:
        for err in errors:
            print err[1]
            for t in traceback.extract_tb(err[2]):
                print t
        assert False
