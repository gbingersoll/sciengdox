import panflute
from panflute import debug  # zzz
import pexpect
import re


class PythonRunner(object):
    prompt = r'>>> '
    continuation = r'\.\.\. '

    def __init__(self):
        self.proc = pexpect.spawn('python')
        self.proc.expect(PythonRunner.prompt)

    def run_lines(self, lines, echo_input=True):
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
            if not echo_input:
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
    pass


def element_classes(elem):
    return elem.classes if hasattr(elem, 'classes') else []


def instantiate_python_runner(doc):
    # Instantiate runner if it does not exist
    try:
        doc.python_runner
    except AttributeError:
        doc.python_runner = PythonRunner()


def exec_python_block(elem, doc):
    instantiate_python_runner(doc)
    elem.text = doc.python_runner.run_lines(elem.text.splitlines())
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


def exec_code_in_math(elem, doc):
    m = re.search(r'`([^`]*?)`{([^}]*)}', elem.text)
    if m is not None:
        code = m[1]
        classes = m[2]
        if '.python' in classes:
            # Run the code
            result = exec_inline_python(panflute.Str(code), doc).text

            # Replace the result in the Math element
            before = elem.text[0:m.span()[0]]
            after = elem.text[m.span()[1]:]
            elem.text = before + result + after

    return None


def exec_code_blocks(elem, doc):
    classes = element_classes(elem)
    if type(elem) == panflute.Math:
        return exec_code_in_math(elem, doc)

    if 'python' in classes and 'noexec' not in classes:
        if type(elem) == panflute.CodeBlock:
            return exec_python_block(elem, doc)
        elif type(elem) == panflute.Code:
            return exec_inline_python(elem, doc)


def finalize(doc):
    try:
        doc.python_runner.close()
    except AttributeError:
        pass


def main(doc=None):
    return panflute.run_filter(exec_code_blocks,
                               prepare=prepare,
                               finalize=finalize,
                               doc=doc)


if __name__ == "__main__":
    main()
