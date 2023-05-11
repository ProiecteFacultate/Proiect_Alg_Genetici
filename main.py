import math
import decimal
import random
import copy
import sys


def xToBinary(x):   #transforma x in sirul de 0 si 1 tinand cont de intervale
    d = decimal.Decimal(decimal.Decimal(b - a) / decimal.Decimal(pow(2, l)))
    interval = None
    left = 1
    r = int((b - a) / d) + 1
    while l <= r and interval is None:
        mid = (left + r) // 2
        if (x < a + decimal.Decimal(mid * d) and x >= a + decimal.Decimal((mid - 1) * d)) or (a + decimal.Decimal(mid * d) > b):
            interval = mid - 1
        elif x < a + decimal.Decimal(mid * d):
            r = mid - 1
        else:
            left = mid + 1

    return format(interval, '0' + str(l) + 'b')

def binaryToX(binary_string):
    intVal = int(binary_string, 2)
    d = decimal.Decimal(decimal.Decimal(b - a) / decimal.Decimal(pow(2, l)))
    return round(a + decimal.Decimal(intVal * d), 6)

def calculeazaF(x):
    return decimal.Decimal(coef1 * x * x + coef2 * x + coef3)

def calculeazaProbSelectare():
    sum = decimal.Decimal(0)
    for i in range(n):
        sum += calculeazaF(valCromozomi[i])

    for i in range(n):
        probSelectare.append(decimal.Decimal(calculeazaF(valCromozomi[i]) / sum))

def selectie():
    Pas1 = []   #p1t din curs (slide 39)
    q = [0]
    sumPartiala = 0
    for x in probSelectare:
        sumPartiala += x
        q.append(sumPartiala)

    q[len(q) - 1] = 1  #altfel nu o sa fie exact 1

    for i in range(n):
        u = random.random()  #by default se ia intervalul [0,1)
        st = 1
        dr = n
        interval = None
        while interval == None:
            mid = (st + dr) // 2
            if u < q[mid] and u >= q[mid - 1]:
                interval = mid
            elif u >= q[mid]:
                st = mid + 1
            else:
                dr = mid - 1
        Pas1.append([u, interval - 1])  #avem indexare de la 0 in valCromozomi de ex intervalul [p0 = 0, p1] se ia interval = 1, dar e p pentru valCromozomi[0]

    valCromozomiCopie = copy.deepcopy(valCromozomi)
    for i in range(n):
        valCromozomi[i] = valCromozomiCopie[Pas1[i][1]]

    return Pas1

def selecteazaPentruIncrucisare():
    dateParticipare = []
    for i in range(n):
        u = random.uniform(0, 1) #asta e [0, 1], random.random() era [0, 1)
        if u < (pc / 100):
            dateParticipare.append([u, True])
        else:
            dateParticipare.append([u, False])

    return dateParticipare

def incruciseazaCrom(index1, index2):  #indexii in valCromozomi
    punctRupere = random.randint(0, l)
    c1nou = copy.deepcopy(xToBinary(valCromozomi[index2]))
    c2nou = copy.deepcopy(xToBinary(valCromozomi[index1]))

    for i in range(punctRupere):
        c1nou_list = list(c1nou)
        c2nou_list = list(c2nou)
        aux = c1nou_list[i]
        c1nou_list[i] = c2nou_list[i]
        c2nou_list[i] = aux
        c1nou = ''.join(c1nou_list)
        c2nou = ''.join(c2nou_list)

    if punctRupere != 0:   #altfel lasam asa, nu inversam
        valCromozomi[index1] = binaryToX(c1nou)
        valCromozomi[index2] = binaryToX(c2nou)

    return punctRupere

