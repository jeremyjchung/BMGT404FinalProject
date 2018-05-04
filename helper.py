def secondsToTime(t):
    h = int(t / 3600)
    m = int((t - h * 3600) / 60)
    s = int(t - h * 3600 - m * 60)

    return "%02d:%02d:%02d" % (h, m, s)

def foodToStr(lst):
    return "\n".join(list(map(lambda x: x[0] + "\t\t" + str(x[1]), lst)))
