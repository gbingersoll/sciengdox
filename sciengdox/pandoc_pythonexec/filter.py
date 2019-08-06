from panflute import *


def echo_code_blocks(elem, doc):
    if type(elem) == CodeBlock:
        debug(elem.text)


def main(doc=None):
    return run_filter(echo_code_blocks, doc=doc)


if __name__ == "__main__":
    main()
