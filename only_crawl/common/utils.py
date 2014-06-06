import sys
import socket
import os
import threading

def urlopenWithRetry(opener, url, timeout = 10, retryTime = 3):
    while retryTime >= 0 :
        try:
            resp = opener.open(url, timeout=timeout)
            return resp.read()
        except socket.timeout, e1:
            retryTime -= 1 
            syslog("http timeout, retry again.(retry remains %s) url=%s" % (retryTime, url), LOG_ERROR)
            continue
        except Exception, e2:
            syslog(str(Exception) + ":" + str(e2) + ", at url=" + url, LOG_ERROR)
            break
    return None

def upDiv(a, b):
    return (a+b-1) / b

def getShardingConf(size, maxDownloadCount=20, perferedSplitNum=4):
    tmpCount = upDiv(size, perferedSplitNum)
    if tmpCount > maxDownloadCount:
        tmpCount = maxDownloadCount
    
    splitNum = upDiv(size, tmpCount)
    downloadCount = tmpCount
    return [splitNum, downloadCount]

def createDir(savePath):
    #create dir
    if os.path.isdir(savePath) is not True:
        os.makedirs(savePath)

#following from Python cookbook, #475186
def has_colours(stream):
    if not hasattr(stream, "isatty"):
        return False
    if not stream.isatty():
        return False # auto color only on TTYs
    try:
        import curses
        curses.setupterm()
        return curses.tigetnum("colors") > 2
    except:
        # guess false in case of error
        return False
has_colours = has_colours(sys.stdout)

#constant
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
LOG_DEBUG, LOG_INFO, LOG_WARNING, LOG_ERROR = range(4)
level_str = ["DEBUG", "INFO", "WARNING", "ERROR"]

def getLogColour(level):
    color_range = [WHITE, GREEN, YELLOW, RED]
    return color_range[level]

syslogLock = threading.Lock()

def syslog(text, level=LOG_INFO):
    syslogLock.acquire()
    if has_colours:
        seq = "\x1b[1;%dm" % (30+getLogColour(level)) + "[%s]: " % (level_str[level]) + "\x1b[0m"
        sys.stdout.write(seq)
        sys.stdout.write(text + "\n")
    else:
        sys.stdout.write(text + "\n")
    syslogLock.release()

def dynamicImport(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod