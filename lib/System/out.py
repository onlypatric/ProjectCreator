import sys;

def print(x:object,flush:bool=False):
    sys.stdout.write(x.__str__())
    if flush:
        sys.stdout.flush()
def println(x:object):
    sys.stdout.write("%s%s"%(x.__str__(),"\n"))
