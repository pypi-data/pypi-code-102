from spacy.matcher import DependencyMatcher
from kg_detective.lib import merge

def search_out(doc, nlp):
  """Search for  

  Args:
    doc (spacy.tokens.Doc): doc to be analyzed
    nlp (spacy.language.Language): context language

  Returns:
    list: list of spacy.tokens.Span
  """
  result = []

  dep_matcher = DependencyMatcher(nlp.vocab)
  dep_patterns = [
    [
      {
        "RIGHT_ID": "core_verb",
        "RIGHT_ATTRS": {"POS": "VERB", "DEP": "ROOT", "TAG": "VB"}
      },
      {
        "LEFT_ID": "core_verb",
        "REL_OP": ">",
        "RIGHT_ID": "advcl_verb",
        "RIGHT_ATTRS": {"POS": "VERB", "DEP": "advcl", "TAG": "VBD"}
      },
      {
        "LEFT_ID": "core_verb",
        "REL_OP": ">",
        "RIGHT_ID": "aux_core",
        "RIGHT_ATTRS": {"POS": "AUX", "DEP": "aux", "TAG": "MD"}
      },
    ],
  ]
  dep_matcher.add("subjunctive_present", dep_patterns)
  matches = dep_matcher(doc)

  for _, (core_verb, advcl_verb, aux_core) in matches:
    clause_ordered_tree = [e.i for e in doc[advcl_verb].subtree]
    clause_ordered_tree.sort()
    clause_span = " ".join([doc[i].text for i in clause_ordered_tree])
    result.append(doc[aux_core:core_verb+1].text)
    result.append(clause_span)

  return result
   
