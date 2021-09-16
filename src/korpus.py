try:
    import cPickle as pickle
except ImportError:
    import pickle
import sys
import builder


class Korpus:
    def __init__(self):
        with open('data.p', 'rb') as fp:
            data = pickle.load(fp)
        self.korp = data
        return


# Ta in sökord.
# Hitta sökord i filen
# Hitta med det indexet orden som är relevanta
# plocka ut alla index
# Läs i fil.
# Skriv ut


def find_line(search_word, index, k):
    hash_code = builder.calc_hash(search_word)
    pointer = k.korp.get(hash_code)
    index.seek(pointer)
    fst_word = index.readline()
    print(fst_word)
    index_line = fst_word.split()
    return index_line


def search(search_word, index):
    while True:
        line = index.readline()
        word = line.split()[0]
        if word == search_word:
            return line
        elif word[2] != search_word[2]:
            return ""

def print_korpus(indices, word):
    len_print = 10
    korpus = open('../files/text.txt', 'r')
    if len(indices) > 25:
        answer = input("More than 25 lines, are you sure you want to proceed? (y/n)").lower()
        if answer == "n" or answer == "no":
            return

    print("Det finns", len(indices), "förekomster av ordet.")

    for ind in indices:
        if int(ind) - len_print <= 0:
            korpus.seek(0)
        else:
            korpus.seek(int(ind) - len_print)
        print(korpus.read(len_print * 2 + len(word)).replace("\n", " "))
    return


def main():
    k = Korpus()
    index = open('../files/index.txt', 'r')
    search_word = sys.argv[1].lower()

    index_line = find_line(search_word, index, k)

    if index_line[0] == search_word:
        print_korpus(index_line[1:], index_line[0])
    else:
        line = search(search_word, index)
        if line == "":
            print("Does not exist")
        else:
            print_korpus(line[1:], line[0])
    return


main()
