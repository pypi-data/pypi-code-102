#from compare import StrCloseComparer
from abc import ABC, abstractmethod
import re

class MatchDetail:
    def __init__(self, item, src, closeness):
        self.closeness=closeness
        self.name=item.name
        self.src=src
        self.item=item

    def full_descr(self):
        return self.item.full_descr()

    def _is_valid_operand(self, other):
        return hasattr(other, "name") and hasattr(other, "closeness")
        
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.closeness < other.closeness

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f'<MatchDetail: name={self.name}, closeness={self.closeness}>'
    
class MatchDetails:
    def __init__(self, data):
        self.data = data
    def has_match(self):
        return len(self.data) > 0

class Matcher(ABC):
    @abstractmethod
    def __init__(self, comparer, ignorer, threshold):
        self.comparer = comparer
        self.ignorer = ignorer
        self.threshold = threshold
        self.matches = None
                 
    @abstractmethod
    def match(self, post)->MatchDetails:
        pass

    def is_match(self, match_detail: MatchDetail, threshold=None):
        if threshold is None:
            threshold = self.threshold
        return (match_detail
                and match_detail.closeness >= threshold)

    def collapse_matches(self, details: MatchDetails)->MatchDetails:
        detail_map = {}
        for detail in details.data:
            if (detail in detail_map and (detail > detail_map[detail])) or (detail not in detail_map):
                detail_map[detail] = detail
        return MatchDetails(list(detail_map.values()))
        

class PhraseMatcher(Matcher):
    def make_phrases(self, text_list):
        max_phrase_len = self.get_phrase_len()
        for text in text_list:
            if not text:
                continue
            words = text.replace('/', ' ').strip().split(' ')
            skip = 0
            for word_pos in range(len(words)):
                for offset in range(max_phrase_len, 0, -1):
                    if word_pos + offset > len(words):
                        continue
                    yield ' '.join(words[word_pos:word_pos+offset])
    @abstractmethod
    def get_phrase_len(self)->int:
        pass

    @abstractmethod
    def get_origin_text(self, post)->str:
        pass

    def try_match(self, phrase):
        if phrase.lower() in self.wiki._items:
            return MatchDetail(self.wiki._items[phrase.lower()], phrase, 1)
        phrase_len = phrase.count(' ') + 1
        for name in self.wiki._items:
            item = self.wiki._items[name]
            match = MatchDetail(item, phrase, self.comparer.compare(phrase, item.name))
            if self.is_match(match, self.threshold**phrase_len):
                return match
        return None
    
    def match(self, post):
        self.matches = MatchDetails([])
        match_len = 0
        skip = 0
        for phrase in self.make_phrases(self.get_origin_text(post)):
            if phrase.count(' ')+1 < match_len:
                continue
            if phrase.count(' ')+1 == match_len:
                skip = skip - 1
            if skip > 0:
                continue

            if self.ignorer.want_ignore(phrase):
                match_len = phrase.count(' ')+1
                skip = match_len-1
                continue
            
            details = self.try_match(phrase)
            if (self.is_match(details)
                and not details.item.ignorer.want_ignore(details.src)):
                self.matches.data.append(details)
                match_len = details.src.count(' ')+1
                skip = match_len-1
                if details.item.name == 'Hermes':
                    print('hermes: ', phrase)
            elif details and details.item.ignorer.want_ignore(details.src):
                match_len = details.src.count(' ')+1
                skip = match_len-1
                
        self.matches = self.collapse_matches(self.matches)
        return self.matches

class WikiMatcher(PhraseMatcher):
    def __init__(self, comparer, ignorer, wiki, threshold):
        super().__init__(comparer, ignorer, threshold)
        self.wiki = wiki

    def get_phrase_len(self)->int:
        return self.wiki.max_word_cnt

    def get_origin_text(self, post)->str:
        text = [post.title]
        if post.selftext:
            text.append(post.selftext)
        text = [re.sub('[^0-9a-z-A-Z \[\]]+', '', t) for t in text]
        return text

class EnvokedWikiMatcher(WikiMatcher):
    def make_phrases(self, text_list):
        res = re.findall(r'\[\[.*?\]\]', text_list)
        return [r[2:-2] for r in res]
    
