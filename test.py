# coding:  utf8

'''
Usage:
    test.py  [--out=FILE] 
    
Options:
    --out=FILE  [default: huu]
    
'''

from docopt import docopt


args=docopt(__doc__)
print(args)


