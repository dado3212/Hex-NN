import time

# Timing functions
def timing(f):
  def wrap(*args):
    time1 = time.time()
    ret = f(*args)
    time2 = time.time()
    print '%s function took %s' % (f.func_name, handleTime((time2-time1)*1000.0))
    return ret
  return wrap

def handleTime(ms):
  if (ms < 2000):
    return "%0.3f ms" % (ms)
  elif (ms < 1000 * 60):
    return "%0.3f s" % (ms/1000.0)
  elif (ms < 1000 * 60 * 60):
    return "%0.2f min" % (ms/1000.0/60.0)
  else:
    return "%0.2f hrs" % (ms/1000.0/60.0/60.0)