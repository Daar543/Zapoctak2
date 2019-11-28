#ČÁST 1 - VYGENEROVÁNÍ ROZMĚRŮ ŠACHOVNICE A UMÍSTĚNÍ FIGUR NA POLE

def sloupec(x):
    return chr(ord("a")-1+x)

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
    for k in range(1,radky+1):
        for j in range(1,sloupce+1):
            zkouma[i] = (sloupec(j)+str(k))
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
soubor = open("vsechnypozice.txt","w") #uložíme do souboru
for k in range(len((pozice))):
    soubor.write(str(pozice[k]))
    soubor.write("\n")
soubor.close()

###ČÁST 2 - ZRUŠENÍ NELEGÁLNÍCH POZIC

# figury na stejných polích

# hrajeme bez krále

### ČÁST 3 - MOŽNÉ TAHY (definice)

#vzájemný šach
