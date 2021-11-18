#from Hgments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from pygments import highlight as H
class highlight(object):
 def highlight(self,code,lexer=PythonLexer(),formatter=HtmlFormatter()):
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
  return pycodet
if __name__=="__main__":
  print ("正在运行测试......")
  h=highlight().highlight(
  """
<!--Html code-->
<html>
<head>
<meta charset="utf-8">
</head>
<body>
</body>
</html>
  """)
  print (h)