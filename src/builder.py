from collections import defaultdict

try:
    import cPickle as pickle
except ImportError:
    import pickle


class Builder:
    lazy_man_dict = {}
    index_dict = defaultdict(list)
    last_word = ""
    offset = 0
    string_arr = []

    # Building the files. Reading from rawindex, to remove duplicates and lastly writes that to file.
    def build(self):
        with open('/afs/kth.se/misc/info/kurser/DD2350/adk21/labb1/rawindex.txt', 'r', encoding="latin-1") as raw_index:
            for line in raw_index:
                words = line.split()
                self.read_korpus(words)
            self.write_to_file()
        return

    # Writes the index file without duplicates to tmp folder.
    def write_to_file(self):
        with open('/var/tmp/index.txt', 'w+', encoding="latin-1") as index:
            for key, value in self.index_dict.items():
                self.lazy_index(key, index.tell())
                index.write(key + " " + " ".join(value) + "\n")
        return

    # Simply reads each word and index, if a word exists, append index to its array
    def read_korpus(self, words):
        word = words[0]
        ind = words[1]
        self.index_dict[word].append(ind)
        return

    # Creates the lazymanshashmap (dict) with the index of each aaa, aab, ... entry.
    def lazy_index(self, word, offset):
        lazy_hash = calc_hash(word)
        if lazy_hash not in self.lazy_man_dict:
            self.lazy_man_dict[lazy_hash] = offset
        return lazy_hash


# Calculates the index in the way that was presented during lecture. f(a) * 900 + f(b) * 30 + f(c)
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
    b = Builder()
    b.build()
    with open('lazy.p', 'wb') as fp:
        pickle.dump(b.lazy_man_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)


main()
