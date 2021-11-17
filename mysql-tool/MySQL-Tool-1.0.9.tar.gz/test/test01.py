"""
Installing collected packages: pycparser, pyparsing, cffi, zipp, webencodings, urllib3, typing-extensions, six, packaging, jeepney, idna, cryptography, charset-normalizer, certifi, SecretStorage, requests, Pygments, importlib-metadata, docutils, bleach, tqdm, rfc3986, requests-toolbelt, readme-renderer, pkginfo, keyring, colorama, twine
Successfully installed Pygments-2.10.0 SecretStorage-3.3.1 bleach-4.1.0 certifi-2021.5.30 cffi-1.14.6 charset-normalizer-2.0.6 colorama-0.4.4 cryptography-3.4.8 docutils-0.17.1 idna-3.2 importlib-metadata-4.8.1 jeepney-0.7.1 keyring-23.2.1 packaging-21.0 pkginfo-1.7.1 pycparser-2.20 pyparsing-2.4.7 readme-renderer-29.0 requests-2.26.0 requests-toolbelt-0.9.1 rfc3986-1.5.0 six-1.16.0 tqdm-4.62.3 twine-3.4.2 typing-extensions-3.10.0.2 urllib3-1.26.7 webencodings-0.5.1 zipp-3.5.0

"""
from mysql_tool.mysql_tool import my_mysql
host = "server04"
password = "bestwond2019"
db = my_mysql(host=host, user="root", port=3306, database="gaas", password=password)

sql = "select * from device where device_number=%s;"
data = db.my_fetchone(sql, ['2000000036'], return_type='dict')
print(data)

sql = "select * from device where device_number=%(device_number)s;"
data = db.my_fetchone(sql, {"device_number":'2000000036'}, return_type='dict')
print(data)

