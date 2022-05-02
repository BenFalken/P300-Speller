class LangNode:
    def __init__(self, **kwargs):
        self.word = ''
        self.children = []
        self.totalWeight = 0
        # Gotta make the object iterable somewhow
        #print(kwargs)
        if 'l' not in kwargs:
            self.letter = -1
        else:
            self.letter = kwargs['l']
        if 'n' not in kwargs:
            self.weights = []
        else:
            n = kwargs['n']
            self.weights = [0 for _ in range(n)]