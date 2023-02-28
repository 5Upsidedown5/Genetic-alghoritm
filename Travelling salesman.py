import numpy as np


def generuj_graf(liczba_pkt): #generate graph
    graf = np.zeros([liczba_pkt, liczba_pkt])
    for x in range(liczba_pkt):
        for y in range(liczba_pkt):
            if x != y:
                graf[x, y] = np.random.randint(1, 6)
            else:
                graf[x,y] = 100000 #punishment

    return graf


def decode_osobnik(osobnik, populacjabp):
    decoded_osobnik = []
    for x in osobnik:
        decoded_osobnik.append(populacjabp[x])
    return decoded_osobnik


def remove_duplicate(tab):
    temp = []
    tab.append(-1)
    l_duplikatow = 0
    for i in range(len(tab) - 1):
        if tab[i] != tab[i + 1]:
            temp.append(tab[i])
        else:
            l_duplikatow += 1
    return temp, l_duplikatow


def ocena(osobnik, graf): #rating for decoded subject
    temp_osobnik = sorted(osobnik)
    temp_osobnik, l_duplikatow = remove_duplicate(temp_osobnik) #sorting and deleting duplitaces from subject
    if l_duplikatow == 0:
        l_duplikatow = 1
    dist = 0
    for i in range(len(osobnik) - 1): #calculating route cost
        dist += graf[osobnik[i], osobnik[i + 1]]

    grade = ((1 / (dist+1)) + (1 / l_duplikatow) + (1 / ((len(graf) - len(temp_osobnik)) + 1))) * 100 #rating pattern

    if osobnik[0] == 0 and osobnik[-1] == 0: #checking if the subject started and ended in starting point
        grade *= 1
    else:
        grade *= 0.01 #if no - reduce rating
    return grade


def generuj_populacje_bp(wielkosc_populacji, graf):
    populacja_bp = []
    for _ in range(wielkosc_populacji):
        populacja_bp.append(np.random.randint(0, len(graf)))
    return populacja_bp


def generuj_populacje_rozwiazan(wielkosc_populacji, populacja_bp):
    populacja_rozwiazan = []
    for _ in range(wielkosc_populacji):
        temp = []
        for _ in range(len(graf) + 1):
            temp.append(np.random.randint(0, len(populacja_bp))) #indicator drawing for population
        populacja_rozwiazan.append(temp)

    return populacja_rozwiazan


def ocena_populacji_rozwiazan(populacja_rozwiazn, graf, populacja_bp):
    tab_ocen = []
    for x in populacja_rozwiazn:
        tab_ocen.append(ocena(decode_osobnik(x, populacja_bp), graf)) #rating for each subject
    return tab_ocen


def ocena_populacji_bp(populacja_bp, populacja_rozwiazan, oceny_rozwiazan, oceny_bp):
    for i in range(len(populacja_rozwiazan)):
        for x in populacja_rozwiazan[i]:
            if oceny_rozwiazan[i] > oceny_bp[x]: #checking if new rating is better than old one
                oceny_bp[x] = oceny_rozwiazan[i] #if yes - swap
    return oceny_bp


def turniej(wielkosc_turnieju, populacja, oceny):
    kandydaci = []
    for _ in range(wielkosc_turnieju):
        kandydaci.append(np.random.randint(0, len(populacja))) #picking up new candidates indexes
    best = kandydaci[0]
    for x in kandydaci: #searching for best
        if oceny[best] < oceny[x]:
            best = x

    return populacja[best]


def generuj_populacje_rodzicow(populacja, oceny):
    populacja_rodzicow = []
    for _ in range(len(populacja)):
        populacja_rodzicow.append(turniej(3, populacja, oceny))
    return populacja_rodzicow


