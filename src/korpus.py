try:
    import cPickle as pickle
except ImportError:
    import pickle


class Korpus:
    def __init__(self):
        with open('data.p', 'rb') as fp:
            data = pickle.load(fp)
        print(data)
        return

def main():
    k = Korpus()


main()
