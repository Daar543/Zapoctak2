#ČTENÍ SOUBORU
#HLAVNÍ PROGRAM - NULOVÉ POZICE
import cProfile
from sys import getsizeof
from matplotlib import pyplot as plt
from copy import deepcopy #na nezávislé kopírování seznamů
import time
import random


def Profil():
    def RealSort(seznam): #seznam, kde některé hodnoty nejsou vzájemně porovnatelné, proto to převedu na číselnou rsp. písemnou hodnotu
        for i in range(len(seznam)):
            if seznam[i][2] == "X":
                seznam[i][2] = chr(ord("a")-1)
            if seznam[i][5] == None:
                seznam[i][5] = "N"
        seznam.sort(key = lambda x: x[3])
        for i in range(len(seznam)):
            if seznam[i][2]== chr(ord("a")-1):
                seznam[i][2] = "X"
        return seznam
    def Celakoncovka(radky,sloupce,meto=0):
        rantajm_zac = time.time()
        celkempoli = 2*(radky*sloupce)*(radky*sloupce-1)*(radky*sloupce-1)
        print("Horní odhad: ", celkempoli)
        kontrola_generovani = 2**15
        zacatek_ocislovani = 2**15
        kontrola_ocislovani = 2**16
        kontrola_vypisovani = 2**13
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
            soubor.write("[")
            for k in range(len((pozice))):
                soubor.write(str(pozice[k])+",")
            soubor.write("]")
            soubor.close()
            print("Zapsano do souboru ",sou)
        def Pispekne(nazev,pozice,radky,sloupce):
            sou = str(nazev)+str(radky)+"x"+str(sloupce)+".txt"
            print("Otviram soubor ",sou)
            soubor = open(sou,"w") #uložíme do souboru
            for k in range(len((pozice))):
                soubor.write(str(pozice[k]))
                soubor.write("\n")
            soubor.close()
            print("Zapsano do souboru ",sou)
        def Odmazkonec(seznam):
            while seznam[-1] in [None,"",0,"0"]:
                seznam.pop()
            return seznam
        def Zaklad(soubor):
            with open(soubor,"r") as s:
                ss = s.read()
            print("rd")
            databaze = eval(ss)
            print("evl")
            puredatabaze = []
            for i in databaze:
                k = i[:-3]
                puredatabaze.append(k)
            print("dc")
            Pis("Purepozice_",puredatabaze,8,8)
            Pispekne("Format_Purepozice_",puredatabaze,8,8)
            return(databaze,puredatabaze)

        def Nahraj(soubor): #i s přípono
            with open(soubor,"r") as e:
                datab = e.read()
                print("rd")
                vysledek = eval(datab)
                print("evl")
            return vysledek


        def Preindexuj(seznam,veleseznam):
            def VelkyIndexing(seznam,veleseznam):
                ti = time.time()
                seznam.sort()
                zara = 0 #zarážka pro indexování, ať nehledá od nuly
                nov = [[-1,-1]for i in range(len(seznam))]
                kk = len(veleseznam)//2+3
                print("Délka:",len(seznam))
                for i in range(len(seznam)):
                    if (i+1)%kontrola_ocislovani == 0:
                        tim = ti-1
                        ti = time.time()
                        print("Tridime",i,":",ti-tim-1,"sek. Celková velikost:",len(seznam))
                    if JeLegalni(seznam[i]):
                        poop = seznam[i].pop()
                        if poop != -1: #kvůli zkrácení ValErrů
                            try:
                                #if seznam[i] in veleseznam:
                                #zara = veleseznam.index(seznam[i])
                                zara = veleseznam.index(seznam[i],zara,kk)
                                nov[i] = [poop,zara]
                                seznam[i] = -1 #ať nekazím paměť
                            except ValueError:
                                for vynul in range(i+1,len(seznam)-1):
                                    if seznam[i] and seznam[vynul][:-1] == seznam[i]: #pro všechny shodné ( = chybné) seznamy bez posledního prvku...
                                        seznam[vynul][-1] = -1 #...hodíme minus jedničku, takže ty další neprojdou
                                    else:
                                        break #ať nejede do konce seznamu
                                continue
                            finally:
                                seznam[i] = None #čistím paměť
                        else:
                            seznam[i] = [None]
                            continue
                        #print(nov)
                #input()
                nov.sort(key = lambda x: x[0])
                #print(nov)
                return nov
            #szn = [['a1', 'b4', 'X', 'B', None, 'N', 2], ['a1', 'b4', 'X', 'B', None, 'N', 3], ['a1', 'b4', 'X', 'B', None, 'N', 1], ['a1', 'd4', 'X', 'B', None, 'N', 0], ['a1', 'e4', 'X', 'B', None, 'N', 1], ['a1', 'e4', 'X', 'B', None, 'N', 2], ['a1', 'e4', 'X', 'B', None, 'N', 0], ['a1', 'e4', 'X', 'B', None, 'N', 0], ['a1', 'e4', 'X', 'B', None, 'N', 0], ['a1', 'e4', 'X', 'B', None, 'N', 0], ['a1', 'f4', 'X', 'B', None, 'N', 0]]   
            #vlszn=[['a1', 'c1', 'X', 'B', None, 'N'],['a1', 'd1', 'X', 'B', None, 'N'],['a1', 'e1', 'X', 'B', None, 'N'],['a1', 'f1', 'X', 'B', None, 'N'],['a1', 'c2', 'X', 'B', None, 'N'],['a1', 'd2', 'X', 'B', None, 'N'],['a1', 'e2', 'X', 'B', None, 'N'],['a1', 'f2', 'X', 'B', None, 'N'],['a1', 'a3', 'X', 'B', None, 'N'],['a1', 'b3', 'X', 'B', None, 'N'],['a1', 'c3', 'X', 'B', None, 'N'],['a1', 'd3', 'X', 'B', None, 'N'],['a1', 'e3', 'X', 'B', None, 'N'],['a1', 'f3', 'X', 'B', None, 'N'],['a1', 'a4', 'X', 'B', None, 'N'],['a1', 'b4', 'X', 'B', None, 'N'],['a1', 'c4', 'X', 'B', None, 'N'],['a1', 'd4', 'X', 'B', None, 'N'],['a1', 'e4', 'X', 'B', None, 'N'],['a1', 'f4', 'X', 'B', None, 'N'],['a1', 'a5', 'X', 'B', None, 'N'],['a1', 'b5', 'X', 'B', None, 'N'],['a1', 'c5', 'X', 'B', None, 'N'],['a1', 'd5', 'X', 'B', None, 'N'],['a1', 'e5', 'X', 'B', None, 'N'],['a1', 'f5', 'X', 'B', None, 'N'],['a1', 'a6', 'X', 'B', None, 'N'],['a1', 'b6', 'X', 'B', None, 'N'],['a1', 'c6', 'X', 'B', None, 'N'],['a1', 'd6', 'X', 'B', None, 'N']]

            #print(szn)
            #input()
            sezam = VelkyIndexing(seznam,veleseznam)
            vysledne = [[]for i in range(len(veleseznam)+1)] #+1 na koncové mínusy
            #print(vysledne)
            for i in sezam:
                #print(vysledne)
                #print(i[0],i[1])
                #input()
                vysledne[i[0]].append(i.pop()) #vyhazuji 
            #print(vysledne)
            vysledne.pop()
            return vysledne
        #pozice = Nahraj("Pozice8x8.txt")
        #purepozice = Nahraj("Purepozice_8x8.txt")
        #ROZMĚRY
        maxsloupec = sloupec(sloupce)
        maxradek = radky

        def Cas(promenna, ti = 0):
                if promenna%1024 == 0:
                    tim = ti+1
                    ti = time.time()
                    print(promenna//1024,": ",ti+1-tim," sek")



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
            #Nelegální pozice - bez krále
            def JeLegalni(konpozice):
                if konpozice[1] == "X" or konpozice[0] == "X":
                    return False
                bilkra = SouradnicePole(konpozice[0])
                cerkra = SouradnicePole(konpozice[1])
                if bilkra[0]-cerkra[0] in range(-1,2) and bilkra[1]-cerkra[1] in range(-1,2):
                    return False
                return True
            def ZrusNelegal(databaze): #do nové databáze přesune jen legální pozice
                novadatab = []
                for i in range(len(databaze)):
                    if JeLegalni(databaze[i]):
                        novadatab.append(databaze[i])
                    databaze[i] = None #čistím paměť
                return novadatab
            """def BezKral(pozice): 
                novepozice=[] #napsat nový seznam je jednodušší než odstraňovat prvky a přepisovat indexy ve starém seznamu (výjimka je odstranění posledního prvku)
                for x in range(len(pozice)):
                    if (x+1)%65536== 0:
                           print(x) 
                    j = (pozice[x])[:]
                    if j[0] != "X" and j[1] != "X":
                        novepozice.append(j)
                    pozice[x] = []
                return novepozice
            #Pis("jenpoziceskrali",pozice,radky,sloupce)

            #pozice s králi vedle sebe (jediná explicitně zadaná nemožná pozice, všechny ostatní budou založeny na možnosti tahu)
            def VedleKral(pozice):
                novepozice=[]
                for x in range(len(pozice)):
                    if (x+1)%65536== 0:
                           print(x) 
                    j = (pozice[x])[:]
                    bk = (j[0])[:]
                    ck = (j[1])[:] #umístění bílého a černého krále, rozdíl mezi řadou a sloupcem musí být větší než 1 alespoň u jednoho parametru
                    if bk == "X" or ck == "X":
                        novepozice.append(j)
                        continue
                    else:
                        if abs((ord(bk[0])-ord(ck[0])))>1 or abs((int(bk[1])-int(ck[1])))>1:
                            novepozice.append(j)
                    pozice[x] = []
                return novepozice"""

            def umisti(pozice,n):
                zkouma = pozice[n][:] #jedna pozice
                i = 0
                while zkouma[i] != None: #prvni neumistena figura
                    i += 1
            
                #vytvoří celý seznam, z něj vymaže figury na stejných polích
                zkouma[i] = -1 #figura není umístěna na žádném poli
                pozice[n] = zkouma[:] #nahrazujeme první instanci v seznamu (tzn. smažeme pozici s nedefinovaným umístěním figury) zbytek budeme přidávat, čímž se velikost seznamu rozšíří
                for k in range(1,radky+1): #projdeme všechna pole šachovnice
                    for j in range(1,sloupce+1):
                        if (sloupec(j)+str(k)) not in zkouma: #pole není obsazeno 
                            zkouma[i] = (sloupec(j)+str(k)) #a1, b1, c1...
                        #print(zkouma)
                        zkoumacopy = zkouma[:]
                        pozice.append(zkoumacopy)
                        if (len(pozice)+1)%2097152== 0:
                           print(len(pozice))
                           if (len(pozice)+1)%8388608== 0:
                               pozice = VedleKral(pozice)
                               print("x",len(pozice),"x")
                return pozice 
            pozice = umisti(pozice,0)
            #zopakuji postup pro všechny další figury, přičemž zachovávám i možnost, kdy všechny fugury nebudou na šachovnici
            for k in range(pocetfigur-1):
                for i in range(len(pozice)):
                    umisti(pozice,i)
            for i in pozice:
                for j in range(len(i)):
                    if i[j] == -1:
                        i[j] = "X"
            #Pis("vsechnypozice",pozice,radky,sloupce)

            #ZRUŠENÍ NELEGÁLNÍCH POZIC

            # figury na stejných polích - vyřešeno při generování figur

            # hrajeme bez krále
            #konec
            """for i in range(len(pozice)):
                if (i+1)%524288== 0:
                           print(i) 
                for j in range(len(pozice[i])):
                    pozice[i][j] = Rozkoduj(pozice[i][j])"""
            print("Odstranovani nelegalnich pozic")
            pozice = ZrusNelegal(pozice)
            """pozice = BezKral(pozice)
            pozice = VedleKral(pozice)"""
            return pozice
        def Rozmnoz(databaze): #rozmnoží databázi podle toho, kdo je na tahu, a také ke každé pozici napíše, kolik tahů zbývá do matu (None = nevíme)
            databaze.sort()
            for i in range(len(databaze)):
                k = (databaze[i])[:]
                databaze[i].append("B") #bílý na tahu
                databaze[i].append(None)
                k.append("C")
                k.append(None)
                databaze.append(k) #přidá pozici s černým na tahu na konec DTB
                #Mohl bych nyní i eliminovat pozice, kde je na tahu strana dávající šach - to však vyžaduje testování funkce "JeSach", kde nároky mohou být velké (věž se může pohybovat na (řádky+sloupce) polí, a toto bych musel ověřit u každé pozice).
            return databaze
        def Redukuj(databaze): #zruší opakování
            databazen = [] #nová dtb
            for i in range(len(databaze)-1):
                #Progress(i,len(databaze))
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
            if seznam:
                v = len(seznam)-1
                if seznam == [] or seznam == [None]:
                    return []
                else:
                    while seznam[v] == None:
                        seznam.pop()
                        v -=1
                        if seznam == []:
                            break
        #NA PRÁZDNÉ ŠACHOVNICI

        #King
        """def TahKralem(umisteni): #umisteni krale
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
            return tahy"""

        #Věž
        """def TahVezi(umisteni): #umisteni veze
            if umisteni == "X":
                return []
            rada = int(umisteni[1])
            sloupec = desloupec(umisteni[0])
            n = 0
            tahy = [None]*(radky-1+sloupce-1) #vez muze o neomezeny pocet poli jednim smerem 
            for i in range(-(sloupec-1),sloupce-sloupec+1):  #dozadu o tolik rad, na kolikate je (jednotky neresim, ZEFEKTIVNIT)
                if i !=0: 
                    if sloupec +i <= sloupce and sloupec + i > 0:
                            tahy[n] = [sloupec + i, rada]
                            tahy[n] = NazevPole(tahy[n])
                            n += 1
            for j in range(-(rada-1),radky-rada+1):
                if j!=0:   
                    if rada + j <= radky and rada + j > 0:
                        tahy[n] = [sloupec, rada+j]
                        tahy[n] = NazevPole(tahy[n])
                        n += 1
            OdmazKonec(tahy)
            return tahy"""
        def TahKralem(konpozice,kde): #umisteni krale
            kde= konpozice[kde]
            rada = int(kde[1:])
            sloupek = desloupec(kde[0])
            tahy = []
            for i in range(-1,2):
                for j in range(-1,2):
                    if i !=0 or j!=0:
                        if sloupek +i <= sloupce and sloupek + i > 0 and rada + j <= radky and rada + j > 0:
                                tahy.append(NazevPole([sloupek + i, rada + j])) 
            return tahy
        def MuzeVez(konpozice,kde=2):
            kde= konpozice[kde]
            #print(konpozice)
            if kde != "X":
                tahy = []
                rada = int(kde[1:])
                sloupek = desloupec(kde[0])
                #DOLEVA
                for i in range(1,sloupek): 
                    r = NazevPole([sloupek-i,rada])
                    if r not in konpozice:
                        tahy.append(r)
                    else:
                        if konpozice.index(r) == 1:
                            tahy.append(r)
                        break
                #DOPRAVA
                for i in range(1,sloupce-sloupek+1):
                    r = NazevPole([sloupek+i,rada])
                    if r not in konpozice:
                        tahy.append(r)
                    else:
                        if konpozice.index(r) == 1:
                            tahy.append(r)
                        break
                #NAHORU
                for i in range(1,radky-rada+1):
                    r = NazevPole([sloupek,rada+i])
                    if r not in konpozice:
                        tahy.append(r)
                    else:
                        if konpozice.index(r) == 1:
                            tahy.append(r)
                        break
                #DOLŮ
                for i in range(1,rada): 
                    r = NazevPole([sloupek,rada-i])
                    if r not in konpozice:
                        tahy.append(r)
                    else:
                        if konpozice.index(r) == 1:
                            tahy.append(r)
                        break
                """#LH
                for i in range(1,radky-rada+1): #jdu podle řad
                    if sloupek-i > 0:
                        r = NazevPole([sloupek-i,rada+i])
                        if r not in konpozice:
                            tahy.append(r)
                        else:
                            if konpozice.index(r) == 1:
                                tahy.append(r)
                            break
                #LD
                for i in range(1,rada): 
                    if sloupek-i > 0:
                        r = NazevPole([sloupek-i,rada-i])
                        if r not in konpozice:
                            tahy.append(r)
                        else:
                            if konpozice.index(r) == 1:
                                tahy.append(r)
                            break
                #PH
                for i in range(1,radky-rada+1): #jdu podle řad
                    if sloupek+i <= sloupce:
                        r = NazevPole([sloupek+i,rada+i])
                        if r not in konpozice:
                            tahy.append(r)
                        else:
                            if konpozice.index(r) == 1:
                                tahy.append(r)
                            break
                #PD
                for i in range(1,rada): 
                    if sloupek+i <= sloupce:
                        r = NazevPole([sloupek+i,rada-i])
                        if r not in konpozice:
                            tahy.append(r)
                        else:
                            if konpozice.index(r) == 1:
                                tahy.append(r)
                            break"""
                """#DOLEVA DOPRAVA
                for i in range(1-sloupek,sloupce-sloupek+1):  #dozadu o tolik rad, na kolikate je (jednotky neresim, ZEFEKTIVNIT)
                    if i !=0 and sloupek +i <= sloupce and sloupek + i > 0:
                            tahy.append(NazevPole([sloupek + i, rada]))
                #NAHORU DOLŮ
                for j in range(1-rada,radky-rada+1):
                    if j!=0 and rada + j <= radky and rada + j > 0: 
                        tahy.append(NazevPole([sloupek, rada+j]))
                #ŠIKMO +X
                for j in range(1-rada,radky-rada+1):
                    if j!=0 and rada + j <= radky and rada + j > 0 and sloupek + j in range(0,sloupce+1):
                        tahy.append(NazevPole([sloupek+j, rada+j]))
                #ŠIKMO -X
                for j in range(1-rada,radky-rada+1):
                    if j!=0 and rada + j <= radky and rada + j > 0 and sloupek + j in range(0,sloupce+1):
                        tahy.append(NazevPole([sloupek-j, rada+j]))
                blok = [konpozice[0],konpozice[1]]
                for v in range(len(blok)):
                    koc = konpozice[v]
                    ves = kde[0]
                    ver = kde[1:]
                    if koc in tahy:
                        kor = desloupec(koc[0])
                        kos = int(koc[1:])
                        ves = desloupec(ves)
                        ver = int(ver)
                        if kor == ves: #sloupec
                            if ver > kos: #je nahoře, blok dolů podle řad
                                for s in range(0,kos):
                                    blok.append(sloupec(ves)+str(s)) #a1,a2,a3...
                            else: #blok směrem nahoru
                                for s in range(kos+1,radky+1): #...a6,a7,a8
                                    blok.append(sloupec(ves)+str(s))
                        else: #řada
                            if ves > kor:
                                for s in range(0,kor): #a1,b1...
                                    blok.append(sloupec(s)+str(ver))
                            else:
                                for s in range(kor+1,sloupce+1): #...g1,h1
                                    blok.append(sloupec(s)+str(ver))
                vysl = []
                for i in tahy:
                    if i not in blok:
                        vysl.append(i)
                return vysl"""
                return tahy
            else:
                return[]

        #CO JE NA CÍLOVÝCH POLÍCH
        def Napada(databaze,cislo,figura,pole):
            if pole in TahyNeom(databaze,cislo,figura,pole):
                return True
            return False

        def Vyhledej_indexy(seznam,velkyseznam,zacatek=0):
            indeseznam = []
            ind = zacatek
            for j in seznam: #sortovaný
                ind = velkyseznam.index(j,ind)#začínáme u prvního indexu
                indeseznam.append(ind)
                #print(indeseznam)
                #time.sleep(0.1)
            return indeseznam

        """def MuzeVez(databaze,cislo,figura):
            j = databaze[cislo]
            if j[2] != "X":
                p = j[2]
                vse = TahyNeom(databaze,cislo,figura)
                blok = [j[0],j[1]]
                #print(blok)
                #print(vse)
                for v in range(len(blok)):
                    if j[v] in vse:
                        k = j[v] #pole figury
                        #print(k)
                        if k[0] == p[0]: #sloupec
                            if int(p[1]) > int(k[1]): #je nahoře, blok dolů podle řad
                                for s in range(0,int(k[1])):
                                    blok.append(p[0]+str(s)) #a1,a2,a3...
                            else: #blok směrem nahoru
                                for s in range((int(k[1])+1),radky+1): #...a6,a7,a8
                                    blok.append(p[0]+str(s))
                        else: #řada
                            if desloupec(p[0]) > desloupec(k[0]):
                                for s in range(0,desloupec(k[0])): #a1,b1...
                                    blok.append(sloupec(s)+p[1])
                                    
                            else:
                                for s in range(desloupec(k[0])+1,sloupce+1): #...g1,h1
                                    blok.append(sloupec(s)+p[1])
                #print(blok)
                #print(list(set(vse)-set(blok)))
                vysl = list(set(vse)-set(blok))
                #vysl.sort()
                return vysl
            else:
                return[]"""
        def TahyNeom(databaze,cislo,figura):
            if figura == 0 or figura == 1:
                return TahKralem(Polefigury(databaze,cislo,figura))
            elif figura == 2:
                l = databaze[cislo]
                if l[2]!="X":
                    return TahVezi(Polefigury(databaze,cislo,figura))
            return
        def TahyObec(databaze,cislo,figura): #tahy nikoli neomezené, ale neřeším legalitu
            if figura == 0 or figura == 1:
                return TahKralem(databaze[cislo],figura) #vrací list
            elif figura == 2:
                return MuzeVez(databaze[cislo],figura) #vrací list
            return
        #VYHLEDÁVACÍ FUNKCE
        def Celapozice(databaze,cislo):
            return databaze[cislo]
        def Polefigury(databaze,cislo,index):
            return ((Celapozice(databaze,cislo))[index])
        def Barvafigury(index):
            return (index%2)
        def JeLegalni(konpozice):
            if konpozice[1] == "X" or konpozice[0] == "X":
                return False
            bilkra = SouradnicePole(konpozice[0])
            cerkra = SouradnicePole(konpozice[1])
            if bilkra[0]-cerkra[0] in range(-1,2) and bilkra[1]-cerkra[1] in range(-1,2):
                return False
            return True
                


        #PŘESKOČIT OBSAZENÁ POLE - VĚŽ
        def BlokVezi(databaze,cislo,index): #mám dvě skupiny: blokovaná a všechna možná pole, všechna ostatní pole na šachovnici můžu ignorovat
            obs = Charak(databaze,cislo,index,"obsa") #blok
            vse = TahyNeom(databaze,cislo,index) #možná
            #můžu využít toho, že věž se pohybuje jenom po řadě nebo sloupci, takže rozdělím na dva případy
            rad = [] #stejná řada, mění se sloupec
            sloup = [] #stejný sloupec, mění se řada
            if vse:
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

        def hard_MuzeVez(databaze,cislo,figura):
            l = databaze[cislo]
            if l[figura] != "X":
                zakaz = BlokVezi(databaze,cislo,figura)+Charak(databaze,cislo,figura,"vlas")
                if zakaz:
                    return (list(set(TahyNeom(databaze,cislo,figura)) - set(zakaz))) #všechny tahy - zakázané tahy; použit rozdíl množin
                else:
                    return TahyNeom(databaze,cislo,figura)
            else:
                return 
        def BraniVez(databaze,cislo,figura):
            br = [""]
            j = Charak(databaze,cislo,figura,"soup")
            k = MuzeVez(databaze,cislo,figura)
            for i in range(len(j)):
                if j[i] in k:
                    br.append(j[i])
            return br
        #Král
        
        def LegalKral(databaze,cislo,figura,puredatabaze):
            j = (TahyNeom(databaze,cislo,figura))[:] #seznam všech tahů
            zakaz = []
            for i in range(len(j)):
                if DoSachu(databaze,cislo,figura,j[i],puredatabaze) == True:
                    zakaz.append(j[i])
            zakaz = zakaz+Charak(databaze,cislo,figura,"vlas")
            return (list(set(TahyNeom(databaze,cislo,figura)) - set(zakaz)))
        def NelegalKral(databaze,cislo,figura):
            if figura == 1:
                b = MuzeVez(databaze,cislo,2)
                return b
            else:
                return []
        
        def DoSachu(databaze,cislo,figura,tah,puredatabaze):
            a = easy_Presunpozice(databaze[cislo],figura,tah)
            c = a[:-3]
            if c in puredatabaze:
                if figura == 1: #cerny tahne
                    b = JeSach(databaze,puredatabaze.index(c))
                    if b in ["C","O"]:
                        return True
                elif figura == 0: #bily tahne
                    b = JeSach(databaze,puredatabaze.index(c))
                    if b in ["B","O"]:
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
                if j[i]!="X":
                    x = Brani(databaze,cislopozice,i) #podmínky existence
                    if x:
                        if j[k] in x: #může-li být král sebrán figurou, i pokud nemůže táhnout kvůli šachu (proto neřeším legalitu - ta je založena na pravidlu "Je šach" a proto by se mi podmínky zacyklily).
                            sach = "B"
                            break
            k = 1 #cerny kral
            for i in range(0,len(j)-2,2): #step 2 - jen figury opačné barvy
                if j[i]!="X":
                    x = Brani(databaze,cislopozice,i)
                    if x:
                        if j[k] in x: #totéž
                            if sach == "B":
                                return "O"
                            else:
                                return "C"
            if sach == "B":
                return "B"
            else:
                return "N"
        def JeMat(databaze,cislopozice,puredatabaze):
            j = databaze[cislopozice]
            if j[2] == X:
                return "N"
            if j[5] == "C":
                for i in range(1,len(j)-3,2):
                    k = TahyObec(databaze,cislopozice,i) #list cílových polí
                    if k:
                        for n in range(len(k)):
                            r =  easy_Presunpozice(databaze[cislopozice],i,k[n]) #pozice vzniklá přesunutím jedné figury
                            s = r[:-3]
                            if s in puredatabaze:
                                v = puredatabaze.index(s) #číslo pozice
                                w = databaze[v]
                                if w[5] == "C":
                                    continue
                                else:
                                    return "Není" #není mat
                            else: #nelegální pozice, není v DTB
                                continue
                return "C"
            elif j[5] == "B":
                for i in range(0,len(j)-3,2):
                    k = TahyObec(databaze,cislopozice,i) #list cílových polí
                    if k:
                        for n in range(len(k)):
                            r =  easy_Presunpozice(databaze[cislopozice],i,k[n]) #pozice vzniklá přesunutím jedné figury
                            s = r[:-3]
                            if s in puredatabaze:
                                v = puredatabaze.index(s) #číslo pozice
                                w = databaze[v]
                                if w[5] == "B":
                                    continue
                                else:
                                    return "Není" #není mat
                            else: #nelegální pozice, není v DTB
                                continue
                return "B"
        #Jednoduchá verze (efektivnější, ale ne obecná)
        def easy_JeSach(databaze,cislopozice):
            j = databaze[cislopozice]
            sach = ""
            if j[2] == "X" or j[0] == "X":
                return "N"
            else:
                umisteniv = j[2]
                radav = int(umisteniv[1])
                sloupecv = desloupec(umisteniv[0])
                umistenik = j[1]
                radak = int(umistenik[1])
                sloupeck = desloupec(umistenik[0])
                #jsou na stejné řadě/sloupci?
                if radav == radak or sloupecv == sloupeck: #může být šach
                    umistenib = j[0] #neblokuje bílýkrál?
                    sloupecb = desloupec(umistenib[0])
                    radab = int(umistenib[1])
                    if radav == radak:
                        if radab == radav:
                            if sloupecv>sloupeck: #napravo věž
                                if sloupecb in range(sloupeck+1,sloupecv): #král mezinima
                                    return "N"
                                else:
                                    return "C"
                            else: #nalevo věž
                                if sloupecb in range(sloupecv+1,sloupeck): #král mezinima
                                    return "N"
                                else:
                                    return "C"
                        else:
                            return "C" #král je na jiné řadě
                    else:
                        if sloupecb == sloupecv:
                            if radav>radak: #nad věž
                                if radab in range(radak+1,radav): #král mezinima
                                    return "N"
                                else:
                                    return "C"
                            else: #pod věž
                                if radab in range(radav+1,radak): #král mezinima
                                    return "N"
                                else:
                                    return "C"
                        else:
                            return "C" #král je na jiném sloupci

            return
        def easy_JeMat(databaze,cislopozice,puredatabaze):
            j = databaze[cislopozice]
            if j[5] == "C":
                i=1
                k = TahyObec(databaze,cislopozice,i) #list cílových polí
                if k:
                    for n in range(len(k)):
                            r =  easy_Presunpozice(databaze[cislopozice],i,k[n]) #pozice vzniklá přesunutím jedné figury
                            s = r[:-3]
                            if s in puredatabaze:
                                v = puredatabaze.index(s) #číslo pozice
                                w = databaze[v]
                                if w[5] == "C":
                                    continue
                                else:
                                    return "Není" #není mat
                            else: #nelegální pozice, není v DTB
                                continue
                return "C"
            return
        def primitiv_JeMat(konkretnipozice): #jenom pozice, a popisuje, jak matové pozice vypadají: #VRACÍ HODNOTU TRUE/FALSE, NE BILY/CERNY
                if konkretnipozice[5] != "C":
                    return False
                p = konkretnipozice[1]
                sloupeck = desloupec(p[0])
                radak = int(p[1])
                p = konkretnipozice[0]
                sloupecb = desloupec(p[0])
                radab = int(p[1])
                p = konkretnipozice[2]
                if p == "X":
                    return False
                sloupecv = desloupec(p[0])
                radav = int(p[1])
                if sloupeck == 1 and radak in (1,radky): #v rohu na sloupci a 
                    if sloupecb in (1,2) and radav == radak:
                        if sloupecv !=2:
                            if (radak == radky and radab == radky-2) or (radak == 1 and radab == 3):
                                return True
                    elif radab in (1,2,radky-1,radky) and sloupecv == sloupeck:
                        if (radak == 1 and radab in (1,2) and abs(sloupecb - sloupeck) ==2) or (radak == radky and radab in (radky-1,radky) and abs(sloupecb-sloupeck) ==2) :
                            if (radak == 1 and radav!=2) or (radak == radky and radav!=radky-1):
                                return True
                    return False
                elif sloupeck == sloupce and radak in (1,radky): #v rohu napravo
                    if sloupecb in (sloupce-1,sloupce) and radav == radak:
                        if sloupecv !=sloupce-1:
                            if (radak == radky and radab == radky-2) or (radak == 1 and radab == 3):
                                return True
                    elif radab in (1,2,radky-1,radky) and sloupecv == sloupeck:
                        if (radak == 1 and radab in (1,2) and sloupecb == sloupce-2) or (radak == radky and radab in (radky-1,radky) and sloupecb == sloupce-2):
                            if (radak ==1 and radav!= 2)or (radak == radky and radav != radky-1):
                                return True
                    return False
                else: #mimo roh
                    if sloupeck == 1 and sloupecb == 3 and radak == radab and sloupecv == 1:
                        if abs(radak - radav) == 1:
                            return False
                        else:
                            return True
                    elif sloupeck == sloupce and sloupecb == sloupce -2 and radak == radab and sloupecv == sloupce:
                        if abs(radak - radav) == 1:
                            return False
                        else:
                            return True
                    elif radak == 1 and radab == 3 and sloupeck == sloupecb and radav == 1:
                        if abs(sloupeck - sloupecv) == 1:
                            return False
                        else:
                            return True
                    elif radak == radky and radab == radky -2 and sloupeck == sloupecb and radav == radky:
                        if abs(sloupeck - sloupecv) == 1:
                            return False
                        else:
                            return True
                return False


        

        #4. PŘESUN
        def Finalpozice(databaze,cislo,figura,pole,puredatabaze):
            #Je tah legální(v seznamu možných tahů)?
            if figura == 0 or figura == 1:
                #print(TahyNeom(puredatabaze,cislo,figura),"...",NelegalKral(puredatabaze,cislo,figura))
                if pole in TahyNeom(puredatabaze,cislo,figura) and pole not in NelegalKral(puredatabaze,cislo,figura):
                    j = (databaze[cislo])[:]
                    k = j[:-3]
                    if pole in k:
                        m = k.index(pole)
                        if m%2 == figura%2:
                            return "Nelegalni" #nemůžu brát svoji figuru
                        else:
                            k[k.index(pole)] = "X"
                            k[figura] = pole
                    else:
                        k[figura]= pole
                    f = ord("C")-ord(j[3]) #bílé 1, černé 0
                    if k in puredatabaze:
                        j = databaze[(puredatabaze.index(k)+(f*(len(databaze)//2)))] #hrál - li bílý, pak se přesunu do druhé půlky, kde hraje černý
                    else:
                        return "Nelegalni"
                else:
                    return "Nelegalni"
            elif figura == 2:
                if figura  == "X":
                    return "Nelegalni"
                if pole in MuzeVez(databaze,cislo,figura):
                    j = (databaze[cislo])[:]
                    k = j[:-3]
                    if pole in k:
                        k[k.index(pole)] = "X"
                        k[figura] = pole
                    else:
                        k[figura]= pole
                    f = ord("C")-ord(j[3]) #bílé 1, černé 0
                    if k in puredatabaze:
                        j = databaze[(puredatabaze.index(k)+(f*(len(databaze)//2)))] #hrál - li bílý, pak se přesunu do druhé půlky, kde hraje černý
                    else:
                        return "Nelegalni"
                else:
                    return "Nelegalni"
            else:
                return "Nelegalni"
            return j
        def Presunpozice(databaze,cislo,figura,pole): #Narozdíl od Finalpozice toto pouze řeší vzniknutí nové pozice přesunutím dané figury
            j = (databaze[cislo])[:]
            if pole not in j: #jestli pole není obsazeno
                j[figura] = pole
            elif j.index(pole)%2 != figura%2: #braní - opačná barva
                k = j.index(pole)
                j[k] = "X" #odstraníme figuru ze šachovnice
                j[figura] = pole
            else:
                return [None,None,None] #blbost, berem vlastní
            return j
        def easy_Presunpozice(jasnapozice,figura,pole):
            j = jasnapozice[:]
            if pole not in j:
                j[figura] = pole
            else:
                k = j.index(pole)
                j[k] = "X" #odstraníme figuru ze šachovnice
                j[figura] = pole
            return j
        #Které pozice mohou vzniknout? (obecně ty, které obsahují ostatní figury na stejných místech)
        def Vyplivni(databaze,cislopozice,figura): #při zpětných tazích může figura vyplivnout jinou (opak braní); vrací všechny výsledné pozice
            r = []
            j = databaze[cislopozice]
            u = j[figura]
            for i in range((figura-1)%2,len(j),2): #opačné barvy
                if i!=figura and j[i] == "X":
                    v = TahyObec(databaze,cislopozice,figura)
                    for k in range(len(v)):
                        p = j[:]
                        p[figura] = v[k]
                        p[i] = u #"vyplivneme" figuru na této pozici
                        r.append (p)
            return r

        #CESTA OD MATU - NEJTĚŽŠÍ
        def Matovanicislo1(databaze,puredatabaze):
            print (len(databaze))
            k = len(databaze)
            nultadatabaze = []
            for i in range(len(databaze)//2-1,len(databaze)):
                #r = (100*i)//len(databaze)
                #if r == x:
                    #print (i,"",end="")
                    #x += 5
                #Progress(i,len(databaze))
                    if primitiv_JeMat(databaze[i]) == True:
                        j = databaze[i]
                        j[4] = 0 #je mat, tzn. zbývá 0 tahů do matu
                        nultadatabaze.append(j)
                #vrátí číslo pozice, s kterou budem pracovat
            Pis("matovepozice",databaze,radky,sloupce)
            Pispekne("format_matovepozice",databaze,radky,sloupce)
            Pispekne("databaze0__",nultadatabaze,radky,sloupce)
            return nultadatabaze

        def RemizyBT(databaze,puredatabaze): #pouze remízy na nedostatek matroše; první tah - vyplivnutí
            start = time.time()
            zakladniremizy = []
            v = len(databaze)
            for i in range(v//2+1): #bílý na tahu -> černý na tahu
                j = databaze[i]
                if j[4] == "R":
                            zakladniremizy.append(j)
                            for a in range(1,len(j)-3,2):
                                b = Vyplivni(databaze,i,a)
                                if b:
                                    for c in range(len(b)):
                                        d = b[c] #nová pozice vzniklá vyplivnutím 
                                        g = d[:-3]#ruším poslední prvky
                                        if g in puredatabaze:
                                            e = puredatabaze.index(g) #v databázi bez tahů i s tahy jsou indexy stejné, ale na tahu bude BÍLÝ (protože se vrací PRVNÍ prvek)
                                            d = databaze[e+v//2] #jdem na výslednou pozici
                                            d[4] = "R1"
            end = time.time()
            print(end-start)
            print(str((end-start)/(radky*sloupce))+" sekundy na pole")
            print("remizyBT")
            return zakladniremizy

        #STROMEČEK Z TAHŮ
        def Stromek(pozice):
            nasledne = [[] for i in range(len(pozice))]
            predchozi = [[] for i in range(len(pozice))]
            #Stromeček následných
            ti = time.time()
            for i in range(len(pozice)):  
                if i % (radky+sloupce)**(2) == 0:
                    tir = ti+1
                    ti = time.time()
                    print(i,": ",(ti+1-tir)," sek")
                if (i+1)%50000 == 0: #ne první
                    Pis("Stromecek_nasl",nasledne,radky,sloupce)
                    Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
                j = pozice[i]
                if j[3] == "B" and j[5] != "C":
                    for figura in [0,2]:
                        vsetah = TahyObec(pozice,i,figura)
                        for v in vsetah:
                            dal = Presunpozice(pozice,i,figura,v)[:-3]
                            if dal in purepozice:
                                    index_pozice = purepozice.index(dal)+len(pozice)//2 #za půlkou, černý 
                                    nasledne[i].append(index_pozice) #přidám číslo pozice do seznamu stromu
                    nasledne[i].sort()
                elif j[3] == "C" and j[5] != "B":
                    figura = 1
                    vsetah = TahyObec(pozice,i,figura)
                    for v in vsetah:
                        dal = Presunpozice(pozice,i,figura,v)
                        if dal in purepozice:
                                    index_pozice = purepozice.index(dal) #první půlka, bílý
                                    nasledne[i].append(index_pozice) #přidám číslo pozice do seznamu stromu
                    nasledne[i].sort()
            Pis("Stromecek_nasl",nasledne,radky,sloupce)
            Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
            for i in range(len(nasledne)):
                if i % (radky+sloupce)**(2) == 0:
                    print(i)
                nasledne[i].sort
            Pis("Stromecek_nasl",nasledne,radky,sloupce)
            Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
            """with open("Stromecek_nasl8x8.txt","r") as e:
                nasl = e.read()
                print("rd")
                nasledne = eval(nasl)
                print("evl")
            with open("Stromecek_pred8x8.txt","r") as e:
                pred = e.read()
                print("rd")
                predchozi = eval(pred)
                print("evl")
            #pozice = Nahraj("databaze_0_8x8.txt")"""



            """for i in range(len(predchozi)):
                if i % (radky+sloupce)**(3) == 0:
                    print(i)
                xa = (predchozi[i])[:]
                predchozi[i] = (predchozi[i+len(predchozi)//2])[:]
                predchozi[i+len(predchozi)//2] = xa[:]"""

            #Stromeček přechozích
            ti = time.time()
            for i in range(len(pozice)):
                if i % (radky+sloupce)**(2) == 0:
                    tir = ti+1
                    ti = time.time()
                    print(i,": ",(ti+1-tir)," sek")
                if (i+1)%50000 == 0: #ne první
                    Pis("Stromecek_pred",predchozi,radky,sloupce)
                    Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)
                j = pozice[i]
                if j[3] == "C":
                    for figura in [0,2]:
                        vsetah = TahyObec(pozice,i,figura)
                        for v in vsetah:
                            dal = Presunpozice(pozice,i,figura,v)[:-3]
                            if dal in purepozice:
                                    index_pozice = purepozice.index(dal) #za půlkou, černý
                                    if pozice[index_pozice][5] != "C":
                                        predchozi[i].append(index_pozice) #přidám číslo pozice do seznamu stromu
                elif j[3] == "B":
                    figura = 1
                    vsetah = TahyObec(pozice,i,figura)
                    for v in vsetah:
                        dal = Presunpozice(pozice,i,figura,v)[:-3]
                        if dal in purepozice:
                                    index_pozice = purepozice.index(dal)+len(pozice)//2 #první půlka, bílý
                                    if pozice[index_pozice][5] != "B":
                                        predchozi[i].append(index_pozice) #přidám číslo pozice do seznamu stromu
            Pis("Stromecek_pred",predchozi,radky,sloupce)
            Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)
            #cProfile.run("Stropre()")
            for i in range(len(predchozi)):
                        if i %(radky+sloupce)**(2) == 0:
                                print(i)
                        predchozi[i].sort()
            Pis("Stromecek_pred",predchozi,radky,sloupce)
            Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)
            ti = time.time()
            for i in range(len(pozice)):
                tir = ti+1
                ti = time.time()
                if i %((radky+sloupce)**(2)) == 0:
                    print(print(i,": ",(ti+1-tir)," sek"))
                if pozice[i][3] == "B":
                    are = Vyplivni(pozice,i,1)
                    for k in are:
                        k = k[:-3]
                        if k in purepozice:
                            ind = purepozice.index(k)+len(purepozice)//2
                            predchozi[i].append(ind)
            for i in range(len(predchozi)):
                if i % (radky+sloupce)**(2) == 0:
                                print(i)
                predchozi[i].sort()
            Pis("Stromecek_pred",predchozi,radky,sloupce)
            Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)
            #Stromečky máme, co teď?
            return nasledne, predchozi, time.time()

        #STROMEK OBEMA SMERY NARAZ
        def Stromekc():
                    nasledne = [[] for i in range(len(pozice))]
                    predchozi = [[] for i in range(len(pozice))]
                    ti = time.time()
                    predb_seznam = []
                    for i in range(len(pozice)//2):  
                        if i % (kontrola_vypisovani) == 0:
                            tir = ti+1
                            ti = time.time()
                            print(i,": ",(ti+1-tir)," sek")
                        """if (i+1)%50000 == 0: #ne první
                            Pis("Stromecek_nasl",nasledne,radky,sloupce)
                            Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
                            Pis("Stromecek_pred",predchozi,radky,sloupce)
                            Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)"""

                        j = pozice[i]
                        
                        if j[3] == "B":
                            
                            for figura in [0,2]:
                                vsetah = TahyObec(pozice,i,figura)
                                for v in vsetah:
                                    dal = Presunpozice(pozice,i,figura,v)[:-3]
                                    if dal and JeLegalni(dal):
                                        dal.append(i)
                                        predb_seznam.append(dal)
                        
                         
                        elif j[3] == "C":
                            continue
                            #končíme s indexingem bílých
                        if (i+1)%(zacatek_ocislovani) == 0:
                            zatim = Preindexuj(predb_seznam,purepozice)
                            for i in range(len(zatim)):
                                for j in range(len(zatim[i])):
                                    zatim[i][j]+=len(pozice)//2
                            for i in range(len(zatim)):
                                refer = pozice[i]
                                for j in reversed(range(len(zatim[i]))):
                                    r = zatim[i][j]
                                    if refer[5] != "C" and pozice[r][5] != "B":
                                        nasledne[i].append(r)
                                    if pozice[r][5] != "C":
                                        predchozi[i].append(r)
                            zatim,predb_seznam = [],[]
                    zatim = Preindexuj(predb_seznam,purepozice)
                    for i in range(len(zatim)):
                        for j in range(len(zatim[i])):
                            zatim[i][j]+=len(pozice)//2
                    for i in range(len(zatim)):
                        refer = pozice[i]
                        for j in reversed(range(len(zatim[i]))):
                            r = zatim[i][j]
                            if refer[5] != "C" and pozice[r][5] != "B":
                                nasledne[i].append(r)
                            if pozice[r][5] != "C":
                                predchozi[i].append(r)
                    zatim,predb_seznam = [],[]

                    #a černý
                        
                    predb_seznam = []
                    ti = time.time()
                    for i in range(len(pozice)//2,len(pozice)):  
                        if i % (kontrola_vypisovani) == 0:
                            tir = ti+1
                            ti = time.time()
                            print(i,": ",(ti+1-tir)," sek")
                        """if (i+1)%50000 == 0: #ne první
                            Pis("Stromecek_nasl",nasledne,radky,sloupce)
                            Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
                            Pis("Stromecek_pred",predchozi,radky,sloupce)
                            Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)"""
                        j = pozice[i]
                        if j[3] == "C":
                            figura = 1
                            vsetah = TahyObec(pozice,i,figura)
                            for v in vsetah:
                                dal = Presunpozice(pozice,i,figura,v)[:-3]
                                if dal and JeLegalni(dal):
                                    dal.append(i)
                                    predb_seznam.append(dal)
                            """for h in indxsezn:
                                            index_pozice = h
                                            if j[5] != "B" and pozice[index_pozice][5]!="C":
                                                nasledne[i].append(index_pozice)
                                            if pozice[index_pozice][5] != "B":
                                                predchozi[i].append(index_pozice)
                                                #přidám číslo pozice do seznamu stromu"""
                        elif j[3] == "B":
                            continue
                        if (i+1)%(zacatek_ocislovani) == 0:
                            zatim = Preindexuj(predb_seznam,purepozice)
                            """for i in range(len(zatim)):
                                for j in range(len(zatim[i])):
                                    zatim[i][j]+=len(pozice)//2"""
                            for i in range(len(zatim)):
                                refer = pozice[i]
                                for j in reversed(range(len(zatim[i]))):
                                    r = zatim[i][j]
                                    if refer[5] != "B" and pozice[r][5] != "C":
                                        nasledne[i].append(r)
                                    if pozice[r][5] != "B":
                                        predchozi[i].append(r)
                            zatim,predb_seznam = [],[]
                    zatim = Preindexuj(predb_seznam,purepozice)
                    """for i in range(len(zatim)):
                        for j in range(len(zatim[i])):
                            zatim[i][j]+=len(pozice)//2"""
                    for i in range(len(zatim)):
                        refer = pozice[i]
                        for j in reversed(range(len(zatim[i]))):
                            r = zatim[i][j]
                            if refer[5] != "B" and pozice[r][5] != "C":
                                nasledne[i].append(r)
                            if pozice[r][5] != "B":
                                predchozi[i].append(r)
                    zatim,predb_seznam = [],[]
                    
                    Pis("Stromecek_nasl",nasledne,radky,sloupce)
                    Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
                    for i in range(len(nasledne)):
                        if i % (zacatek_ocislovani) == 0:
                            print(i)
                        nasledne[i].sort
                    Pis("Stromecek_nasl",nasledne,radky,sloupce)
                    Pispekne("Format_Stromecek_nasl",nasledne,radky,sloupce)
                    #Výpliv
                    ti = time.time()
                    for i in range(len(pozice)):
                        #print(pozice[i])
                        if i %(kontrola_vypisovani) == 0:
                            tir = ti+1
                            ti = time.time()
                            print(i,": ",(ti+1-tir)," sek")
                        if pozice[i][3] == "B":
                            are = Vyplivni(pozice,i,1)
                            are.sort()
                            ind = 0
                            for k in are:
                                #print(k)
                                k = k[:-3]
                                if JeLegalni(k):
                                    try:
                                        ind = purepozice.index(k,ind)
                                        predchozi[i].append(ind+len(purepozice)//2)
                                    except ValueError:
                                        continue
                        predchozi[i].sort()
                    Pis("Stromecek_pred",predchozi,radky,sloupce)
                    Pispekne("Format_Stromecek_pred",predchozi,radky,sloupce)
                    return nasledne,predchozi,time.time()
        def Zapismatovepozice(databaze):
            for j in databaze:
                if primitiv_JeMat(j) == True:
                    j[4] = 0
            return
        """Zapismatovepozice(pozice)
        Pis("databaze_0_",pozice,radky,sloupce)
        Pispekne("Format_databaze_0_",pozice,radky,sloupce)"""

        def Remizyzero(databaze):
            ti = time.time()
            for i in range(len(databaze)):
                if i % (radky+sloupce)**(3) == 0:
                    tim = ti+1
                    ti = time.time()
                    print(i,": ",ti+1-tim," sek")
                if databaze[i][2] == "X":
                    databaze[i][4] = "R"
            return databaze

        def Remizyjedna(databaze):
            ti = time.time()
            for i in range(len(databaze)):
                if i%(radky+sloupce)**(2) == 0:
                    tim = ti+1
                    ti = time.time()
                    print(i,": ",ti+1-tim," sek")
                if databaze[i][4] == "R":
                    pre = predchozi[i]
                    for k in pre:
                        if databaze[k][4] != "R":
                            databaze[k][4] = "R1"
            return databaze

        """pozice = Remizyzero(pozice)
        Pis("Remizy_",pozice,radky,sloupce)
        Pispekne("Format_Remizy_",pozice,radky,sloupce)
        pozice = Nahraj("Remizy_8x8.txt")
        pozice = Remizyjedna(pozice)
        Pis("RemizyJ_",pozice,radky,sloupce)
        Pispekne("Format_RemizyJ_",pozice,radky,sloupce)"""

        #pozice = Nahraj("RemizyJ_8x8.txt")

        def Matovanizpetne(databaze,predchozi,nasledne,tahy=0):
            ti = time.time()
            for i in range(len(databaze)):
                """if databaze[i][0] == "c1" and databaze[i][1] == "a2" and databaze[i][2] == "b8" and databaze[i][3] == "B" and type(databaze[i][4]) == int: #and databaze[i][4] %2 == 0:
                    print(databaze[i])
                    ver = predchozi[i]
                    print(ver)
                    for m in range(len(ver)):
                        print(databaze[ver[m]],"\n")
                    ver = nasledne[i]
                    print(ver)
                    for m in range(len(ver)):
                        print(databaze[ver[m]],"\n")"""
                if i%(radky+sloupce)**(3) == 0:
                    tim = ti+1
                    ti = time.time()
                    print(i,": ",ti+1-tim," sek")
                if tahy%2 == 0:
                    if databaze[i][3] == "C" and databaze[i][4] == tahy:
                        zpe = predchozi[i]
                        for k in zpe:
                            umi = databaze[k] #samotná pozice
                            if umi[4] == None: #není číslo
                                umi[4] = tahy+1
                elif tahy%2 == 1:
                    if databaze[i][3] == "B" and databaze[i][4] == tahy: #tohle bude složitější
                        ari = predchozi[i] #vyšší
                        for se in ari: #se je číslo předchozí pozice
                            kur = databaze[se]
                            ap = kur[4] #číslo
                            if ap not in ["R","R1"]:
                                if ap == None:
                                    databaze[se][4] = tahy + 1
                                elif ap < tahy+1:
                                    databaze[se][4] = tahy+1
                                    dal = predchozi[se]
                                    for cile in dal: #čísla v předchozích
                                        far = nasledne[cile]
                                        minim = tahy
                                        for cislo in far:
                                            a = databaze[cislo][4]
                                            if a not in [None,"R","R1"] and a < minim:
                                                minim = a
                                        if minim%2 == 0:
                                            databaze[cile][4] = minim+1
                                        else:
                                            aaaaaa = 1
            if tahy%2 == 1:
                for i in range(len(databaze)):
                    if databaze[i][3] == "C":
                        ver = nasledne[i]
                        diehard = []
                        for m in range(len(ver)):
                            are = (databaze[ver[m]])
                            if type(are[4]) == int:
                                diehard.append(are[4])
                            elif are[4] in ["R","R1"]:
                                diehard = []
                                break
                        if diehard != []:
                            if max(diehard)%2 == 1:
                                databaze[i][4] = max(diehard)+1
                        else:
                            continue
            if tahy%2 == 0:
                for i in range(len(databaze)):
                    if databaze[i][3] == "B":
                        ver = nasledne[i]
                        diehard = []
                        for m in range(len(ver)):
                            are = (databaze[ver[m]])
                            if type(are[4]) == int:
                                diehard.append(are[4])
                            elif are[4] in ["R","R1",None]:
                                continue
                        if diehard != []:
                            if min(diehard)%2 == 0:
                                databaze[i][4] = min(diehard)+1
                        else:
                            continue



                    
                        """
                        zpe = predchozi[i]
                        for k in zpe:
                            umi = databaze[k]
                            if umi[4] not in ["R","R1"]:
                                if umi[4] == None:
                                    umi[4] = tahy+1
                                elif umi[4] < tahy + 1: #a je to tady
                                    umi[4] = tahy+1
                                    pre = predchozi[k]
                                    for cislo_zmenitelna_pozice in pre:
                                        dar = databaze[cislo_zmenitelna_pozice]
                                        nas = nasledne[cislo_zmenitelna_pozice]
                                        minim = tahy +1
                                        for v in nas:
                                            a = databaze[v][4]
                                            if a not in [None,"R","R1"] and a < minim:
                                                minim = a
                                        databaze[cislo_zmenitelna_pozice][4] = minim+1"""
            return databaze
        def Prelesti(databaze,predchozi,nasledne,opak = 0):
            for i in range(len(databaze)):
                if databaze[i][3] == "B":
                    tahy = databaze[i][4]
                    dalsi = nasledne[i]
                    min = 41
                    for ser in dalsi: #ser je číslo
                        a = databaze[ser][4]
                        if a not in [None,"R","R1"] and a < min:
                            min = a
                    f = min
                    if min != 41:
                        databaze[i][4] = f+1
            print(opak," ... ", 1)
            for i in range(len(databaze)):
                if databaze[i][4] == "C":
                    dalsi = nasledne[i]
                    max = 0
                    for ser in dalsi:
                        a = databaze[ser][4]
                        if a in ["R","R1"]:
                            max = a+""
                            break
                        elif a  == None:
                            print( "Nic" )
                        elif type(a)  == int:
                            if a > max:
                                max = a
                        else:
                            print("Blbost")
                    if type(max) == str:
                        databaze[i][4] = max+""
                    elif type(max) == int:
                        databaze[i][4] = max+1
                    else:
                        print("Blbost")
            return databaze
        def Prosmejdi(databaze):
            for i in range(len(databaze)):
                if databaze[i][5] in ["B","C"] and databaze[i][5] != databaze[i][3]:
                    databaze[i][4] = "Nex"
                elif databaze[i][2] == "X":
                    databaze[i][4] = "R"
                elif databaze[i][5] not in ["B","C"] and nasledne[i] == []:
                    databaze[i][4] = "Pat"
            return databaze
        #print("ara")
        """pozice = Nahraj("Pozice_40ZP_8x8.txt")
        for n in range(40):
            pozice = Prelesti(pozice,predchozi,nasledne,n)
        Pis("Finish_"+str(39+1)+"ZP_",pozice,radky,sloupce)
        Pispekne("Format_Finish_"+str(39+1)+"ZP",pozice,radky,sloupce)"""
        



        pozice = Generuj()
        pozice = Rozmnoz(pozice)
        pozice = Redukuj(pozice)
        osekpoz = len(pozice)
        print("Zbylo: ",osekpoz,)
        print("Část 1 hotova")
        purepozice = deepcopy(pozice)
        for i in range(len(purepozice)):
            purepozice[i] = purepozice[i][:-2]
        print("Část 2 hotova")
        for i in range(len(pozice)):
            pozice[i].append(easy_JeSach(pozice,i))
            if (i+1)%(2**(7+(radky+sloupce//2))) == 0:
                print(i)
        print("Část 3 hotova")
        pozice = RealSort(pozice)
        pozice = Redukuj(pozice)
        print("Část 4 hotova, zapisuje se")
        #Pis("Pozice_",pozice,radky,sloupce)
        Pispekne("Format_Pozice_",pozice,radky,sloupce)
        """pozice = Nahraj("Pozice_20x8.txt")
        purepozice = [[]for i in range(len(pozice))]
        for i in range(len(pozice)):
            purepozice[i] = purepozice[i][:-3]"""
        nasledne,predchozi,rantajm_pre = Stromekc()
        pozice = Remizyzero(pozice)
        Pis("Remizy_",pozice,radky,sloupce)
        Pispekne("Format_Remizy_",pozice,radky,sloupce)
        pozice = Remizyjedna(pozice)
        Pis("RemizyJ_",pozice,radky,sloupce)
        Pispekne("Format_RemizyJ_",pozice,radky,sloupce)
        print("Počítám matování")
        Zapismatovepozice(pozice)
        """Pis("databaze_0_",pozice,radky,sloupce)
        Pispekne("Format_databaze_0_",pozice,radky,sloupce)"""
        kontrolala = []
        prumery = []
        for n in range(4*(radky+sloupce)+20):
            suma = 0
            pocet = 0
            pozice = Matovanizpetne(pozice,predchozi,nasledne,n)
            diagram = []
            progre = 2**((radky+sloupce)//2+7)
            for i in range(len(pozice)):
                    if (i+1)%progre == 0:
                        print(i)
                    if pozice[i][4] is None:
                        suma+=2*(radky+sloupce)
                        pocet += 1
                    if pozice[i][4] not in [None,"Nex","Pat"]:
                        if pozice[i][4] == "R":
                            diagram.append(-2)
                        elif pozice[i][4] == "R1":
                            diagram.append(-1)
                        else:
                            suma += pozice[i][4]
                            pocet += 1
                            diagram.append(pozice[i][4])
            prumery.append(suma/pocet)
            digra = [0,0,0]
            for i in range(len(diagram)):
                if diagram[i]+2 >= len(digra):
                    while len(digra)<=diagram[i]+2:
                        digra.append(0)
                digra[diagram[i]+2]+=1
            #plt.plot(digra)
            #plt.pause(.1)
            if diagram == kontrolala:
                plt.plot(digra)
                plt.savefig("Pozice_Finish"+str(radky)+"x"+str(sloupce)+".png")
                plt.clf()
                plt.close()
                plt.plot(prumery)
                plt.savefig("Vyvoj_Pozice_Finish"+str(radky)+"x"+str(sloupce)+".png")
                plt.clf()
                plt.close()
                break
            else:
                kontrolala = diagram[:]
                diagram = []
                plt.clf()
            #Pis("Pozice_"+str(n+1)+"ZP_",pozice,radky,sloupce)
            #Pispekne("Format_Pozice_"+str(n+1)+"ZP",pozice,radky,sloupce)
        pozice = Prosmejdi(pozice)
        Pis("Pozice_Finish_",pozice,radky,sloupce)
        Pispekne("Format_Pozice_Finish",pozice,radky,sloupce)
        rantajm_kon = time.time()
        rantajm_cel = rantajm_kon-rantajm_zac
        print("Všechny pozice: ",celkempoli)
        print("Osekano: ", celkempoli-osekpoz)
        print("Celkem pozic: ",osekpoz)
        print("Čas: ",rantajm_cel," v minutách:", int(rantajm_cel)//60+1)
        print("Sekundy na pozici: ",rantajm_cel/osekpoz)
        print("Pozic za sekundu-analýza:",osekpoz/(rantajm_pre-rantajm_zac))
        print("Max. počet půltahů: ",n)
        print()
        nasledne,predchozi,pozice,purepozice = None,None,None,None
        print("Dokončeno. Seznam pozic najdeš v souboru \"Format_Pozice_Finish"+str(radky)+"x"+str(sloupce)+".txt\"")
        #input()
    def cobylo(od,do):
        bylo = []
        for i in range(od,do+1):
            for j in range(od,do+1):
                #f = open("Format_Pozice_Finish"+str(od)+"x"+str(do)+".txt","r")
                try:
                    f = open("Format_Pozice_Finish"+str(i)+"x"+str(j)+".txt","r")
                    bylo.append([i,j,i*j])
                except FileNotFoundError:
                    continue
        return bylo
    #Celakoncovka(15,8)
    #input()
    """uffff = time.time()
    Celakoncovka(20,5)
    jetotam = time.time()
    print("\n\nUFF. Trvalo to",(jetotam-uffff)//60," minut.")
    input("\n\n\nKONEC\n\n\n")"""

    def Koncovka_nahodne(bylo=[]):
        while len(bylo)!=100:
            a = random.randint(3,12)
            b = random.randint(3,12)
            while [a,b,a*b] in bylo:
                a = random.randint(3,12)
                b = random.randint(3,12)
            print(a,b)
            bylo.append([a,b,a*b])
            Celakoncovka(a,b)


    def Koncovka_systematicky_vzestupne(bylo=[]):
        bude = []
        for a in range(3,12+1):
            for b in range(3,12+1):
                bude.append([a,b,a*b])
        bude.sort(key=lambda x: x[2])

        for k in range(len(bude)):
            if bude[k] not in bylo:
                bylo.append(bude[k])
                Celakoncovka(bude[k][0],bude[k][1])


    def Koncovka_systematicky_sestupne(bylo=[]):
        bude = []
        for a in range(3,12+1):
            for b in range(3,12+1):
                bude.append([a,b,a*b])
        bude.sort(key=lambda x: x[2])

        for k in reversed(range(len(bude))):
            if bude[k] not in bylo:
                bylo.append(bude[k])
                Celakoncovka(bude[k][0],bude[k][1])

    def Koncovka_volitelne(bylo=[]):
        a,b = 0,0
        while a == 0:
                  k = input("Zadej počet řádků šachovnice (3-12) ")
                  try:
                      k = int(k)
                      if k not in range(3,13):
                          print("Nepovolený rozsah")
                      else:
                        a = k
                  except IndexError:
                      print("Není číslo")
                      pass
        while b == 0:
                  l = input("Zadej počet sloupců šachovnice (3-12) ")
                  try:
                      l = int(l)
                      if l not in range(3,13):
                          print("Nepovolený rozsah")
                      else:
                        b = l
                  except:
                      print("Není číslo")
                      pass
        if [a,b,a*b] not in bylo:
            Celakoncovka(a,b,0)
        else:
            potvrzeni = input("Tahle koncovka je už udělaná. Chceš ji vygenerovat znova? (A,+)")
            if potvrzeni in ["A","a","+"]:
                Celakoncovka(a,b,0)
            else:
                print("Takže ne. Ok, končím program.")
    print("Tohle je program na generování koncovek král a věž proti králi. Jakým způsobem mám koncovky vygenerovat?")
    print("A - náhodně","B - systematicky vzestupně (podle velikosti celé šachovnice)","C - systematicky sestupně (podle velikosti celé šachovnice)","jinak - jedna konkrétní velikost šachovnice","X - ukončit","",sep="\n")
    zpusob = input().lower()
    print()
    print("Přepsat staré koncovky? A = ano, jinak ne")
    prepsat = input().lower()
    if prepsat == "a":
        bylo = cobylo(3,12)
    else:
        bylo = []
    if zpusob == "a":
        Koncovka_nahodne(bylo)
    elif zpusob == "b":
        Koncovka_systematicky_vzestupne(bylo)
    elif zpusob == "c":
        Koncovka_systematicky_sestupne(bylo)
    elif zpusob == "x":
        print("Ukončuji program")
    else:
        Koncovka_volitelne(bylo)
Profil()
input()
