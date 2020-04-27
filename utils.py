def parseSP500fromWikiPedia():
    lines = open('SP500 List.txt', 'r').readlines()
    symbList = []
    symbDict = {}
    for line in lines:
        symb = line.split('	')[0]
        symbList.append(symb)
        symbDict[symb] = line.split('\t')[1::]
    print(symbDict)
    fout = open('SP500OUT.py', 'w')
    fout.write(str('symbList = '+str(symbList) + '\n'))
    fout.write(str('symbDict = '+str(symbDict)))
