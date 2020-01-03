import re


class TableCell(object):
    def __init__(self, content, max_width=None):
        manual_lines = str(content).split('\n')
        if max_width:
            self.lines = []
            for mr in manual_lines:
                words = re.split(r'\s+', mr)
                sublines = [words[0]]
                for w in words[1:]:
                    if (len(sublines[-1]) + len(w) + 1) <= max_width:
                        sublines[-1] += ' ' + w
                    else:
                        sublines.append(w)
                self.lines += sublines
        else:
            self.lines = manual_lines

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, indices):
        if isinstance(indices, slice):
            if (indices.step or 1) > 1:
                raise ValueError("Skipping lines not allowed")

        lines = []
        try:
            lines = self.lines.__getitem__(indices)
        except IndexError:
            return ''

        if isinstance(indices, slice):
            requested_lines = ((indices.stop or len(self.lines)) -
                               (indices.start or 0))
            lines += [''] * (requested_lines - len(lines))

        return lines

    @property
    def width(self):
        return max(map(lambda a: len(a), self.lines))


class TableLine(object):
    def __init__(self, cells):
        self.cells = cells

    def __len__(self):
        return len(self.cells)

    def __getitem__(self, indices):
        return self.cells.__getitem__(indices)

    @property
    def width(self):
        return max(map(lambda a: a.width, self.cells))

    @property
    def height(self):
        return max(map(lambda a: len(a), self.cells))


class Table(object):
    def __init__(self, cell_strings, max_widths=None, headerless=False):
        cell_strings = cell_strings or [[]]
        if not isinstance(cell_strings, list):
            cell_strings = [cell_strings]
        if not isinstance(cell_strings[0], list):
            cell_strings = [cell_strings]

        # Store max column widths
        self.max_widths = max_widths or [None] * len(cell_strings[0])

        # Convert cell strings to TableCell
        self.cells = []
        for row in cell_strings:
            cells = []
            for idx, col in enumerate(row):
                cells.append(TableCell(col, self.max_widths[idx]))
            self.cells.append(cells)

        self._headerless = headerless

    @property
    def headerless(self):
        return self._headerless

    @headerless.setter
    def headerless(self, h):
        self._headerless = h

    @property
    def num_rows(self):
        if len(self.cells) == 1 and len(self.cells[0]) == 0:
            return 0
        return len(self.cells)

    @property
    def num_cols(self):
        return len(self.cells[0])

    def __getitem__(self, indices):
        if isinstance(indices, tuple):
            if len(indices) != 2:
                raise ValueError("Expected 2 indices")

            if not isinstance(indices[0], slice):
                return self.cells[indices[0]].__getitem__(indices[1])

            retval = []
            rows = self.cells.__getitem__(indices[0])
            for rr in rows:
                retval.append(rr.__getitem__(indices[1]))

            return retval

        return self.cells.__getitem__(indices)

    def insert_row(self, idx, cell_strings, max_widths=None):
        new_row = self._build_new_row(cell_strings, max_widths)
        if self.num_cols == 0:
            self.cells[0] = new_row
        else:
            self.cells.insert(idx, new_row)

    def append_row(self, cell_strings, max_widths=None):
        new_row = self._build_new_row(cell_strings, max_widths)
        if self.num_cols == 0:
            self.cells[0] = new_row
        else:
            self.cells.append(new_row)

    def insert_column(self, idx, cell_strings, max_width=None):
        self._add_new_col(cell_strings, max_width, idx)

    def append_column(self, cell_strings, max_width=None):
        self._add_new_col(cell_strings, max_width)

    def markdown(self, caption, label, alignments=None, footnotes=None):
        # build horizontal dividers
        column_widths = self._column_widths()
        alignments = alignments or 'd'*self.num_cols
        header_divider = [self._aligned_header(w, alignments[i])
                          for i, w in enumerate(column_widths)]
        header_divider = '+' + '+'.join(header_divider) + '+'
        row_divider = re.sub(r'[=:]', '-', header_divider)
        line_divider = re.sub(r'[=:]', ' ', header_divider)
        line_divider = re.sub(r'[+]', '|', line_divider)

        # initialize output
        strings = [row_divider]
        header_divider_idx = None

        # iterate through rows
        for r in range(self.num_rows):
            num_lines = TableLine(self[r, :]).height
            for ll in range(num_lines):
                segments = [self._pad_string(self[r, c][ll], column_widths[c])
                            for c in range(self.num_cols)]
                strings.append('| ' + ' | '.join(segments) + ' |')
                strings.append(line_divider)

            strings[-1] = row_divider
            header_divider_idx = header_divider_idx or (len(strings) - 1)

        # replace header divider string
        if self._headerless:
            strings[0] = header_divider
        else:
            strings[header_divider_idx] = header_divider

        # Build caption and label
        caption = f"\n\nTable: {caption} {{#{label}}}\n"

        # Build footnote text
        footnote_str = ''
        if footnotes is not None:
            for name in footnotes:
                footnote_str += f"\n[^{name}]: {footnotes[name]}"
            footnote_str += '\n'

        # Combine everything and return
        return ('\n'.join(strings) + caption + footnote_str)

    def _build_new_row(self, cell_strings, max_widths=None):
        if len(self.max_widths) and max_widths is not None:
            raise ValueError('Max widths already established on table')

        if self.num_cols == 0:
            self.max_widths = max_widths or [None] * len(cell_strings)
        else:
            self._compare_dims(self.num_cols, len(cell_strings))

        return [TableCell(a, self.max_widths[i])
                for i, a in enumerate(cell_strings)]

    def _add_new_col(self, cell_strings, max_width=None, idx=None):
        new_col = [TableCell(a, max_width) for a in cell_strings]
        if self.num_rows == 0:
            self.cells = [[x] for x in new_col]
        else:
            self._compare_dims(self.num_rows, len(cell_strings))
            for j, row in enumerate(self.cells):
                if idx is None:
                    row.append(new_col[j])
                else:
                    row.insert(idx, new_col[j])
        if idx is None:
            self.max_widths.append(max_width)
        else:
            self.max_widths.insert(idx, max_width)

    def _compare_dims(self, a, b):
        if a != b:
            raise ValueError(f"Expected {a} items, got {b}")

    def _column_widths(self):
        widths = []
        for i in range(self.num_cols):
            widths.append(TableLine(self[:, i]).width)
        return widths

    def _pad_string(self, str, width):
        return str + (' ' * (width - len(str)))

    def _aligned_header(self, width, alignment):
        header = '=' * (width + 2)
        if alignment == 'l':
            header = ':' + header[1:]
        elif alignment == 'c':
            header = ':' + header[1:-1] + ':'
        elif alignment == 'r':
            header = header[0:-1] + ':'

        return header


if (__name__ == '__main__'):
    tbl = Table([['abc def', 'bcd', 'xyz'],
                 ['egg', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']],
                max_widths=[4, None, 4])
    print(tbl.markdown('my caption', 'tbl:label', 'crl'))
