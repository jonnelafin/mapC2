#Written By Elias Eskelinen aka "jonnelafin"
#Some examples:
# 10#89219024037939033406124925000#100
# 11#36764827488688866953459972691816448#121
# 5#0x00057DC4#25
# 6#0x12492780#36
# 7#1907373448064#49
#Full layers:
# 4#0x00000660#16N4#0x0000CC00#16N4#0x0000CA60#16N4#0x00000033#16N4#0x0000CA53#16N
#Math example:
#Try making a donut with the math function
# 5#0x000739C0#25
# 0x00001000
# select - as the operator

add_library('UiBooster')




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
supressHex = False
def toInt(val, doHex=True):
    global supressHex
    if doHex:
        if int(val, 2) < 2147483646: #Max hex value
            return "0x" + hex(int(val, 2))
        if not supressHex:
            print("Value is over the max hex value. Int will be used instead. This warning will be supressed on future uses of the function.")
            supressHex = True
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
#    print(toBin(val, siz))
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
    global subdivs, data, mDown, booster, asString, eGrid, eFill, layers, layern, layerSel
    layersn = 5
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
    eGrid = True
    eFill = True
    layers = []
    layern = 0
    for i in range(layersn):
        layers.append(genDat(subdivs))
    layerSel = False
    showInfo()
def draw():
    global mDown, data, asString, layers
    background(150, 150, 150)
    if eGrid:
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
                for li in range(len(layers)):
                    try:
                        lol = layers[li][pointer]
                    except Exception as e:
                        layers[li][pointer] = False
            if data[pointer] == True:
                fill(0, 255, 0)
                rect(x, y, width/subdivs, height/subdivs)
            if abs(mx - x) < (width/subdivs/2) and abs(my - y) < (height/subdivs/2):
                fill(255, 255, 255)
                if eFill:
                    rect(x, y, width/subdivs, height/subdivs)
                if mDown:
                    mDown = False
                    data[pointer] = not data[pointer]
                    m = genMap(data, subdivs)
                    en = toInt(m)
                    #print(m)
                    #print(en)
                    print(pack(en, subdivs, len(m)))
                    #print(parseMap(en, subdivs-1, len(m)))
    fill(220, 0, 0)
    layers[layern] = data
    m = genMap(data, subdivs)
    en = toInt(m)
    asString = str(en)
    text(asString, 50, 50)
    if layerSel:
        text("L", 12, 12)
def mouseClicked(): 
    global mDown
    mDown = True
def keyPressed():
    global subdivs, data, eGrid, eFill, layerSel
#    if str(key) in "123456789":
#        subdivs = int(key)
    if str(key) == "c":
        data = {}
        layers[layern] = {}
    elif str(key) == "z":
        m = genMap(data, subdivs)
        en = toInt(m)
        if "0x" in en:
            code = pack(str(int(en, 0)-1), subdivs, len(m))
        else:
            code = pack(str(int(en)-1), subdivs, len(m))
        subdivs, data, yeets = unpack(code);
        print(code)
        data = dataFromPacked(data, subdivs-1, yeets)
    elif str(key) == "x":
        m = genMap(data, subdivs)
        en = toInt(m)
        if "0x" in en:
            code = pack(str(int(en, 0)+1), subdivs, len(m))
        else:
            code = pack(str(int(en)+1), subdivs, len(m))
        subdivs, data, yeets = unpack(code);
        print(code)
        data = dataFromPacked(data, subdivs-1, yeets)
    elif (str(key) == "s" or str(key) == "o") and not layerSel:
        m = genMap(data, subdivs)
        print(m)
        en = toInt(m)
        code = pack(str(en), subdivs, len(m))
        print("Current mapcode is: " + code)
        print("Layers: ")
        all = ""
        indl = 0
        for l in layers:
            m = genMap(l, subdivs)
            en = toInt(m)
            code = pack(str(en), subdivs, len(m))
            all += code + "N"
            print("\tLayer " + str(indl) + ": " + code)
            indl += 1
        print("Combined code: " + all)
        val = booster.showTextInputDialog("Current mapcode is " + code + "\nPaste new mapcode here:")
        if str(val) == "" or str(val) == "None":
            op = ""
        elif not checkCode(val, True, True):
            if checkCode(val, False):#checkCode(pack(val, subdivs, len(m))):
                val = pack(val, subdivs, len(m))
