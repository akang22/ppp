import glob
import string
import random
import os

# error that is recovreable but needs user intention
def printDebugLog(string):
    print(string)

class EvaluationException(Exception):
    pass

def abstractGenerator(str_gen, wd):
    while True:
        next_str_match = next(str_gen)
        matched_files = glob.glob(next_str_match, wd)
        if len(matched_files) == 1:
            yield matched_files[0]
        else:
            if len(matched_files) > 1:
                except EvaluationException(f'[{wd}] {len(matched_files)} files found matching glob {next_str_match}: {', '.join(matched_files)} ')
            else:
                printDebugLog(f'[{wd}] search terminated at {next_str_match}')
                return


def increasingGen():
    i = 1
    while True:
        yield i
        i += 1


def numberGlobGen(re, pos):
    return (re[:pos] + str(i) + re[pos:] for i in increasingGen())


def orderList(re, pos, wd)
    return abstractGenerator(numberGlobGen(re, pos), wd)

# glob: basic glob, with order available as 
# working directory (which contains every folder
# end directory
def convertFolderToPdf(glob, wd, ed):
    file_name = os.pathname '.pdf'
if glob

i = 1
while glob.glob:
    

if name == '__main__':
    main()
