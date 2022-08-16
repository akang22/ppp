import glob
from PIL import Image


# error that is recovreable but needs user intention
def print_debug_log(string):
    """Print"""
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
                except_str = f"[{wd}] {len(matched_files)} files found matching glob"
                f"{next_str_match}: {', '.join(matched_files)}"
                raise EvaluationException(except_str)
            else:
                print_debug_log(f"[{wd}] search terminated at {next_str_match}")
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
        book_path = "/Volumes/KOBOeReader/Library/GPUBundles/x64compatible/kube/"
        chap_name = "Volume. 1 Chapter. 1"
        books = list(order_list("?-*.jpg", 1, chap_name + "/"))
        books = [Image.open(book_path + name) for name in books]
        books[0].save(
            book_path + chap_name + ".pdf",
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=books[1:],
        )
        pass
    except EvaluationException as e:
        print("Evaluation Exception. Please resolve before rerunning.")
        print(e)


if __name__ == "__main__":
    main()