#                print(val)
                subdivs, data, yeets = unpack(val)
                data = dataFromPacked(data, subdivs-1, yeets)
#                print(data)
#                print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
        else:
            subdivs, data, yeets = unpack(val)
            data = dataFromPacked(data, subdivs-1, yeets)
#            print(data)
#            print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
    elif (str(key) == "s" or str(key) == "o") and layerSel:
        m = genMap(data, subdivs)
        print(m)
        en = toInt(m)
        code = pack(str(en), subdivs, len(m))
        print("Current mapcode is: " + code)
        print("Layers: ")
        all = ""
        indl = 0
        for l in layers:
            m = genMap(l, subdivs)
            en = toInt(m)
            code = pack(str(en), subdivs, len(m))
            all += code + "N"
            print("\tLayer " + str(indl) + ": " + code)
            indl += 1
        print("Combined code: " + all)
        val = booster.showTextInputDialog("Current mapcode is " + code + "\nPaste new mapcode with all layers here:")
        if str(val) == "" or str(val) == "None":
            op = ""
        elif not checkCode(val, False, False, True):
            booster.showErrorDialog("Invalid mapcode!", "Error")
        else:
            indz = 0
            for i in val.split("N"):
                val2 = i.replace("N","")
                if val2 != "":
                    subdivs, dat, yeets = unpack(val2)
                    dat = dataFromPacked(dat, subdivs-1, yeets)
                    layers[indz] = dat
                    if indz == layern:
                        data = dat
                    indz += 1
#            print(data)
#            print(parseMap(toInt(genMap(data, subdivs)), subdivs, yeets))
    elif str(key) == "i":
        showInfo()
    elif str(key) == ",":
        subdivs = max(subdivs-1, 1)
    elif str(key) == ".":
        subdivs += 1
    elif str(key) == "g":
        eGrid = not eGrid
    elif str(key) == "f":
        eFill = not eFill
    elif str(key) == "m":
        math()
    elif str(key) == "b":
        bitwise()
    elif str(key) in "12345":
        layer(int(key)-1)
    elif str(key) == "l":
        layerSel = not layerSel
def showInfo():
    booster.showInfoDialog("Welcome to mapC2 by Jonnelafin!\n\nClick on tiles to flip their state.\nPress c to clear,\nz and x to modify the code directly,\no or s to save/load,\nm to use the math function, \nb to use the bitwise function, \nl to switch between using codes and layers for math, bitwise and load, \nnumbers from 1-9 to set the grid size, \nkeys e, r, t, y and u to switch layers and\ni to show this dialogue. \n\nMapcodes are easiest to copy from the console.\nGood Luck!")
def checkCode(code, full=True, silence=False, layrs = False):
    try:
        code = str(code)
        if len(str((code))) < 1:
            if not silence:
                print("E: Mapcode too short!")
            return False
#        print("Code passed test 1")
        if not ("#" in code) and (full or layrs):
            if not silence:
                print("E: A full mapcode should include \"#\"")
            return False
#        print("Code passed test 2")
        if code.count("#") != 2 and full:
            if not silence:
                print("E: A full mapcode should have 2 instances of #, this has " + str(code.count("#")))
            return False
#        print("Code passed test 3")
        if code.count("#") != 10 and layrs:
            if not silence:
                print("E: A full mapcode should have 10 instances of #, this has " + str(code.count("#")))
            return False
        if full:
            w, c, s = unpack(code)
            if s/w != w:
                if not silence:
                    print("E: Aspect ratio must match 1:1")
                return False
        else:
            c = code
#        print("Code passed test 4")
        if layrs:
            if not silence or True:
                print("Detected layer-dependent code.")
            for i in c:
                if not (i.lower() in "0123456789abcdefx#n"):
                    if not silence:
                        print("E: " + i.lower() + " is not hexadecimal!")
                    return False
        elif not ("0x" in c[:2]):
            if not silence or True:
                print("Detected numerical code.")
            for i in c:
                if not (i in "0123456789"):
                    if not silence:
                        print("E: " + i.lower() + " is not a number!")
                    return False
        else:
            if not silence or True:
                print("Detected hexadecimal code.")
            for i in c:
                if not (i.lower() in "0123456789abcdefx"):
                    if not silence:
                        print("E: " + i.lower() + " is not hexadecimal!")
                    return False