def krzyzowanie_mutacja(osobnik1, osobnik2, graf, rodzaj_populacji, populacja=[], Cr=0.8, Mr=0.2):
    # krzyzowanie
    if not (isinstance(osobnik1, int)):
        y = np.random.uniform()
        if y <= Cr:
            if len(osobnik1) % 2 == 0: #setting the intersection line
                line = int(len(osobnik1) / 2)
            else:
                line = int(np.ceil((len(osobnik1) / 2)))
            # if crossing subjects happened
            nkandydat1 = osobnik1[0:line] + osobnik2[line:]
            nkandydat2 = osobnik2[0:line] + osobnik1[line:]
        else: #if not
            nkandydat1 = osobnik1
            nkandydat2 = osobnik2
    else: #if single element
        nkandydat1 = osobnik1
        nkandydat2 = osobnik2

    if rodzaj_populacji == 'bp':
        granica = len(graf) - 1
    else:
        granica = len(populacja) - 1
    #mutation

    if not (isinstance(osobnik1, int)):
        for i in range(len(nkandydat1)):
            y = np.random.uniform()
            if y < Mr:  # checking for mutation
                x = np.random.uniform()  # drawing for addition or substraction
                if x <= 0.5:
                    if nkandydat1[i] == 0:  # protection for not to go beyond index
                        nkandydat1[i] = 0
                    else:
                        nkandydat1[i] -= 1
                else:
                    if nkandydat1[i] == granica:
                        nkandydat1[i] = granica
                    else:
                        nkandydat1[i] += 1

        for i in range(len(nkandydat2)):
            y = np.random.uniform()
            if y < Mr:
                x = np.random.uniform()
                if x <= 0.5:
                    if nkandydat2[i] == 0:
                        nkandydat2[i] = 0
                    else:
                        nkandydat2[i] -= 1
                else:
                    if nkandydat2[i] == granica:
                        nkandydat2[i] = granica
                    else:
                        nkandydat2[i] += 1
    else:

        y = np.random.uniform()
        if y <= Mr:  # checking for mutation
            x = np.random.uniform()  # drawing for addition or substraction
            if x <= 0.5:
                if nkandydat1 == 0:  # zabezpieczenie zeby nie wykroczyc poza indeks
                    nkandydat1 = 0
                else:
                    nkandydat1 -= 1
            else:
                if nkandydat1 == granica: # protection for not to go beyond index
                    nkandydat1 = granica
                else:
                    nkandydat1 += 1

        y = np.random.uniform()
        if y <= Mr:
            x = np.random.uniform()
            if x <= 0.5:
                if nkandydat2 == 0:
                    nkandydat2 = 0
                else:
                    nkandydat2 -= 1
            else:
                if nkandydat2 == granica:
                    nkandydat2 = granica
                else:
                    nkandydat2 += 1

    return nkandydat1, nkandydat2


def dzialaniaGenetyczne(populacja, oceny, rodzaj_populacji):
    populacja_rodzicow = generuj_populacje_rodzicow(populacja, oceny)
    i = 0
    while i < len(populacja) - 1:
        nowy_osobnik1, nowy_osobnik2 = krzyzowanie_mutacja(populacja_rodzicow[i], populacja_rodzicow[i + 1], graf,
                                                           rodzaj_populacji,
                                                           populacja_rodzicow) #generating new subjects
        populacja_rodzicow[i] = nowy_osobnik1 # replacing old subjects
        populacja_rodzicow[i + 1] = nowy_osobnik2
        i += 2
    return populacja_rodzicow


def find_best(populacja_rozwiazn, oceny_rozwiazan): #checking for best rating
    best_ocena = oceny_rozwiazan[0]
    best = 0
    for i in range(len(oceny_rozwiazan)):
        if best_ocena < oceny_rozwiazan[i]:
            best_ocena = oceny_rozwiazan[i]
            best = i
    return populacja_rozwiazn[best], best_ocena


if __name__ == '__main__':
    graf = generuj_graf(5)
    print(graf)
    bp = generuj_populacje_bp(100, graf)
    r = generuj_populacje_rozwiazan(100, bp)
    oceny_rozwiazan = ocena_populacji_rozwiazan(r, graf, bp)
    oceny_bp = np.zeros(len(bp))
    oceny_bp = ocena_populacji_bp(bp, r, oceny_rozwiazan,oceny_bp)
    liczba_epok = 100
    prog_satyfakcji = 200
    i = 0
    best, ocena_best = find_best(r, oceny_rozwiazan)
    print(decode_osobnik(best, bp))
    print(ocena_best)
    while i < liczba_epok :
        r = dzialaniaGenetyczne(r, oceny_rozwiazan, 'r')
        bp = dzialaniaGenetyczne(bp, oceny_bp, 'bp')
        oceny_rozwiazan = ocena_populacji_rozwiazan(r,graf,bp)
        oceny_bp = ocena_populacji_bp(bp,r,oceny_rozwiazan,oceny_bp)
        nbest, nocena_best = find_best(r, oceny_rozwiazan)
        if nocena_best > ocena_best:
            best = nbest
            ocena_best = nocena_best
        print('najlepszy osobnik ', i, "iteracji:")
        print(decode_osobnik(nbest, bp))
        print('ocena: ')
        print(nocena_best)
        if ocena_best > prog_satyfakcji:
            break
        i +=1


    print("")
    print('najlepszy osobnik: ')
    print(decode_osobnik(best, bp))
    print('ocena')
    print(ocena_best)

