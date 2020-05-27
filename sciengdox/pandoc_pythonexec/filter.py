import panflute
import re
import urllib
import asyncio
from itertools import chain


# Wrapper to always provide a list of classes
def element_classes(elem):
    return elem.classes if hasattr(elem, 'classes') else []


class PythonRunner(object):
    prompt = '>>> '
    continuation = '... '

    def __init__(self):
        self._proc = None

    async def start(self):
        assert self._proc is None
        self._proc = await asyncio.subprocess.create_subprocess_exec(
            "python",
            "-i",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT)
        return await self._wait_for_prompt()

    async def run_lines(self, lines, echo_input=True, repl=False):
        indent_level = 0
        output = PythonRunner.prompt

        for idx, line in enumerate(lines):
            # handle empty line in indent
            if line == "" and indent_level != 0:
                if idx == len(lines) - 1:
                    # last line
                    this_level = 0
                else:
                    # find next indent level
                    for el in lines[(idx + 1):]:
                        if el != "":
                            this_level = self._indent_level(el)
                            break
                line = '    ' * this_level

            indent_level = self._indent_level(line)

            # Send the command and capture the result
            self._sendline(line)

            result = await self._wait_for_prompt()

            # Remove any leading line break from result and combine
            # with the input.  Note that this includes prompts which
            # may get removed below depending on args.
            #
            # If the input line was blank, output a space in its place to avoid
            # the blank line getting dropped in HTML output.
            output += ((line if line != "" else " ") + '\n' +
                       re.sub(r'^\r?\n', '', result))

        # Split output into individual lines
        output_lines = output.split('\n')

        # Remove trailing prompt from result
        del output_lines[-1]

        if echo_input:
            if not repl:
                # Remove prompts from the beginning of lines
                output_lines = list(map(
                    lambda x: re.sub(r'^(>>>|\.\.\.)\s', '', x), output_lines))
        else:
            # Remove echoed input lines
            output_lines = list(filter(
                lambda x: not re.search(r'^(>>>|\.\.\.)\s', x), output_lines))

        return '\n'.join(output_lines)

    async def close(self):
        assert self._proc is not None
        self._sendline('exit()')
        await self._proc.wait()

    def _sendline(self, line):
        assert self._proc is not None
        self._proc.stdin.write(str.encode(line + '\r\n'))

    async def _wait_for_prompt(self):
        prompt_bytes = PythonRunner.prompt.encode()
        continuation_bytes = PythonRunner.continuation.encode()

        output = b''

        while True:
            if output[-len(prompt_bytes):] == prompt_bytes:
                break
            if output[-len(continuation_bytes):] == continuation_bytes:
                break
            output += await self._proc.stdout.read(1024)
        return output.decode()

    def _indent_level(self, line):
        m = re.search(r'^\s*', line)
        if m is not None:
            return int(len(m[0]) / 4)
        return 0


def find_inline_code(text):
    m = re.search(r'`([^`]*?)`{([^}]*?)}', text)
    if m is not None:
        code = m[1]
        classes = list(map(lambda c: c[1:] if c[0] == '.' else None,
                           m[2].split(' ')))
        classes = [c for c in classes if c]  # Remove None values
        return (code, classes, m.span())

    return None


async def replace_embedded_code_with_result(text, doc):
    found = find_inline_code(text)
    if found is not None:
        code, classes, span = found
        if 'python' in classes:
            # Run the code
            result = (await exec_inline_python(panflute.Str(code), doc)).text

            # Replace the result in the Math element
            text = text[0:span[0]] + result + text[span[1]:]

    return text


async def exec_python_block(elem, doc):
    elem.text = await doc.runner.run_lines(
        elem.text.splitlines(),
        repl=('repl' in element_classes(elem)))
    if 'echo' in element_classes(elem):
        return None
    return []


async def exec_inline_python(elem, doc):
    elem.text = await doc.runner.run_lines([elem.text], echo_input=False)
    elem.text = elem.text.strip()

    if 'asCode' in element_classes(elem):
        return None
    return panflute.Str(elem.text)


async def exec_code_in_image(elem, doc):
    # Remove escape characters from image url
    url = urllib.parse.unquote(elem.url)

    # Execute any embedded code replacing it with the output result
    url = await replace_embedded_code_with_result(url, doc)

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


# Basically a copy of Element.walk from panflute, but converted to be async.
# See https://github.com/sergiocorreia/panflute/blob/master/panflute/base.py
async def async_walk(element, action, doc=None):
    # Infer the document thanks to .parent magic
    if doc is None:
        doc = element.doc

    # Iterate over children
    for child in element._children:
        obj = getattr(element, child)
        if isinstance(obj, panflute.Element):
            ans = await async_walk(obj, action, doc)
        elif isinstance(obj, panflute.ListContainer):
            ans = []
            for item in obj:
                ans.append(await async_walk(item, action, doc))
            # We need to convert single elements to iterables, so that they
            # can be flattened later
            ans = ((item,) if type(item) != list else item for item in ans)
            # Flatten the list, by expanding any sublists
            ans = list(chain.from_iterable(ans))
        elif isinstance(obj, panflute.DictContainer):
            ans = []
            for k, v in obj.items():
                ans.append((k, await async_walk(v, action, doc)))
            ans = [(k, v) for k, v in ans if v != []]
        elif obj is None:
            ans = None  # Empty table headers or captions
        else:
            raise TypeError(type(obj))
        setattr(element, child, ans)

    # Then apply the action to the element
    altered = await action(element, doc)
    return element if altered is None else altered


async def exec_code_blocks(elem, doc):
    classes = element_classes(elem)
    if type(elem) == panflute.Image:
        return await exec_code_in_image(elem, doc)

    if type(elem) == panflute.Math:
        elem.text = await replace_embedded_code_with_result(elem.text, doc)
        return None

    if 'noexec' not in classes:
        if (type(elem) == panflute.Code and
                re.match(r'^p(q|md)\(.*\)$', elem.text)):
            # Handle special case of printing a quantity or raw markdown if all
            # that is in the code block is `pq(value)` or `pmd(value)`
            await exec_inline_python(elem, doc)
            new_element = panflute.convert_text(elem.text)[0]
            return panflute.Span(*new_element.content)
        if 'python' in classes:
            if type(elem) == panflute.CodeBlock:
                return await exec_python_block(elem, doc)
            elif type(elem) == panflute.Code:
                result = await exec_inline_python(elem, doc)
                if 'md' in classes:
                    new_element = panflute.convert_text(elem.text)[0]
                    return replace_element(doc, elem, new_element)
                return result


async def walk_and_execute_code(doc):
    doc.runner = PythonRunner()
    doc.elements_to_replace = []
    doc.replacement_elements = []

    starting_output = await doc.runner.start()

    doc = await async_walk(doc, exec_code_blocks)

    await doc.runner.close()


def handle_postponed_replacements(elem, doc):
    try:
        idx = doc.elements_to_replace.index(elem)
        return doc.replacement_elements[idx]
    except ValueError:
        return None


def main(doc=None):
    from sys import platform
    if platform == "win32":
        # Check that the user's system is set to use UTF-8 for IO
        import os
        try:
            ioencoding = os.environ["PYTHONIOENCODING"]
        except KeyError:
            ioencoding = 'undefined'
        if ioencoding != 'utf-8':
            raise Exception('Fix interprocess IO by setting a Windows '
                            'environment variable: PYTHONIOENCODING=utf-8')

    doc = panflute.load()
    asyncio.run(walk_and_execute_code(doc))
    doc = doc.walk(handle_postponed_replacements)
    panflute.dump(doc)


if __name__ == "__main__":
    main()
