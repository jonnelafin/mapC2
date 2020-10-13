#Written By Elias Eskelinen aka "jonnelafin"
add_library('UiBooster')
import time

def toBin(val, original=-1):
    if val == "" or val == "None":
        val = "0"
    if "0x" in str(val) and int(val, 0) < 2147483646: #Max hex value
        bin = format(int(val, 0), '08b')
    else:
        bin = format(int(val), '08b')
    if len(bin) < original:
        bin = "0"*(original-len(bin)) + bin
    return bin
def toInt(val, doHex=True):
    if doHex:
        if int(val, 2) < 2147483646: #Max hex value
            return "0x" + hex(int(val, 2))
        print("Value is over the max hex value. Int will be used instead")
    return int(val, 2)
#print(toBin(101))

def parseMap(val, wsize, fsize = -1):
    out = ""
    ind = 0
    for i in toBin(val, fsize):
        if ind > wsize:
            out += "\n"
            ind = 0
        ind = ind + 1
        out = out + i
    return out
def pack(data, wsize, fsize):
    return str(wsize) + "#" + str(data) + "#" + str(fsize)
if __name__ == "__main__":
    map =  "010101010"
    mapw = 3


    #print("Map: " + map)
    enc = toInt(map)
    print("Encoded: " + str(enc))
    #print("Decoded raw: " + str(toBin(enc, len(map))))
    dec = parseMap(enc, mapw-1, len(map))
    print("Decoded map: \n" + str(dec))

    print()
    print(pack(enc, mapw, len(map)))
    
    c = ""
    s = ""
    w = 9
def genDat(subdiv):
    dat = {}
    for i in range(subdiv):
        for z in range(subdiv):
            dat[str([i,z])] = False
    return dat
def dataFromPacked(val, w, siz):
    dat = {}
    ind = 0
    x = -1
    y = 0
    print(toBin(val, siz))
    buff = ""
    aind = 0
    bin = toBin(val, siz)
    for i in bin:
        #print(y, x, i, aind)
        if ind > w:
            ind = 0
            x = 0
            y += 1
            #print(buff)
            buff = ""
        elif aind + 2 > siz:
            x += 1
            dat[str([x,y])] = (bin[aind] == "1")
            buff += bin[aind]
            #print(buff)
        else:
            x += 1
        buff += i
        ind = ind + 1
        aind += 1
        dat[str([x,y])] = (i == "1")
    return dat
def unpack(packd):
    subdiv = int(packd.split("#")[0].replace("#", ""))
    data = str(packd.split("#")[1].split("#")[0].replace("#", ""))
    fsize = int(packd.split("#")[2].replace("#", ""))
    return subdiv, data, fsize
def setup():
    size(500, 500)
    global subdivs, data, mDown, booster, asString
    subdivs = 5
    data = genDat(subdivs)#[[False]*subdivs]*subdivs
    print(data["[0, 0]"])
    mDown = False
    booster = UiBooster()
    #subdivs, data, yeets = unpack(booster.showTextInputDialog("Paste your mapcode here:"))
    #data = dataFromPacked(data, subdivs-1, yeets)
    #print(data)
    #print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
    asString = ""
    showInfo()
def draw():
    global mDown, data, asString
    background(150, 150, 150)
    for i in range(subdivs+1):
        line(width/subdivs*i, 0, width/subdivs*i, height)
        line(0, height/subdivs*i, width, height/subdivs*i)
    for i in range(subdivs):
        for z in range(subdivs):
            x = width/subdivs*i
            y = height/subdivs*z
            mx = mouseX - (width/subdivs/2)
            my = mouseY - (height/subdivs/2)
            
            pointer = str([i, z])
            dat = False
            try:
                dat = data[pointer]
            except Exception as e:
                data[pointer] = False
            if abs(mx - x) < (width/subdivs/2) and abs(my - y) < (height/subdivs/2):
                fill(255, 255, 255)
                rect(x, y, width/subdivs, height/subdivs)
                if mDown:
                    mDown = False
                    data[pointer] = not data[pointer]
                    m = genMap(data, subdivs)
                    en = toInt(m)
                    print(m)
                    print(en)
                    print(pack(en, subdivs, len(m)))
                    #print(parseMap(en, subdivs-1, len(m)))
            elif data[pointer] == True:
                fill(0, 255, 0)
                rect(x, y, width/subdivs, height/subdivs)
    fill(220, 0, 0)
    m = genMap(data, subdivs)
    en = toInt(m)
    asString = str(en)
    text(asString, 50, 50)
def mouseClicked(): 
    global mDown
    mDown = True
def keyPressed():
    global subdivs, data
    if str(key) in "123456789":
        subdivs = int(key)
    elif str(key) == "c":
        data = {}
    elif str(key) == "z":
        m = genMap(data, subdivs)
        en = toInt(m)
        code = pack(str(int(en, 0)-1), subdivs, len(m))
        print(code)
        subdivs, data, yeets = unpack(code);
        data = dataFromPacked(data, subdivs-1, yeets)
    elif str(key) == "x":
        m = genMap(data, subdivs)
        en = toInt(m)
        code = pack(str(int(en, 0)+1), subdivs, len(m))
        print(code)
        subdivs, data, yeets = unpack(code);
        data = dataFromPacked(data, subdivs-1, yeets)
    elif str(key) == "s" or str(key) == "o":
        m = genMap(data, subdivs)
        print(m)
        en = toInt(m)
        code = pack(str(en), subdivs, len(m))
        val = booster.showTextInputDialog("Current mapcode is " + code + "\nPaste new mapcode here:")
        if str(val) == "" or str(val) == "None":
            op = ""
        elif not checkCode(val):
            if checkCode(pack(val, subdivs, len(m))):
                val = pack(val, subdivs, len(m))
                print(val)
                subdivs, data, yeets = unpack(val)
                data = dataFromPacked(data, subdivs-1, yeets)
                print(data)
                print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
                print("Yeet")
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
        else:
            subdivs, data, yeets = unpack(val)
            data = dataFromPacked(data, subdivs-1, yeets)
            print(data)
            print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
    elif str(key) == "i":
        showInfo()
    elif str(key) == ",":
        subdivs -= 1
    elif str(key) == ".":
        subdivs += 1
def showInfo():
    booster.showInfoDialog("Welcome to mapC2!\n\nClick on tiles to flip their state.\nPress c to clear,\nz and x to modify the code directly,\no or s to save/load,\nnumbers from 1-9 to set the grid size and\i to show this dialogue.\n\nTo reset the export size to a lower value,\nyou must first reset data by pressing c.")
def checkCode(code):
    try:
        code = str(code)
        if len(str((code))) < 1:
            return False
        print("Code passed test 1")
        if not ("#" in code):
            return False
        print("Code passed test 2")
        if code.count("#") != 2:
            return False
        print("Code passed test 3")
        w, c, s = unpack(code)
        if s/w != w:
            print("Aspect ratio must match 1:1")
            return False
        print("Code passed test 4")
        return True
    except Exception as e:
        return False
def genMap(dat, subdiv):
    out = ""
    for i in range(subdiv):
        for z in range(subdiv):
            p = str([z, i])
            v = dat[p]
            if v == True:
                out += "1"
            else:
                out += "0"
    return out
