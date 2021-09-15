try:
    import cPickle as pickle
except ImportError:
    import pickle


class Builder:
    # Big file with every index
    raw_index = open('../files/testing.txt', 'r')
    # Index file, no duplicates
    index = open('../files/index.txt', 'w+')
    # The lazy hash file?
    lazy_man = open('../files/lazy.pcl', 'w+')
    lazy_man_dict = {}
    last_word = ""
    offset = 0

    def build(self):
        while True:
            # Read one line at a time
            line = self.raw_index.readline()
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
        chars = list(word)
        chars = [char.replace('ä', chr(ord('z') + 1)) for char in chars]
        chars = [char.replace('å', chr(ord('z') + 2)) for char in chars]
        chars = [char.replace('ö', chr(ord('z') + 3)) for char in chars]
        if len(chars) > 2:
            lazy_hash = ord(chars[0]) * 900 + ord(chars[1]) * 30 + ord(chars[2])
        elif len(chars) == 2:
            lazy_hash = ord(chars[0]) * 900 + ord(chars[1]) * 30
        elif len(chars) == 1:
            lazy_hash = ord(chars[0]) * 900
        else:
            return
        if lazy_hash not in self.lazy_man_dict:
            self.lazy_man_dict[lazy_hash] = self.offset
        return


def main():
    b = Builder()
    b.build()
    print(b.lazy_man_dict)
    with open('data.p', 'wb') as fp:
        pickle.dump(b.lazy_man_dict, fp, protocol=pickle.HIGHEST_PROTOCOL)


main()
