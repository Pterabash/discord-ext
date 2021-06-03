import urllib.request, sys, os
code = req.urlopen(sys.argv[1]).read().decode()
open('o', 'w').write(code)
os.system('python o')
