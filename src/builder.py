try:
    import cPickle as pickle
except ImportError:
    import pickle


class Builder:
    # Big file with every index
    raw_index = open('/afs/kth.se/misc/info/kurser/DD2350/adk21/labb1/rawindex.txt', 'r', encoding = "latin-1")
    # Index file, no duplicates
    index = open('/var/tmp/indexsb.txt', 'w+', encoding="latin-1")
    lazy_man_dict = {}
    last_word = ""
    offset = 0

    def build(self):
        while True:
            # Read one line at a time
            line = self.raw_index.readlines()
            if not line:
                break

            # Take word and its index
            words = line.split()
            self.write_to_file(words)
            self.lazy_index(words[0])
        return

    def write_to_file(self, words):
        word = words[0]
        ind = words[1]

        # Write to index file
        if self.last_word == "":
            self.offset = self.index.tell()
            self.index.write(word)
        elif word != self.last_word:
            self.index.write("\n")
            self.offset = self.index.tell()
            self.index.write(word)
        self.index.write(" ")
        self.index.write(ind)
        self.last_word = word
        return

    def lazy_index(self, word):
        lazy_hash = calc_hash(word)
        if lazy_hash not in self.lazy_man_dict:
            self.lazy_man_dict[lazy_hash] = self.offset
        return lazy_hash


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
    with open('data.p', 'wb') as fp:
        pickle.dump(b.lazy_man_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)


main()
