import glob
import string
import random
import os
import sys
from PIL import image

# error that is recovreable but needs user intention
def print_debug_log(string):
    print(string)

class EvaluationException(Exception):
    pass

def abstract_generator(str_gen, wd):
    while True:
        next_str_match = next(str_gen)
        matched_files = glob.glob(wd + next_str_match)
        if len(matched_files) == 1:
            yield matched_files[0]
        else:
            if len(matched_files) > 1:
                raise EvaluationException(f"[{wd}] {len(matched_files)} files found matching glob {next_str_match}: {', '.join(matched_files)} ")
            else:
                print_debug_log(f'[{wd}] search terminated at {next_str_match}')
                return


def increasing_gen():
    i = 1
    while True:
        yield i
        i += 1


def number_glob_gen(re, pos):
    return (re[:pos] + str(i) + re[pos:] for i in increasing_gen())


def order_list(re, pos, wd):
    return abstract_generator(number_glob_gen(re, pos), wd)


def main():
    try:
        pdf = FPDF()
        book_path = '/Volumes/KOBOeReader/Library/GPUBundles/x64compatible/kube/'
        books = list(orderList('?-*.jpg', 1, 'Volume. 1 Chapter. 1/'))
        for book in books:
            pdf.add_page()
        pass
    except EvaluationException as e:
        print('Evaluation Exception. Please resolve before rerunning.')
        print(e)
    

if __name__ == '__main__':
    main()