#        print("Code passed test 5")
        return True
    except Exception as e:
        return False
def math():
    #0x00421084
    #0x00007C00
    if not layerSel:
        retry = True
        while retry:
            valA = booster.showTextInputDialog("Type in value A:")
            if str(valA) == "None":
                return
            if checkCode(valA, False):
                retry = False
                break
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
        retry = True
        while retry:
            valB = booster.showTextInputDialog("Type in value B:")
            if str(valB) == "None":
                return
            if checkCode(valB, False):
                retry = False
                break
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
    else:
        valA = booster.showSelectionDialog("Please select layer A: ", "MapC2 - Math","1","2","3","4","5")
        if str(valA) == "None":
            return
        valB = booster.showSelectionDialog("Please select layer B: ", "MapC2 - Math","1","2","3","4","5")
        #print(valB)
        if str(valB) == "None":
            return
        mA = genMap(layers[int(valA)-1], subdivs)
#        print(m)
        valA = str(toInt(mA))
#        codeA = pack(str(en), subdivs, len(m))
        mB = genMap(layers[int(valB)-1], subdivs)
#        print(m)
        valB = str(toInt(mB))
#        codeA = pack(str(en), subdivs, len(m))
    op = booster.showSelectionDialog("Please select the operator: ", "MapC2 - Math", "+","-", "*", "/")
    
    if "0x" in valA[:2]:
        valA = int(valA, 0)
    else:
        valA = int(valA)
    if "0x" in valB[:2]:
        valB = int(valB, 0)
    else:
        valB = int(valB)
    
    code = ""
    print(str(valA)+op+str(valB))
    if op == "+":
        code = str(valA + valB)
    elif op == "-":
        code = str(valA - valB)
    elif op == "*":
        code = str(valA * valB)
    elif op == "/":
        code = str(valA / valB)
    
    global subdivs, data
    m = genMap(data, subdivs)
    
    val = pack(code, subdivs, len(m))
    print(val)
    subdivs, data, yeets = unpack(val)
    data = dataFromPacked(data, subdivs-1, yeets)
def bitwise():
    #0x00421084
    #0x00007C00
    if not layerSel:
        retry = True
        while retry:
            valA = booster.showTextInputDialog("Type in value A:")
            if str(valA) == "None":
                return
            if checkCode(valA, False):
                retry = False
                break
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
        retry = True
        while retry:
            valB = booster.showTextInputDialog("Type in value B:")
            if str(valB) == "None":
                return
            if checkCode(valB, False):
                retry = False
                break
            else:
                booster.showErrorDialog("Invalid mapcode!", "Error")
    else:
        valA = booster.showSelectionDialog("Please select layer A: ", "MapC2 - Bitwise","1","2","3","4","5")
        if str(valA) == "None":
            return
        valB = booster.showSelectionDialog("Please select layer B: ", "MapC2 - Bitwise","1","2","3","4","5")
        #print(valB)
        if str(valB) == "None":
            return
        mA = genMap(layers[int(valA)-1], subdivs)
#        print(m)
        valA = str(toInt(mA))
#        codeA = pack(str(en), subdivs, len(m))
        mB = genMap(layers[int(valB)-1], subdivs)
#        print(m)
        valB = str(toInt(mB))
#        codeA = pack(str(en), subdivs, len(m))
    op = booster.showSelectionDialog("Please select the operator: ", "MapC2 - Bitwise", "AND","OR", "NOT", "XOR")
    
    if "0x" in valA[:2]:
        valA = int(valA, 0)
    else:
        valA = int(valA)
    if "0x" in valB[:2]:
        valB = int(valB, 0)
    else:
        valB = int(valB)
    
    global subdivs, data
    m = genMap(data, subdivs)
    
    
    code = ""
    print(str(valA)+op+str(valB))
    if op == "AND":
        code = str(valA & valB)
    elif op == "OR":
        code = str(valA | valB)
    elif op == "NOT":
        code = str(-(~valA))
    elif op == "XOR":
        code = str(valA ^ valB)
    
    
    
    val = pack(code, subdivs, len(m))
    print(val)
    subdivs, data, yeets = unpack(val)
    data = dataFromPacked(data, subdivs-1, yeets)
def layer(num):
    global layers, layern, data
    layers[layern] = data
    layern = num
    data = layers[num]
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