def incrucisare(dateIncrucisare):
    MesajeIncrucisari = []
    indexiDeIncrucisare = []
    for i in range(n):
        if dateIncrucisare[i][1] == True:
            indexiDeIncrucisare.append(i)

    if len(indexiDeIncrucisare) % 2 == 1:   #trebuie perechi, deci nu merge daca avem impar
        indexiDeIncrucisare.pop()

    for i in range(len(indexiDeIncrucisare) // 2):
        cromInit1 = xToBinary(valCromozomi[indexiDeIncrucisare[i * 2]])
        cromInit2 = xToBinary(valCromozomi[indexiDeIncrucisare[i * 2 + 1]])
        punct = incruciseazaCrom(indexiDeIncrucisare[i * 2], indexiDeIncrucisare[i * 2 + 1])
        mesaj = "Recombinare dintre cromozomul " + str(indexiDeIncrucisare[i * 2] + 1) + " cu cromozomul " + str(indexiDeIncrucisare[i * 2 + 1] + 1) + ":\n" + cromInit1 + " " + cromInit2 + " punct " + str(punct) + "\nRezultat " + xToBinary(valCromozomi[indexiDeIncrucisare[i * 2]]) + " " + xToBinary(valCromozomi[indexiDeIncrucisare[i * 2 + 1]])
        MesajeIncrucisari.append(mesaj)

    return MesajeIncrucisari

def muteaza():
    for i in range(n):
        bitsList = list(xToBinary(valCromozomi[i]))
        for j in range(l):  #nrBiti
            u = random.random()
            if u < (pm / 100):
                bitsList[j] = str(abs(int(bitsList[j]) - 1))
        bitsFinal = ''.join(bitsList)

def cautaMaxFitness():
    global n
    maxFitnessIndex = 0
    for i in range(n):
        if calculeazaF(valCromozomi[i]) > calculeazaF(valCromozomi[maxFitnessIndex]):
            maxFitnessIndex = i

    maxFitnessVal = valCromozomi[maxFitnessIndex]
    valCromozomi.pop(maxFitnessIndex)  #scoatem din lista elitistul (pt a nu participa la selectia, a nu mi recombinat sau mutat), iar la finalul creeri noii generatii il adaugam la loc
    n -= 1
    return maxFitnessVal


def genereazaPopInit():
    pop = []
    for i in range(20):
        x = random.uniform(a, b)
        pop.append(round(x, p))

    return pop

def dateInitiale():
    global n
    maxFitnessVal = cautaMaxFitness()
    print("Populatia initiala")
    for i in range(1, n + 1):
        print(str(str(i) + ": " + xToBinary(valCromozomi[i - 1])) + " x= " + str(valCromozomi[i - 1]) + " f= " + str(calculeazaF(valCromozomi[i - 1])))

    print("Probabilitati selectie")
    calculeazaProbSelectare()
    for i in range(1, n + 1):
        print("cromozom  " + str(i) + " probabilitate " + str(probSelectare[i - 1]))

    print("Intervale probabilitati selectie")
    print(0)
    s = 0
    for i in range(n - 1):
        s = decimal.Decimal(s + probSelectare[i])
        print(s)
    print(1.0)

    Pas1 = selectie()   #pas1 contine indexul cromozomilor din valCromozomi
    for i in range(n):
        print("u= " + str(Pas1[i][0]) + " selectam cromozomul " + str(Pas1[i][1] + 1)) #la noi e indexare de la 0, dar cand afisam afisam indexul incepem de la 1

    print("Dupa selectie:")
    for i in range(n):
        print(str(i + 1) + ": " + xToBinary(valCromozomi[i]) + " x= " + str(valCromozomi[i]) + " f= " + str(calculeazaF(valCromozomi[i])))

    print("Probabilitatea de incrucisare " + str(pc / 100))
    dateIncrucisare = selecteazaPentruIncrucisare()
    for i in range(n):
        print(str(i + 1) + ": " + xToBinary(valCromozomi[i]) + " u= " + str(dateIncrucisare[i][0]) + (("<" + str(pc / 100) + " participa") if (dateIncrucisare[i][1] == True) else ""))

    MesajeIncrucisari = incrucisare(dateIncrucisare)
    for mesaj in MesajeIncrucisari:
        print(mesaj, end="\n\n")

    print("Dupa recombinare:")
    for i in range(n):
        print(str(i + 1) + ": " + xToBinary(valCromozomi[i]) + " x= " + str(valCromozomi[i]) + " f=" + str(calculeazaF(valCromozomi[i])))

    print("\nProbabilitate de mutatie pentru fiecare gena " + str(pm / 100))
    print("Probabilitate de mutatie pentru fiecare gena")
    muteaza()
    for i in range(n):
        print(str(i + 1) + ": " + xToBinary(valCromozomi[i]) + " x= " + str(valCromozomi[i]) + " f= " + str(calculeazaF(valCromozomi[i])))

    valCromozomi.append(maxFitnessVal)
    n = n + 1


def ruleazaEtape(etapa):
    global n
    maxx = float('-inf')
    sum = decimal.Decimal(0)
    for x in valCromozomi:
        valF = calculeazaF(x)
        maxx = max(maxx, valF)
        sum += decimal.Decimal(valF)
    print("Etapa " + str(etapa) + ":\n" + "Maxim: " + str(maxx) + " Medie: " + str(sum / n))

    maxFitnessVal = cautaMaxFitness()
    calculeazaProbSelectare()
    Pas1 = selectie()
    dateIncrucisare = selecteazaPentruIncrucisare()
    incrucisare(dateIncrucisare)
    muteaza()

    valCromozomi.append(maxFitnessVal)
    n += 1


###########################################   MAIN   ##########################################################

n = int(input("numar cromozomi = "))
a = int(input("a = "))
b = int(input("b = "))
coef1 = int(input("coef1 = "))  # coef1 * x^2 + coef2 * x + coef3
coef2 = int(input("coef2 = "))
coef3 = int(input("coef3 = "))
p = int(input("precizie = "))
pc = int(input("probabilitate recombinare (%) = "))
pm = int(input("probabilitate mutatie (%) = "))
nrEtape = int(input("numar etape = "))
valCromozomi = genereazaPopInit()

# n = 20
# a = -1
# b = 2
# coef1 = -1
# coef2 = 1
# coef3 = 2
# p = 6
# pc = 25
# pm = 1
# nrEtape = 50
#
# valCromozomi = [-0.914592, -0.516787, -0.246207, 1.480791, 0.835307, 1.229633, 0.133068, -0.897179, 0.100578, -0.311975, 1.411980, 0.404924, 1.954865, 0.359503,
#                  1.255452, 1.124764, 1.527482, 1.573845, -0.562311, 1.191435]


probSelectare = []

l = int(math.log2((b - a) * pow(10, p))) + 1  #nrBiti
dateInitiale()

for i in range(nrEtape):
    ruleazaEtape(i + 1)
