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
    def Barva (databaze,cislo,figura):
        Charakteristika(databaze,cislo,figura,3)
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
        #print(numk)
        return numk
    #TahKralem("b4") #tes
    #input()

    #Kontrola obsazených polí - obecná
    def Kontrola(jaketahy,vsechnytahy,rozmisteni,barva):
        chcemetahy = []*len(vsechnytahy)
        if jaketahy == "neobsazene":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == False:
                    chcemetahy.append(vsechnytahy[i])
        elif jaketahy == "brani":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == (True,1): #opačná barva
                    chcemetahy.append(vsechnytahy[i])
        elif jaketahy == "nemozne":
            for i in range(len(vsechnytahy)):
                if Obsazene(vsechnytahy[i],rozmisteni,barva) == (True,0): #stejná barva
                    chcemetahy.append(vsechnytahy[i])
        else:
            print("Error - Jaké tahy?")
            input()
        return chcemetahy

    #Šablony pro tah králem
    
    def TahKralemSablona1(databaze, cislopozice, poradi): #bude vracet: všechny tahy, rozmístění, barvu
        return(TahKralem(Charakteristika(databaze,cislopozice,poradi,2)))
    def TahKralemSablona2(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,1))
    def TahKralemSablona3(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,3))
    def TahKralemSablonaFull(jaketahy,databaze,cislopozice,poradi):
        return(Kontrola(jaketahy,TahKralemSablona1(databaze, cislopozice, poradi),TahKralemSablona2(databaze, cislopozice, poradi),TahKralemSablona3(databaze, cislopozice, poradi)))

    def Test(cislo,figura):
        print (Rozmisteni(pozice,cislo))
        print ("Figura na poli ",Charakteristika(pozice,cislo,figura,2))
        print("Neobsazene:",TahKralemSablonaFull("neobsazene",pozice,cislo,figura))
        print("Brani:",TahKralemSablonaFull("brani",pozice,cislo, figura))
        print("Nemozne:",TahKralemSablonaFull("nemozne",pozice,cislo, figura))
    def TestObecne(cislo,figura):
        print (Rozmisteni(pozice,cislo))
        print ("Figura na poli ",Charakteristika(pozice,cislo,figura,2))
        print("Neobsazene:",TahXSablonaFull("neobsazene",pozice,cislo,figura))
        print("Brani:",TahXSablonaFull("brani",pozice,cislo, figura))
        print("Nemozne:",TahXSablonaFull("nemozne",pozice,cislo, figura))
    # Obecná šablona
    
    def TahXSablonaFull(jaketahy,databaze,cislopozice,poradi):
        if poradi == 0 or poradi == 1:
            return TahKralemSablonaFull(jaketahy,databaze,cislopozice,poradi)
        if poradi == 2:
            return TahVeziSablonaFull(jaketahy,databaze,cislopozice,poradi)
        
    #Šablony pro tah věží
        
    def TahVeziSablona1(databaze, cislopozice, poradi): #bude vracet: všechny tahy, rozmístění, barvu
        return(TahVezi(Charakteristika(databaze,cislopozice,poradi,2)))
    def TahVeziSablona2(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,1))
    def TahVeziSablona3(databaze, cislopozice, poradi):
        return(Charakteristika(databaze,cislopozice,poradi,3))
    def TahVeziSablonaFull(jaketahy,databaze,cislopozice,poradi):
        return(Kontrola(jaketahy,TahVeziSablona1(databaze, cislopozice, poradi),TahVeziSablona2(databaze, cislopozice, poradi),TahVeziSablona3(databaze, cislopozice, poradi)))
    
    #Další funkce
    def Vyhledejpole(databaze,poradi,pole):
        j = (databaze[poradi])[:]
        for i in range(len(j)):
            if j[i] == pole:
                return i
        return False
    def Brani(databaze,cislopozice,i): #později
        j = (databaze[cislopozice])[:]
        if i == 0 or i == 1:
            return TahKralemSablonaFull("brani",databaze,cislopozice,i)
        if i == 2:
            if j[2]!="X":
                return TahVeziSablonaFull("brani",databaze,cislopozice,i)
    #později
    #DOŘEŠIT

    #Jde-li král do šachu, pak se jedná o nemožný tah - dodělat!
    def DoSachuqm(databaze,cislopozice,seznamtahu,figura): #vždy se jedná o krále
        j = (databaze[cislopozice])[:]
        for i in range(len(seznamtahu)):
            j[figura] = seznamtahu[i] #první nebo druhá figura
            if j in databaze:
                p = databaze.find(j)
                print (p)
                print (Jesach(databaze,p))
                input()
                if figura == 0 and Jesach(databaze,p) == "Bily":
                    return
        return
    #později, až vyřeším přesun
    #Řeším, jestli je v dané pozici šach 
    def JeSach(databaze,cislopozice):
        sach = ""
        j = (databaze[cislopozice])[:]
        k = 0 #bílý král
        for i in range(1,len(j)):
            if j[i]!="X":
                if j[k] in Brani(databaze,cislopozice,i): #může-li být král sebrán figurou...
                    sach = "Bily"
                    break
        k = 1 #cerny kral
        for i in range(0,len(j)):
            if j[i]!="X":
                if j[k] in Brani(databaze,cislopozice,i): #totéž
                    if sach == "Bily":
                        return "Oba"
                    else:
                        return "Cerny"
        if sach == "Bily":
            return "Bily"
        else:
            return "Nikdo"
    #VĚŽ
    def TahVezi(umk): #umisteni veze
        if umk == "X":
            return 
        rada = int(umk[1])
        sloupec = desloupec(umk[0])
        n = 0
        numk = [None]*(radky+sloupce) #vez muze o neomezeny pocet poli jednim smerem 
        for i in range(-sloupce,sloupce):  #dozadu o tolik rad, na kolikate je (jednotky neresim, ZEFEKTIVNIT)
            if i !=0: 
                if sloupec +i <= sloupce and sloupec + i > 0:
                        numk[n] = [sloupec + i, rada]
                        numk[n] = NazevPole(numk[n])
                        n += 1
        for j in range(-radky,radky):
            if j!=0:   
                if rada + j <= radky and rada + j > 0:
                    numk[n] = [sloupec, rada+j]
                    numk[n] = NazevPole(numk[n])
                    n += 1
        #print (numk)
        OdmazKonec(numk)
        #print(numk)
        return numk
    #TahVezi("b4") #tes
    #input() 
            
            
    def testsach(cispoz,fig=0):
        for i in range(3):
            TestObecne(cispoz,i)
        if JeSach(pozice,cispoz) != "Nikdo":
                  input()
        print(JeSach(pozice,cispoz))
    for i in range(500,700):
        testsach(i)
    
    
Koncovka(4,4)
