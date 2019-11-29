#ČÁST 1 - VYGENEROVÁNÍ ROZMĚRŮ ŠACHOVNICE A UMÍSTĚNÍ FIGUR NA POLE

def sloupec(x):
    return chr(ord("a")-1+x)
def Pis(nazev,pozice):
    sou = str(nazev+".txt")
    print("Otviram soubor ",sou)
    soubor = open(sou,"w") #uložíme do souboru
    for k in range(len((pozice))):
        soubor.write(str(pozice[k]))
        soubor.write("\n")
    soubor.close()
    print("Zapsano do souboru ",sou)

#rozmerytxt = open("rozmery.txt","r")
#rozmery = rozmerytxt.read()

#radky = int(input("Rozměry šachovnice v řádcích (3 - 15): "))
#sloupce = int(input("Rozměry šachovnice ve sloupcích(3 - 15): "))
radky = 8
sloupce = 8
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
Pis("vsechnypozice",pozice)
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
Pis("jenpoziceskrali",pozice)

#pozice s králi vedle sebe (jediná explicitně zadaná nemožná pozice, všechny ostatní budou založeny na možnosti tahu)
def VedleKral(pozice):
    novepozice=[]
    for x in range(len(pozice)):
        j = (pozice[x])[:]
        bk = (j[0])[:]
        ck = (j[1])[:]
        if abs((ord(bk[0])-ord(ck[0])))>1 or abs((int(bk[1])-int(ck[1])))>1:
            novepozice.append(j)
    return novepozice
pozice = VedleKral(pozice)
Pis("pozicekdesekralovenenapadaji",pozice)
### ČÁST 3 - MOŽNÉ TAHY (definice)

#vzájemný šach
