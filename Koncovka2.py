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
        #Pis("vsechnypozice",pozice,radky,sloupce)

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
        #Pis("jenpoziceskrali",pozice,radky,sloupce)

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
        return pozice
    def Rozmnoz(databaze): #rozmnoží databázi podle toho, kdo je na tahu, a také ke každé pozici napíše, kolik tahů zbývá do matu (None = nevíme)
        for i in range(len(databaze)):
            k = (databaze[i])[:]
            databaze[i].append("BNT") #bílý na tahu
            databaze[i].append(None)
            k.append("CNT")
            k.append(None)
            databaze.append(k) #přidá pozici s černým na tahu na konec DTB
            #Mohl bych nyní i eliminovat pozice, kde je na tahu strana dávající šach - to však vyžaduje testování funkce "JeSach", kde nároky mohou být velké (věž se může pohybovat na (řádky+sloupce) polí, a toto bych musel ověřit u každé pozice).
        return databaze
    def Redukuj(databaze): #zruší opakování
        databazen = [] #nová dtb
        for i in range(len(databaze)-1):
            if databaze[i] == databaze[i+1]: #pokud jsou dvě pozice stejné, zapisuju tu DALŠÍ
                continue
            else:
                databazen.append(databaze[i])
        databazen.append(databaze[len(databaze)-1]) #poslední pozici nemůžu s ničím porovnávat
        databaze = [] #zahodím
        return databazen

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
            return []
        rada = int(umisteni[1])
        sloupec = desloupec(umisteni[0])
        n = 0
        tahy = [None]*(radky-1+sloupce-1) #vez muze o neomezeny pocet poli jednim smerem 
        for i in range(-(sloupec-1),sloupce-sloupec):  #dozadu o tolik rad, na kolikate je (jednotky neresim, ZEFEKTIVNIT)
            if i !=0: 
                if sloupec +i <= sloupce and sloupec + i > 0:
                        tahy[n] = [sloupec + i, rada]
                        tahy[n] = NazevPole(tahy[n])
                        n += 1
        for j in range(-(rada-1),radky-rada):
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
                if r[i] in j: #jestli na daném místě je nějaká figura
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
    def TahyObec(databaze,cislo,figura): #tahy nikoli neomezené, ale neřeším legalitu
        if figura == 0 or figura == 1:
            return TahKralem(Polefigury(databaze,cislo,figura)) #vrací list
        elif figura == 2:
            return MuzeVez(databaze,cislo,figura) #vrací list
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
        #print (blokrada)

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
        #print (blok)
        return blok

    #Legální tahy

    #Věž

    def MuzeVez(databaze,cislo,figura):
        zakaz = BlokVezi(databaze,cislo,figura)+Charak(databaze,cislo,figura,"vlas")
        return (list(set(TahyNeom(databaze,cislo,figura)) - set(zakaz))) #všechny tahy - zakázané tahy; použit rozdíl množin

    def BraniVez(databaze,cislo,figura):
        br = [""]
        j = Charak(databaze,cislo,figura,"soup")
        k = MuzeVez(databaze,cislo,figura)
        for i in range(len(j)):
            if j[i] in k:
                br.append(j[i])
        return br
    #Král
    
    def LegalKral(databaze,cislo,figura):
        j = (TahyNeom(databaze,cislo,figura))[:] #seznam všech tahů
        zakaz = []
        for i in range(len(j)):
            if DoSachu(databaze,cislo,figura,j[i]) == True:
                zakaz.append(j[i])
        zakaz = zakaz+Charak(databaze,cislo,figura,"vlas")
        return (list(set(TahyNeom(databaze,cislo,figura)) - set(zakaz)))
    
    def DoSachu(databaze,cislo,figura,tah):
        if Presunpozice(databaze,cislo,figura,tah) in databaze:
            if figura == 1: #cerny tahne
                if JeSach(databaze,databaze.index(Presunpozice(databaze,cislo,figura,tah))) in ["Cerny","Oba"]:
                    return True
            elif figura == 0: #bily tahne
                if JeSach(databaze,databaze.index(Presunpozice(databaze,cislo,figura,tah))) in ["Bily","Oba"]: #SPRAVIT CHYBU
                    return True
            return False
        else:
            return True
    def BraniKral(databaze,cislo,figura):
        br = []
        j = Charak(databaze,cislo,figura,"soup")
        k = TahyNeom(databaze,cislo,figura)
        for i in range(len(j)):
            if j[i] in k:
                br.append(j[i])
        return br
    def Brani(databaze,cislo,figura):
        if figura == 0 or figura == 1:
            return BraniKral(databaze,cislo,figura)
        elif figura == 2:
            if figura  == "X":
                return
            return BraniVez(databaze,cislo,figura)
    #Je šach?
    def JeSach(databaze,cislopozice):
        sach = ""
        j = (databaze[cislopozice])[:]
        k = 0 #bílý král
        for i in range(1,len(j)-2,2): #step 2 - jen figury opačné barvy
            x = Brani(databaze,cislopozice,i)
            if j[i]!="X": #podmínky existence
                if x:
                    if j[k] in x: #může-li být král sebrán figurou, i pokud nemůže táhnout kvůli šachu (proto neřeším legalitu - ta je založena na pravidlu "Je šach" a proto by se mi podmínky zacyklily).
                        sach = "Bily"
                        break
        k = 1 #cerny kral
        for i in range(0,len(j)-2,2): #step 2 - jen figury opačné barva
            if j[i]!="X":
                x = Brani(databaze,cislopozice,i)
                if x:
                    if j[k] in x: #totéž
                        if sach == "Bily":
                            return "Oba"
                        else:
                            return "Cerny"
        if sach == "Bily":
            return "Bily"
        else:
            return "Nikdo"
    def JeMat(databaze,cislopozice):
        #nemám dodefinované braní
        j = databaze[cislopozice]
        if JeSach (databaze,cislopozice) == "Cerny":
            for i in range(1,len(j)-2,2):
                k = TahyObec(databaze,cislopozice,i) #list cílových polí
                for n in range(len(k)):
                    r =  Presunpozice(databaze,cislopozice,i,k[n]) #pozice vzniklá přesunutím jedné figury
                    if r in databaze:
                        v = databaze.index(r) #číslo pozice
                        if JeSach (databaze,v) == "Cerny":
                            continue
                        else:
                            return "Není" #není mat
                    else: #nelegální pozice, není v DTB
                        continue
            return "Cerny"
        elif JeSach (databaze,cislopozice == "Bily"):
            for i in range(0,len(j)-2,2):
                k = TahyObec(databaze,cislopozice,i) #list cílových polí
                for n in range(len(k)):
                    r =  Presunpozice(databaze,cislopozice,i,k[n]) #pozice vzniklá přesunutím jedné figury
                    if r in databaze:
                        v = databaze.index(r) #číslo pozice
                        if JeSach (databaze,v) == "Cerny":
                            continue
                        else:
                            return "Není" #není mat
                    else: #nelegální pozice, není v DTB
                        continue
            return "Bily"

    #4. PŘESUN
    def Finalpozice(databaze,cislo,figura,pole):
        #Je tah legální(v seznamu možných tahů)?
        if figura == 0 or figura == 1:
            if pole in LegalKral(databaze,cislo,figura):
                j = (databaze[cislo])[:]
                j[figura] = pole
            else:
                return "Nelegalni"
        elif figura == 2:
            if figura  == "X":
                return
            if pole in MuzeVez(databaze,cislo,figura):
                j = (databaze[cislo])[:]
                j[figura] = pole
            else:
                return "Nelegalni"
        return j
    def Presunpozice(databaze,cislo,figura,pole): #Narozdíl od Finalpozice toto pouze řeší vzniknutí nové pozice přesunutím dané figury
        j = (databaze[cislo])[:]
        j[figura] = pole
        return j
    #Které pozice mohou vzniknout? (obecně ty, které obsahují ostatní figury na stejných místech)
    


    #CESTA OD MATU - NEJTĚŽŠÍ
    #referenční 74,79
    def Matovanicislo1(databaze):
        for i in range(len(databaze)//2,len(databaze)):
            h = databaze[i]
            if JeMat(databaze,i) == "Cerny":
                j = databaze[i]
                if j[3] == "CNT": #černý musí být na tahu, aby dostal mat
                   j[4] = 0 #je mat, tzn. zbývá 0 tahů do matu
            return i #vrátí číslo pozice, s kterou budem pracovat











    #TESTOVÉ PROGRAMY
    pozice = Generuj() #pro skutečné zapsání souboru
    pozice = Redukuj(pozice)
    Rozmnoz(pozice)
    Pis("legalpozice",pozice,radky,sloupce)
    def Test(databaze,cislo):
        print (Celapozice(databaze,cislo))
        def Testuplne(databaze,cislo):
            print (Charak(databaze,cislo,2,"vse"))
            print (Charak(databaze,cislo,2,"praz"))
            print (Charak(databaze,cislo,2,"soup"))
            print (Charak(databaze,cislo,2,"vlas"))
            print (Charak(databaze,cislo,2,"obsa"))
        Testuplne(databaze,cislo)
    #Test(pozice,725)
    #input("...")
    #print(JeSach(pozice,725))
    
    def CharakterSachy(databaze): #příliš náročné - musí prověřit všechny tahy, jestli žádný není šach, tzn. je lepší situaci řešit až na místě (až se k pozici dostanu)
        x = 5
        for i in range(len(databaze)):
            databaze[i].append(JeSach(databaze,i))
            if i == (len(databaze)//100)*x:
                print (100*i//len(databaze),"%")
                x += 5


    #CharakterSachy(pozice) #zrušit
    #Pis("Pozice",pozice,radky,sloupce) #taktéž
    #Pozice jsou uložené o řádek níž, takže při pozici z řádku 721 zadávej číslo 720
    #Test(pozice,863)
    print(JeSach(pozice,78))
    print(JeMat(pozice,78))
    Matovanicislo1(pozice)
Koncovka(3,3) #max 29 sloupců, kvůli znakům



