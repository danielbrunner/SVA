

def read_txt(path):
    f = open(path, "r")
    list_prefs=f.read()
    return list_prefs.split("\n")[1:],list_prefs.split("\n")[0]



