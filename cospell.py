# Main loop
from spylls.hunspell import *
from spylls.hunspell import readers
import re
import argparse
from spell.es_check import ES_checker
from spell.en_check import EN_checker

if __name__ == '__main__':
    # Start to set parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str)
    parser.add_argument('--lag', type=str,default='es',help="en, es")
    parser.add_argument('--dict', type=str, help="en_US, es_red", default='0')
    args = parser.parse_args()

    print(f'Start to load file {args.file}')
    if args.dict == '0':
        if args.lag == 'es':
            ES = ES_checker(args.file)
            ES.check()
        elif args.lag == 'en':
            EN = EN_checker(args.file)
            EN.check()

    else:
        if args.lag == 'es':
            ES = ES_checker(args.file, args.dict)
            ES.check()
        elif args.lag == 'en':
            EN = EN_checker(args.file, args.dict)
            EN.check()

