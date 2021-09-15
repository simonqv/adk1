class Builder:
    # Big file with every index
    raw_index = open('../files/testing.txt', 'r')
    # Index file, no duplicates
    index = open('../files/index.txt', 'w')
    last_word = ""

    def build(self):
        while True:
            # Read one line at a time
            line = self.raw_index.readline()
            if not line:
                break

            # Take word and its index
            words = line.split()

            self.write_to_file(words)
        return

    def write_to_file(self, words):
        word = words[0]
        ind = words[1]
        offset = 0
        # Write to index file
        if self.last_word == "":
            offset = self.index.tell
            self.index.write(word)
        elif word != self.last_word:
            self.index.write("\n")
            offset = self.index.tell
            self.index.write(word)
        self.index.write(" ")
        self.index.write(ind)
        self.last_word = word


