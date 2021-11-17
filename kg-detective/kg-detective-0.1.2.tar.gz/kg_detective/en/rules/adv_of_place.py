import os
from spacy.matcher import PhraseMatcher
from kg_detective.lib import merge


def search_out(doc, nlp):
  """Search for adverbs of place 

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  pkg_path = os.path.dirname(__file__)
  PLACE = open(pkg_path + '/adv_place.txt', 'r').read().splitlines() 

  matcher = PhraseMatcher(nlp.vocab)

  patterns = [nlp.make_doc(text) for text in PLACE]
  matcher.add("adv_place", patterns)

  matches = matcher(doc)
  token_ranges = [(start, end) for _, start, end in matches]

  refined_matches = merge(token_ranges)
  for start, end in refined_matches:
    span = doc[start:end]
    if any([e.pos_ == "ADV" for e in list(span)]):
      result.append({"text": span.text}) 
  return result
   
