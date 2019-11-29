def Koncovka(rdk,slp):
    #ČÁST 1 - VYGENEROVÁNÍ ROZMĚRŮ ŠACHOVNICE A UMÍSTĚNÍ FIGUR NA POLE

    def sloupec(x): #napíšu číslo, vrátí písmeno
        return chr(ord("a")-1+x)
    def desloupec(x): #písmeno sloupce na číslo
        return ord(x)+1-ord("a")
    def SouradnicePole(x):#string na dvojici
        j = [0,0]
        j[0] = desloupec(x[0])
        j[1] = int(x[1])
        return j
    def NazevPole(x):#dvojici na string
        return str(sloupec(x[0]))+str(x[1])
    #print(NazevPole([4,2]))
    #print(SouradnicePole("c5"))
    #input()
    def Pis(nazev,pozice,radky,sloupce):
        sou = str(nazev)+str(radky)+"x"+str(sloupce)+".txt"
        print("Otviram soubor ",sou)
        soubor = open(sou,"w") #uložíme do souboru
        for k in range(len((pozice))):
            soubor.write(str(pozice[k]))
            soubor.write("\n")
        soubor.close()
        print("Zapsano do souboru ",sou)

    def OdmazKonec(seznam):
        while seznam[len(seznam)-1] == None:
            seznam.pop()

    #rozmerytxt = open("rozmery.txt","r")
    #rozmery = rozmerytxt.read()

    #radky = int(input("Rozměry šachovnice v řádcích (3 - 15): "))
    #sloupce = int(input("Rozměry šachovnice ve sloupcích(3 - 15): "))
    radky = rdk
    sloupce = slp
    maxsloupec = sloupec(sloupce)
    maxradek = radky
    print ("Rohy: a1, ",maxsloupec,"1, ",maxsloupec,maxradek,", a",maxradek,sep="") 

    #GENEROVÁNÍ FIGUR
    pocetfigur = 3
    #seznam figur
    pozice=[]
    Kb = None
    Kc = None
    V = None
    #for i in range(1,radky+1):
        #for j in range(1,sloupce+1):
    pozice.append([Kb,Kc,V])
    #print (pozice)
    vsechnypozice = []

    #pozice - seznam všech pozic
    #zkouma - parametry poli zleva doprava
    #Obecně funkce rozmistění
    def umisti(pozice,n):
        zkouma = pozice[n][:] #seznam postaveni
        i = 0
        while zkouma[i] != None: #prvni neumistena figura
            i += 1
        
        #vytvoří celý seznam, z něj vymaže figury na stejných polích
        zkouma[i] = "X" #figura není umístěna na žádném poli
        pozice[n] = zkouma[:] #nahrazujeme první instanci v seznamu, zbytek budeme přidávat
        for k in range(1,radky+1): #projdeme všechna pole šachovnice
            for j in range(1,sloupce+1):
                if (sloupec(j)+str(k)) not in zkouma: #pole není obsazeno 
                    zkouma[i] = (sloupec(j)+str(k)) #a1, b1, c1...
                #print(zkouma)
                zkoumacopy = zkouma[:]
                pozice.append(zkoumacopy)
        #print (vsechnypozice)
    #for i in range(len(pozice)):
    umisti(pozice,0)
    #print (pozice)

    #zopakuji postup pro všechny další figury, přičemž zachovávám i možnost, kdy všechny fugury nebudou na šachovnici
    for k in range(pocetfigur-1):
        for i in range(len(pozice)):
            umisti(pozice,i)
    Pis("vsechnypozice",pozice,radky,sloupce)
    ###ČÁST 2 - ZRUŠENÍ NELEGÁLNÍCH POZIC

    # figury na stejných polích - vyřešeno při generování figur

    # hrajeme bez krále
    def BezKral(pozice):
        novepozice=[]
        for x in range(len(pozice)):
            j = (pozice[x])[:]
            if j[0] != "X" and j[1] != "X":
                novepozice.append(j)
        return novepozice
    pozice = BezKral(pozice)
    Pis("jenpoziceskrali",pozice,radky,sloupce)

    #pozice s králi vedle sebe (jediná explicitně zadaná nemožná pozice, všechny ostatní budou založeny na možnosti tahu)
    def VedleKral(pozice):
        novepozice=[]
        for x in range(len(pozice)):
            j = (pozice[x])[:]
            bk = (j[0])[:]
            ck = (j[1])[:] #umístění bílého a černého krále, rozdíl mezi řadou a sloupcem musí být větší než 1 alespoň u jednoho parametru
            if abs((ord(bk[0])-ord(ck[0])))>1 or abs((int(bk[1])-int(ck[1])))>1:
                novepozice.append(j)
        return novepozice
    pozice = VedleKral(pozice)
    Pis("pozicekdesekralovenenapadaji",pozice,radky,sloupce)
    ### ČÁST 3 - MOŽNÉ TAHY (definice)
    
        #Na neobsazené pole - obecně
    def Obsazene(CilPole,Rozmisteni,barva):
        for i in range(len(Rozmisteni)):
            if Rozmisteni[i] == CilPole:
                return (True,(barva+i%2)%2) #i%2 - barva kamene (sudá/lichá) #bílé 0, černé 1; 1=opačné, 0 nebo 2 = stejné
        return False #pole není obsazeno
    def Charakteristika(databaze,cislo,figura,cochcu): #pozice,poradi,cislofig
        j = (databaze[cislo])[:] #jedna pozice
        k = (j[figura])[:] #pole
        n = figura %2 #barva
        if cochcu == 1:
            return j
        elif cochcu == 2:
            return k
        elif cochcu == 3:
            return n
    def Rozmisteni(databaze,cislo):
        return databaze[cislo]
    #KRÁL
    
    #Všechny tahy
    
    def TahKralem(umk): #umisteni krale
        rada = int(umk[1])
        sloupec = desloupec(umk[0])
        n = 0
        numk = [None]*8
        for i in range(-1,2):
            for j in range(-1,2):
                if i !=0 or j!=0:
                    if sloupec +i <= sloupce and sloupec + i > 0:
                        if rada + j <= radky and rada + j > 0:
                          numk[n] = [sloupec + i, rada + j]
                          numk[n] = NazevPole(numk[n])
                          n += 1
                  
        #print (numk)
        OdmazKonec(numk)
        print(numk)
        return numk
    #TahKralem("b4") #tes
    #input()

    #Kontrola obsazených polí
    def Kontrola(jaketahy,vsechnytahy,rozmisteni,barva):
        chcemetahy = []*len(vsechnytahy)
        if jaketahy == "neobsazene":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == False:
                    chcemetahy.append(vsechnytahy[i])
        elif jaketahy == "brani":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == (True,1):
                    chcemetahy.append(vsechnytahy[i])
        elif jaketahy == "nemozne":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == (True,0):
                    chcemetahy.append(vsechnytahy[i])
        else:
            print("Error - Jaké tahy?")
            input()
        return chcemetahy
    def TahKralemSablona1(databaze, cislopozice, poradi): #bude vracet: všechny tahy, rozmístění, barvu
        return(TahKralem(Charakteristika(databaze,cislopozice,poradi,2)))
    def TahKralemSablona2(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,1))
    def TahKralemSablona3(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,3))
    def TahKralemSablonaFull(jaketahy,databaze,cislopozice,poradi):
        return(Kontrola(jaketahy,TahKralemSablona1(databaze, cislopozice, poradi),TahKralemSablona2(databaze, cislopozice, poradi),TahKralemSablona3(databaze, cislopozice, poradi)))
    print (Rozmisteni(pozice,515))
    print(TahKralemSablonaFull("neobsazene",pozice,515,0))
Koncovka(4,4)
