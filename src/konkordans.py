try:
    import cPickle as pickle
except ImportError:
    import pickle
import sys

with open('lazy.p', 'rb') as fp:
    korp = pickle.load(fp)


# finds the line where the first aaa___ combo is
def find_line(search_word, index):
    hash_code = calc_hash(search_word)  # use hash to find the index of ___
    pointer = korp.get(hash_code)  # get said index
    index.seek(pointer)  # place pointer at index
    fst_word = index.readline()  # read first line with ___
    index_line = fst_word.split()  # split to separate each element
    return index_line


# if first word not correct: search for it below first entry of ___
def search(search_word, index):
    while True:
        line = index.readline()
        if not line:  # If there's no line (end of file) return empty.
            return ""
        word = line.split()
        if word[0] == search_word:  # If word is found, return
            return line
        elif word[0][2] != search_word[2]:  # If 3rd letter deviates, we've gone too far.
            return ""


def print_korpus(line):
    if isinstance(line, str):  # if parameter is string, split it
        words = line.split()
    else:
        words = line

    len_print = 30
    korpus = open('/afs/kth.se/misc/info/kurser/DD2350/adk21/labb1/korpus', 'r', encoding="latin-1")

    print("Det finns", len(words[1:]), "förekomster av ordet.")

    # Prints first 25 occurrences of the word.
    for ind in words[1:25]:
        if int(ind) - len_print <= 0:
            korpus.seek(0)
        else:
            korpus.seek(int(ind) - len_print)
        print(korpus.read(len_print * 2 + len(words[0])).replace("\n", " "))

    # If more than 25 words, ask if user want all.
    if len(words[1:]) > 25:
        answer = input("\nMore than 25 lines, are you sure you want to proceed? (y/n)").lower()
        if answer == "y" or answer == "yes":
            for ind in words[25:]:
                korpus.seek(int(ind) - len_print)
                print(korpus.read(len_print * 2 + len(words[0])).replace("\n", " "))
    return


def calc_hash(word):
    chars = list(word)
    chars = [char.replace('ä', chr(ord('z') + 1)) for char in chars]
    chars = [char.replace('å', chr(ord('z') + 2)) for char in chars]
    chars = [char.replace('ö', chr(ord('z') + 3)) for char in chars]
    if len(chars) > 2:
        return ord(chars[0]) * 900 + ord(chars[1]) * 30 + ord(chars[2])
    elif len(chars) == 2:
        return ord(chars[0]) * 900 + ord(chars[1]) * 30
    elif len(chars) == 1:
        return ord(chars[0]) * 900
    else:
        return


def main():
    with open('/var/tmp/index.txt', 'r', encoding="latin-1") as index:
        try:
            search_word = sys.argv[1].lower()
        except:
            print("no input")
            return

        index_line = find_line(search_word, index)

        print("")

        if index_line[0] == search_word:
            print_korpus(index_line)
        else:
            if len(search_word) > 2:
                line = search(search_word, index)
            else:
                print("Does not exist")
                return
            if line == "":
                print("Does not exist")
            else:
                print_korpus(line)
    return


main()
