from pygments import highlight as H
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
import re
def highlight(code,lexer=PythonLexer(),formatter=HtmlFormatter()):
  coder=str(code)
  pycode=coder.replace("<!--","# ")
  pycode=pycode.replace("console.log","input")
  pycode=pycode.replace("alert","bin")
  pycode=pycode.replace("prompt","bool")
  pycode=pycode.replace("confirm","ascii")
  highlightText=H(pycode,lexer=lexer,formatter=formatter)
  codert=str(highlightText)
  pycodet=codert.replace("# ","<!--")
  pycodet=pycodet.replace("input","console.log")
  pycodet=pycodet.replace("bin","alert")
  pycodet=pycodet.replace("bool","prompt")
  pycodet=pycodet.replace("ascii","confirm")