import datetime
import os


def listdir_sorted(path=""):
    list_sorted = []
    files = os.listdir(path)
    for file in files:
        if (".png" in file) or (".jpg" in file):
            list_sorted.append(file)
    return sorted(list_sorted)


def jpg2png(name):
    return name.replace(".jpg", ".png")


def mkdir(path="", name=""):
    try:
        os.mkdir("{}{}".format(path,
                               name))
    except FileExistsError:
        pass
