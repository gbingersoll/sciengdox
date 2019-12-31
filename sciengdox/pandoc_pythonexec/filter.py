import panflute
from panflute import debug  # zzz
import pexpect
import re
import urllib


class PythonRunner(object):
    prompt = r'>>> '
    continuation = r'\.\.\. '

    def __init__(self):
        self.proc = pexpect.spawn('python')
        self.proc.expect(PythonRunner.prompt)

    def run_lines(self, lines, echo_input=True, repl_prefix=None):
        indent_level = 0
        output = ""

        for idx, line in enumerate(lines):
            # handle empty line in indent
            if line == "" and indent_level != 0:
                if idx == len(lines) - 1:
                    # last line
                    this_level = 0
                else:
                    # find next indent level
                    for l in lines[(idx + 1):]:
                        if l != "":
                            this_level = self._indent_level(l)
                            break
                line = '    ' * this_level

            indent_level = self._indent_level(line)

            # Send the command and capture the result
            self.proc.sendline(line)
            self.proc.expect([PythonRunner.prompt, PythonRunner.continuation])
            result = self.proc.before.decode('utf-8')
            if echo_input:
                result = (repl_prefix or '') + result
            else:
                # Remove input line and any leading line break
                result = re.sub(r'^\r?\n', '', result[len(line):])
            output += result

        return output

    def close(self):
        self.proc.sendline('exit()')
        self.proc.close()
        return self.proc.exitstatus, self.proc.signalstatus

    def _indent_level(self, line):
        m = re.search(r'^\s*', line)
        if m is not None:
            return int(len(m[0]) / 4)
        return 0


def prepare(doc):
    doc.elements_to_replace = []
    doc.replacement_elements = []


def element_classes(elem):
    return elem.classes if hasattr(elem, 'classes') else []


def find_inline_code(text):
    m = re.search(r'`([^`]*?)`{([^}]*?)}', text)
    if m is not None:
        code = m[1]
        classes = list(map(lambda c: c[1:] if c[0] == '.' else None,
                           m[2].split(' ')))
        classes = [c for c in classes if c]  # Remove None values
        return (code, classes, m.span())

    return None


def replace_embedded_code_with_result(text, doc):
    found = find_inline_code(text)
    if found is not None:
        code, classes, span = found
        if 'python' in classes:
            # Run the code
            result = exec_inline_python(panflute.Str(code), doc).text

            # Replace the result in the Math element
            text = text[0:span[0]] + result + text[span[1]:]

    return text


def instantiate_python_runner(doc):
    # Instantiate runner if it does not exist
    try:
        doc.python_runner
    except AttributeError:
        doc.python_runner = PythonRunner()


def exec_python_block(elem, doc):
    instantiate_python_runner(doc)
    repl_prefix = '>>> ' if 'repl' in element_classes(elem) else None
    elem.text = doc.python_runner.run_lines(elem.text.splitlines(),
                                            repl_prefix=repl_prefix)
    if 'echo' in element_classes(elem):
        return None
    return []


def exec_inline_python(elem, doc):
    instantiate_python_runner(doc)
    elem.text = doc.python_runner.run_lines([elem.text],
                                            echo_input=False).strip()

    if 'asCode' in element_classes(elem):
        return None
    return panflute.Str(elem.text)


def exec_code_in_image(elem, doc):
    # Remove escape characters from image url
    url = urllib.parse.unquote(elem.url)

    # Execute any embedded code replacing it with the output result
    url = replace_embedded_code_with_result(url, doc)

    # Remove any single quotes around executed output
    url = re.sub(r'\'', '', url)

    # Restore escaped nature of image url
    elem.url = urllib.parse.quote(url)
    return None


def replace_element(doc, old_elem, new_elem):
    if isinstance(old_elem, panflute.Inline):
        if isinstance(new_elem, panflute.Inline):
            return new_elem
        elif isinstance(new_elem, panflute.Block):
            # new_elem is block.  Need to replace parent.
            doc.elements_to_replace.append(old_elem.parent)
            doc.replacement_elements.append(new_elem)
    elif isinstance(old_elem, panflute.Block):
        if isinstance(new_elem, panflute.Block):
            return new_elem
        if isinstance(new_elem, panflute.Inline):
            # new_elem is inline.  Wrap in paragraph.
            return panflute.Para(new_elem)
    return None


def handle_postponed_replacements(elem, doc):
    try:
        idx = doc.elements_to_replace.index(elem)
        return doc.replacement_elements[idx]
    except ValueError:
        return None


def exec_code_blocks(elem, doc):
    classes = element_classes(elem)
    if type(elem) == panflute.Image:
        return exec_code_in_image(elem, doc)

    if type(elem) == panflute.Math:
        elem.text = replace_embedded_code_with_result(elem.text, doc)
        return None

    if 'noexec' not in classes:
        if (type(elem) == panflute.Code and
                re.match(r'^pq\(.*\)$', elem.text)):
            # Handle special case of printing a quantity if all that
            # is in the code block is `pq(value)`
            exec_inline_python(elem, doc)
            new_element = panflute.convert_text(elem.text)[0]
            return panflute.Span(*new_element.content)
        if 'python' in classes:
            if type(elem) == panflute.CodeBlock:
                return exec_python_block(elem, doc)
            elif type(elem) == panflute.Code:
                result = exec_inline_python(elem, doc)
                if 'md' in classes:
                    new_element = panflute.convert_text(elem.text)[0]
                    return replace_element(doc, elem, new_element)
                return result


def finalize(doc):
    try:
        doc.python_runner.close()
    except AttributeError:
        pass


def main(doc=None):
    return panflute.run_filters([exec_code_blocks,
                                 handle_postponed_replacements],
                                prepare=prepare,
                                finalize=finalize,
                                doc=doc)


if __name__ == "__main__":
    main()
