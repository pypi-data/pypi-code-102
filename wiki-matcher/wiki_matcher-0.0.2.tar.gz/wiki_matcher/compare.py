from strsimpy.jaro_winkler import JaroWinkler
from abc import ABC, abstractmethod 

class WikiComparer(ABC):
    @abstractmethod
    def compare(self, src, target):
        pass

class ExactComparer(WikiComparer):
    def compare(self, src, target):
        return src == target

class StrCloseComparer(WikiComparer):
    strcmp = JaroWinkler()
    def compare(self, src, target):
        return self.get_similarity(src, target)

    def get_similarity(self, src, target):
        split_src = src.lower().split(' ')
        split_target = target.lower().split(' ')

        if len(split_src) != len(split_target):
            return 0
        
        similarity = 1
        for i in range(len(split_src)):
            similarity *= self.strcmp.similarity(
                split_src[i], split_target[i])
            similarity *= self.strcmp.similarity(
                split_src[i][::-1], split_target[i][::-1])
        return similarity
