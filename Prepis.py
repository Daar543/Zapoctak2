def Koncovka(rdk,slp):
    #ORIENTACE NA ŠACHOVNICI

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


    #ZÁPIS DO SOUBORU
    def Pis(nazev,pozice,radky,sloupce):
        sou = str(nazev)+str(radky)+"x"+str(sloupce)+".txt"
        print("Otviram soubor ",sou)
        soubor = open(sou,"w") #uložíme do souboru
        for k in range(len((pozice))):
            soubor.write(str(pozice[k]))
            soubor.write("\n")
        soubor.close()
        print("Zapsano do souboru ",sou)
    
    #ROZMĚRY
    radky = rdk
    sloupce = slp
    maxsloupec = sloupec(sloupce)
    maxradek = radky



    #GENEROVÁNÍ FIGUR
    def Generuj():
        pocetfigur = 3
        #seznam figur
        pozice=[]
        Kb = None
        Kc = None
        V = None
        pozice.append([Kb,Kc,V])   #pozice bez figur
        vsechnypozice = []

        #Obecně funkce rozmistění
        def umisti(pozice,n):
            zkouma = pozice[n][:] #jedna pozice
            i = 0
            while zkouma[i] != None: #prvni neumistena figura
                i += 1
        
            #vytvoří celý seznam, z něj vymaže figury na stejných polích
            zkouma[i] = "X" #figura není umístěna na žádném poli
            pozice[n] = zkouma[:] #nahrazujeme první instanci v seznamu (tzn. smažeme pozici s nedefinovaným umístěním figury) zbytek budeme přidávat, čímž se velikost seznamu rozšíří
            for k in range(1,radky+1): #projdeme všechna pole šachovnice
                for j in range(1,sloupce+1):
                    if (sloupec(j)+str(k)) not in zkouma: #pole není obsazeno 
                        zkouma[i] = (sloupec(j)+str(k)) #a1, b1, c1...
                    #print(zkouma)
                    zkoumacopy = zkouma[:]
                    pozice.append(zkoumacopy)
        umisti(pozice,0)
        #zopakuji postup pro všechny další figury, přičemž zachovávám i možnost, kdy všechny fugury nebudou na šachovnici
        for k in range(pocetfigur-1):
            for i in range(len(pozice)):
                umisti(pozice,i)
        Pis("vsechnypozice",pozice,radky,sloupce)

        #ZRUŠENÍ NELEGÁLNÍCH POZIC

        # figury na stejných polích - vyřešeno při generování figur

        # hrajeme bez krále
        def BezKral(pozice): 
            novepozice=[] #napsat nový seznam je jednodušší než odstraňovat prvky a přepisovat indexy ve starém seznamu (výjimka je odstranění posledního prvku)
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
        return pozice

    #ROZDĚLENÍ POLÍ - OBSAZENÉ, NEOBSAZENÉ
    def Obsazene(CilPole,Rozmisteni): #které pole; kde stojí figury
        for i in range(len(Rozmisteni)):
            if Rozmisteni[i] == CilPole:
                return i%2 #i%2 - barva kamene (sudá/lichá) #bílé 0, černé 1
        return -1 #pole není obsazeno
    

    #SEZNAM MOŽNÝCH TAHŮ
    def OdmazKonec(seznam):
        while seznam[len(seznam)-1] == None:
            seznam.pop()

    #NA PRÁZDNÉ ŠACHOVNICI

    #King
    def TahKralem(umisteni): #umisteni krale
        rada = int(umisteni[1])
        sloupec = desloupec(umisteni[0])
        n = 0
        tahy = [None]*8
        for i in range(-1,2):
            for j in range(-1,2):
                if i !=0 or j!=0:
                    if sloupec +i <= sloupce and sloupec + i > 0:
                        if rada + j <= radky and rada + j > 0:
                          tahy[n] = [sloupec + i, rada + j]
                          tahy[n] = NazevPole(tahy[n])
                          n += 1
        OdmazKonec(tahy)
        return tahy

    #Věž
    def TahVezi(umisteni): #umisteni veze
        if umisteni == "X":
            return 
        rada = int(umisteni[1])
        sloupec = desloupec(umisteni[0])
        n = 0
        tahy = [None]*(radky+sloupce) #vez muze o neomezeny pocet poli jednim smerem 
        for i in range(-sloupce,sloupce):  #dozadu o tolik rad, na kolikate je (jednotky neresim, ZEFEKTIVNIT)
            if i !=0: 
                if sloupec +i <= sloupce and sloupec + i > 0:
                        tahy[n] = [sloupec + i, rada]
                        tahy[n] = NazevPole(tahy[n])
                        n += 1
        for j in range(-radky,radky):
            if j!=0:   
                if rada + j <= radky and rada + j > 0:
                    tahy[n] = [sloupec, rada+j]
                    tahy[n] = NazevPole(tahy[n])
                    n += 1
        OdmazKonec(tahy)
        return tahy

    #CO JE NA CÍLOVÝCH POLÍCH
    def Napada(databaze,cislo,figura,pole):
        if pole in TahyNeom(databaze,cislo,figura,pole):
            return True
        return False

    #Rozdělení polí
    def Charak(databaze,cislo,figura,co): #co bude text
        vysledek = []
        j = Celapozice(databaze,cislo)
        r = TahyNeom(databaze,cislo,figura) # r - všechna pole
        if co == "praz":
            for i in range(len(r)):
                if r[i] not in j: #jestli na daném místě není žádná figura
                    vysledek.append(r[i])
        elif co == "soup": #soupeřova
            for i in range(len(r)):
                if r[i] in j: #jestli na daném místě je nějaká figura
                    if (j.index(r[i]))%2 != Barvafigury(figura): #odlišná barva
                        vysledek.append(r[i])
        elif co == "vlas": #vlastni
            for i in range(len(r)):
                if r[i] in j: #jestli na daném místě je nějaká figura
                    if (j.index(r[i]))%2 == Barvafigury(figura): #stejná barva
                        vysledek.append(r[i])
        elif co == "obsa": #jakákoli cizí
            for i in range(len(r)):
                if r[i] in j: #jestli na daném místě je nějaká žádná figura
                    vysledek.append(r[i])
        elif co == "vse": #všechna pole
            f = r[:]
            return f
        return vysledek
    def TahyNeom(databaze,cislo,figura):
        if figura == 0 or figura == 1:
            return TahKralem(Polefigury(databaze,cislo,figura))
        elif figura == 2:
            return TahVezi(Polefigury(databaze,cislo,figura))
        return
    #VYHLEDÁVACÍ FUNKCE
    def Celapozice(databaze,cislo):
        return databaze[cislo]
    def Polefigury(databaze,cislo,index):
        return ((Celapozice(databaze,cislo))[index])
    def Barvafigury(index):
        return (index%2)

    #PŘESKOČIT OBSAZENÁ POLE - VĚŽ
    def BlokVezi(databaze,cislo,index): #mám dvě skupiny: blokovaná a všechna možná pole, všechna ostatní pole na šachovnici můžu ignorovat
        obs = Charak(databaze,cislo,index,"obsa") #blok
        vse = TahyNeom(databaze,cislo,index) #možná
        #můžu využít toho, že věž se pohybuje jenom po řadě nebo sloupci, takže rozdělím na dva případy
        rad = [] #stejná řada, mění se sloupec
        sloup = [] #stejný sloupec, mění se řada
        j = vse[0] 
        #jedná se o první pole, kam může naše věž 
        for i in range(len(obs)):
            k = obs[i]
            if k[1] == j[1]: #index řady
                rad.append(k) #je-li zakázané pole na stejné řadě jako věž, řadí se do první skupiny, jinak (je na stejném sloupci) se řadí do druhé skupiny
            else:
                sloup.append(k) #jiný případ nemůže nastat
        #print ("Blokrada:",rad)
        #print ("Bloksloup:",sloup)

        #Je-li pole blokované, pak musí být všechna pole za ním nepřístupná
        u = Polefigury(databaze,cislo,index)

        blokrada = []
        for i in range(len(rad)): #je to na řadě, ale mění se SLOUPEC
            j = rad[i]
            j = desloupec(j[0])
            if desloupec(u[0]) < j: #figura je nalevo, ruší se pole napravo
                for k in range(j+1,sloupce+1):
                    blokrada.append(sloupec(k)+u[1]) #seznam polí
            elif desloupec(u[0]) > j: #figura je napravo, ruší se pole nalevo
                for k in range(1,j):
                    blokrada.append(sloupec(k)+u[1]) #seznam polí
        print (blokrada)

        bloksloupec = []
        for i in range(len(sloup)):
            j = sloup[i]
            j = int(j[1])
            if int(u[1]) < j: #figura je dole, ruší se pole nad
                for k in range(j+1,radky+1):
                    bloksloupec.append(u[0]+str(k))
            elif int(u[1]) > j: #figura je nahoře, ruší se pole pod
                for k in range (1,j):
                    bloksloupec.append(u[0]+str(k))
        blok = blokrada + bloksloupec
        print (blok)
        return blok


















    #TESTOVÉ PROGRAMY
    pozice = Generuj()
    def Test(databaze,cislo):
        print (Celapozice(databaze,cislo))
        def Testuplne(databaze,cislo):
            print (Charak(databaze,cislo,2,"vse"))
            print (Charak(databaze,cislo,2,"praz"))
            print (Charak(databaze,cislo,2,"soup"))
            print (Charak(databaze,cislo,2,"vlas"))
            print (Charak(databaze,cislo,2,"obsa"))
        Testuplne(databaze,cislo)
    #Pozice jsou uložené o řádek níž, takže při pozici z řádku 721 zadávej číslo 720
    Test(pozice,863)
    BlokVezi(pozice,863,2)
Koncovka(4,4)

