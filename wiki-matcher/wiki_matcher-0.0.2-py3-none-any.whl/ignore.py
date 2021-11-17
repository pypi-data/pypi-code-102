import re

class Ignorer:
    def want_ignore(self, phrase):
        return False

class ListIgnorer(Ignorer):
    def __init__(self, ignore_list):
        self.ignore_list = [re.sub('\s+', ' ', i.casefold()) for i in ignore_list]

    def want_ignore(self, phrase):
        return phrase.casefold() in self.ignore_list

    def max_word_cnt(self):
        if self.ignore_list:
            return max([i.count(' ') + 1 for i in self.ignore_list])
        else:
            return 0

class FileIgnorer(ListIgnorer):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            super.__init__((l.replace('\n', ' ') for l in f.readlines()))
