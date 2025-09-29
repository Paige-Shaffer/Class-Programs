import pathlib

def getTimestamps(filename):
    fname = pathlib.Path(filename)
    stats = fname.stat()
    if not fname.exists(): 
        return []
    return(stats.st_ctime,stats.st_mtime,stats.st_atime)

def createDecoyFiles(filenames):
    with open("SneakersDecoys.txt","w") as f:
        for file in filenames:
            (ctime, mtime, atime) = getTimestamps(file)
            f.write("%s,%s,%s,%s\n" % (file,ctime,mtime,atime))

decoys = [r"Honey/Sneakers1.txt",r"Honey/Sneakers2.txt", r"Honey/Sneakers3.txt", r"Honey/Sneakers4.txt", r"Honey/Sneakers5.txt", r"Honey/Sneakers6.txt"]
createDecoyFiles(decoys)
