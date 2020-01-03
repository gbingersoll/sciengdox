from sciengdox.tables import Table, TableLine, TableCell
from pytest import raises


def test_TableCell_init_stores_data():
    tc = TableCell("my cell contents")
    assert tc[0] == "my cell contents"


def test_TableCell_init_stores_non_string_data_as_string():
    tc = TableCell(1789)
    assert tc[0] == "1789"


def test_TableCell_len_gives_row_count():
    assert len(TableCell("my cell contents")) == 1


def test_TableCell_init_splits_text_at_line_breaks():
    tc = TableCell("my cell\ncontents")
    assert len(tc) == 2
    assert tc[0] == "my cell"
    assert tc[1] == "contents"


def test_TableCell_init_splits_rows_at_max_width_using_whitespace():
    tc = TableCell("my cell  contents", max_width=7)
    assert len(tc) == 2
    assert tc[0] == "my cell"
    assert tc[1] == "contents"

    tc = TableCell("my cell  contents", max_width=6)
    assert len(tc) == 3
    assert tc[0] == "my"
    assert tc[1] == "cell"
    assert tc[2] == "contents"


def test_TableCell_allows_indexing_multiple_rows_of_text():
    tc = TableCell("my cell  contents", max_width=6)
    assert len(tc) == 3
    assert tc[0] == "my"
    assert ' '.join(tc[1:]) == "cell contents"


def test_TableCell_width_returns_width_of_widest_line():
    assert TableCell("my cell  contents", max_width=10).width == 8
    assert TableCell("your cell  stuff", max_width=6).width == 5


def test_TableCell_init_simultaneously_splits_on_line_breaks_and_max_width():
    tc = TableCell("this is a cell\nwith some manual\nbreaks", max_width=9)
    assert len(tc) == 5
    assert tc[0] == "this is a"
    assert tc[1] == "cell"
    assert tc[2] == "with some"
    assert tc[3] == "manual"
    assert tc[4] == "breaks"


def test_TableCell_returns_empty_string_for_out_of_range_line_index():
    tc = TableCell("my cell  contents", max_width=6)
    assert len(tc) == 3
    assert tc[0] == "my"
    assert tc[1] == "cell"
    assert tc[2] == "contents"
    assert tc[-1] == "contents"
    assert tc[-2] == "cell"
    assert tc[-3] == "my"

    assert tc[3] == ""
    assert tc[-4] == ""


def test_TableCell_raises_exception_for_skipping_lines():
    tc = TableCell("my cell  contents", max_width=6)
    assert tc[0:2:1] == ['my', 'cell']
    with raises(ValueError, match=r'Skipping lines not allowed'):
        tc[0:3:2]


def test_TableCell_returns_empty_string_array_for_out_of_range_line_indexes():
    tc = TableCell("my cell  contents", max_width=6)
    assert len(tc) == 3
    assert tc[0:2] == ['my', 'cell']
    assert tc[0:3] == ['my', 'cell', 'contents']
    assert tc[0:4] == ['my', 'cell', 'contents', '']


def test_TableLine_init_stores_provided_cells():
    tl = TableLine([TableCell("a"), TableCell("b"), TableCell("c")])
    assert len(tl) == 3
    assert tl[0][0] == "a"
    assert tl[1][0] == "b"
    assert tl[2][0] == "c"


def test_TableLine_width_returns_widest_width():
    tl = TableLine([TableCell("abcd"), TableCell("ef"), TableCell("g")])
    assert tl.width == 4


def test_TableLine_height_returns_largest_line_count():
    tl = TableLine([TableCell("a"), TableCell("ef\ngh\ni"), TableCell("j\nk")])
    assert tl.height == 3


def test_Table_stores_initial_strings_as_cells():
    tbl = Table([['a', 'b', 'c'], ['d', 'e', 'f']])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 3
    assert tbl[0][1][0] == 'b'
    assert tbl[1][2][0] == 'f'


def test_Table_is_indexable_with_tuple():
    tbl = Table([['a', 'b', 'c'], ['d', 'e', 'f']])
    subtable = tbl[0, 2]
    assert tbl[0, 2][0] == 'c'
    assert tbl[1, 0][0] == 'd'
    with raises(ValueError, match=r'Expected 2 indices'):
        tbl[1, 0, 1]


def test_Table_is_subsettable():
    tbl = Table([['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']])
    subtable = tbl[1:, 2]
    assert subtable[0][0] == 'f'
    assert subtable[1][0] == 'i'
    subtable = tbl[:, 1:3]
    assert subtable[0][0][0] == 'b'
    assert subtable[0][1][0] == 'c'
    assert subtable[1][0][0] == 'e'
    assert subtable[1][1][0] == 'f'
    subtable = tbl[1, :]
    assert subtable[0][0] == 'd'
    assert subtable[1][0] == 'e'


def test_Table_allows_empty_values():
    tbl = Table(None)
    assert tbl.num_rows == 0
    assert tbl.num_cols == 0


def test_Table_init_with_1D_values_makes_one_row():
    tbl = Table(['a', 'b', 'c'])
    assert tbl.num_rows == 1
    assert tbl.num_cols == 3
    assert tbl[0, 1][0] == 'b'


def test_Table_init_with_single_value_makes_one_row_one_column():
    tbl = Table('a')
    assert tbl.num_rows == 1
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == 'a'


def test_Table_init_enforces_max_widths_on_columns():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[7, 6, 10])
    assert tbl[0, 0][0] == 'abc def'
    assert tbl[1, 1][0] == 'dog'
    assert tbl[1, 1][1] == 'walker'

    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    assert tbl[0, 0][0] == 'abc'
    assert tbl[0, 0][1] == 'def'
    assert tbl[0, 2][0] == 'cat'
    assert tbl[0, 2][1] == 'food'
    assert tbl[1, 1][0] == 'dog walker'


def test_Table_insert_row_inserts_cells_before_the_given_row():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.insert_row(1, ['x', 'y', 'z'])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 3
    assert tbl[1, 0][0] == 'x'
    tbl.insert_row(0, ['2', '3', '4'])
    assert tbl.num_rows == 4
    assert tbl.num_cols == 3
    assert tbl[0, 1][0] == '3'


def test_Table_insert_row_enforces_max_widths_on_new_cells():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.insert_row(1, ['wx tuv', 'y', 'z'])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 3
    assert tbl[1, 0][0] == 'wx'
    assert tbl[1, 0][1] == 'tuv'


def test_Table_insert_row_raises_if_the_number_of_new_cells_does_not_match():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Expected 3 items, got 4'):
        tbl.insert_row(1, ['w', 'x', 'y', 'z'])


def test_Table_insert_row_can_insert_into_empty_table():
    tbl = Table(None)
    tbl.insert_row(0, ['a', 'b'])
    assert tbl.num_rows == 1
    assert tbl.num_cols == 2
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 1][0] == 'b'


def test_Table_insert_row_can_insert_into_empty_table_with_max_widths():
    tbl = Table(None)
    tbl.insert_row(0, ['a bcde', 'xyz'], max_widths=[4, 3])
    assert tbl.num_rows == 1
    assert tbl.num_cols == 2
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 0][1] == 'bcde'
    assert tbl[0, 1][0] == 'xyz'
    tbl.insert_row(0, ['--', 'gh ijk'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 2
    assert tbl[0, 1][0] == 'gh'
    assert tbl[0, 1][1] == 'ijk'


def test_Table_insert_row_raises_if_max_widths_already_exist():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Max widths already established on table'):
        tbl.insert_row(0, ['x', 'y', 'z'], max_widths=[4, 3, 2])


def test_Table_append_row_inserts_cells_at_the_bottom():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.append_row(['x', 'y', 'z'])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 3
    assert tbl[2, 0][0] == 'x'
    assert tbl[2, 1][0] == 'y'


def test_Table_append_row_enforces_max_widths_on_new_cells():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.append_row(['wx tuv', 'y', 'z'])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 3
    assert tbl[2, 0][0] == 'wx'
    assert tbl[2, 0][1] == 'tuv'


def test_Table_append_row_raises_if_the_number_of_new_cells_does_not_match():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Expected 3 items, got 2'):
        tbl.append_row(['w', 'x'])


def test_Table_append_row_can_append_to_empty_table():
    tbl = Table(None)
    tbl.append_row(['a', 'b'])
    assert tbl.num_rows == 1
    assert tbl.num_cols == 2
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 1][0] == 'b'


def test_Table_append_row_can_append_to_empty_table_with_max_widths():
    tbl = Table(None)
    tbl.append_row(['a bcde', 'xyz'], max_widths=[4, 3])
    assert tbl.num_rows == 1
    assert tbl.num_cols == 2
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 0][1] == 'bcde'
    assert tbl[0, 1][0] == 'xyz'
    tbl.append_row(['--', 'gh ijk'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 2
    assert tbl[1, 1][0] == 'gh'
    assert tbl[1, 1][1] == 'ijk'


def test_Table_append_row_raises_if_max_widths_already_exist():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Max widths already established on table'):
        tbl.append_row(['x', 'y', 'z'], max_widths=[4, 3, 2])


def test_Table_insert_column_inserts_cells_before_the_given_column():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.insert_column(1, ['x', 'y'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 4
    assert tbl[0, 1][0] == 'x'
    assert tbl[1, 1][0] == 'y'
    tbl.insert_column(0, ['2', '3'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 5
    assert tbl[1, 0][0] == '3'


def test_Table_insert_column_enforces_max_widths_on_new_cells():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[4, None, 4])
    tbl.insert_column(1, ['wx tuv', 'y'], max_width=3)
    assert tbl.num_rows == 2
    assert tbl.num_cols == 4
    assert tbl[0, 1][0] == 'wx'
    assert tbl[0, 1][1] == 'tuv'
    assert tbl[1, 1][0] == 'y'

    tbl.insert_row(0, ['a', 'b cd', 'e', 'f'])
    assert tbl[0, 1][0] == 'b'
    assert tbl[0, 1][1] == 'cd'


def test_Table_insert_column_raises_if_the_num_of_new_cells_does_not_match():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Expected 2 items, got 3'):
        tbl.insert_column(1, ['w', 'x', 'y'])


def test_Table_insert_column_can_insert_into_empty_table():
    tbl = Table(None)
    tbl.insert_column(0, ['a', 'b'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == 'a'
    assert tbl[1, 0][0] == 'b'


def test_Table_insert_column_can_insert_into_empty_table_with_max_width():
    tbl = Table(None)
    tbl.insert_column(0, ['a bcde', 'xyz'], max_width=4)
    assert tbl.num_rows == 2
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 0][1] == 'bcde'
    assert tbl[1, 0][0] == 'xyz'

    tbl.insert_row(0, ['--- ='])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == '---'
    assert tbl[0, 0][1] == '='


def test_Table_append_column_appends_cells_at_the_right():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[3, None, 4])
    tbl.append_column(['x', 'y'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 4
    assert tbl[0, 3][0] == 'x'
    assert tbl[1, 3][0] == 'y'
    tbl.append_column(['2', '3'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 5
    assert tbl[1, 4][0] == '3'


def test_Table_append_column_enforces_max_widths_on_new_cells():
    tbl = Table([['abc def', 'bcd', 'cat food'],
                 ['egg', 'dog walker', 'guppy']],
                max_widths=[4, None, 4])
    tbl.append_column(['wx tuv', 'y'], max_width=3)
    assert tbl.num_rows == 2
    assert tbl.num_cols == 4
    assert tbl[0, 3][0] == 'wx'
    assert tbl[0, 3][1] == 'tuv'
    assert tbl[1, 3][0] == 'y'

    tbl.insert_row(0, ['a', 'b cd', 'e', 'f gh'])
    assert tbl[0, 3][0] == 'f'
    assert tbl[0, 3][1] == 'gh'


def test_Table_append_column_raises_if_the_num_of_new_cells_does_not_match():
    tbl = Table([['a', 'b', 'c'],
                 ['d', 'e', 'f']])
    with raises(ValueError, match=r'Expected 2 items, got 3'):
        tbl.append_column(['w', 'x', 'y'])


def test_Table_append_column_can_append_to_empty_table():
    tbl = Table(None)
    tbl.append_column(['a', 'b'])
    assert tbl.num_rows == 2
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == 'a'
    assert tbl[1, 0][0] == 'b'


def test_Table_append_column_can_append_to_empty_table_with_max_width():
    tbl = Table(None)
    tbl.append_column(['a bcde', 'xyz'], max_width=4)
    assert tbl.num_rows == 2
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == 'a'
    assert tbl[0, 0][1] == 'bcde'
    assert tbl[1, 0][0] == 'xyz'

    tbl.insert_row(0, ['--- ='])
    assert tbl.num_rows == 3
    assert tbl.num_cols == 1
    assert tbl[0, 0][0] == '---'
    assert tbl[0, 0][1] == '='


def test_Table_markdown_returns_a_grid_table_string():
    tbl = Table([['abc def', 'bcd', 'xyz'],
                 ['egg', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']],
                max_widths=[4, None, 4])
    mkdn = tbl.markdown('my caption', 'tbl:label')
    lines = mkdn.split('\n')
    assert len(lines) == 14
    assert lines[0] == '+------+------------+-------+'
    assert lines[1] == '| abc  | bcd        | xyz   |'
    assert lines[2] == '|      |            |       |'
    assert lines[3] == '| def  |            |       |'
    assert lines[4] == '+======+============+=======+'
    assert lines[5] == '| egg  | dog walker | guppy |'
    assert lines[6] == '+------+------------+-------+'
    assert lines[7] == '| bird | octopus    | cat   |'
    assert lines[8] == '|      |            |       |'
    assert lines[9] == '|      |            | food  |'
    assert lines[10] == '+------+------------+-------+'
    assert lines[11] == ''
    assert lines[12] == 'Table: my caption {#tbl:label}'
    assert lines[13] == ''


def test_Table_markdown_sets_alignment_on_the_header_row():
    tbl = Table([['abc def', 'bcd', 'xyz'],
                 ['egg', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']],
                max_widths=[4, None, 4])

    header_line = tbl.markdown('my caption', 'tbl:label').split('\n')[4]
    assert header_line == '+======+============+=======+'
    header_line = tbl.markdown('my caption', 'tbl:label', 'lll').split('\n')[4]
    assert header_line == '+:=====+:===========+:======+'
    header_line = tbl.markdown('my caption', 'tbl:label', 'rlc').split('\n')[4]
    assert header_line == '+=====:+:===========+:=====:+'
    header_line = tbl.markdown('my caption', 'tbl:label', 'rdl').split('\n')[4]
    assert header_line == '+=====:+============+:======+'


def test_Table_markdown_returns_a_headerless_grid_table_string():
    tbl = Table([['abc def', 'bcd', 'xyz'],
                 ['egg', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']],
                max_widths=[4, None, 4], headerless=True)
    mkdn = tbl.markdown('my caption', 'tbl:label', 'lcr')
    lines = mkdn.split('\n')
    assert len(lines) == 14
    assert lines[0] == '+:=====+:==========:+======:+'
    assert lines[1] == '| abc  | bcd        | xyz   |'
    assert lines[2] == '|      |            |       |'
    assert lines[3] == '| def  |            |       |'
    assert lines[4] == '+------+------------+-------+'
    assert lines[5] == '| egg  | dog walker | guppy |'
    assert lines[6] == '+------+------------+-------+'
    assert lines[7] == '| bird | octopus    | cat   |'
    assert lines[8] == '|      |            |       |'
    assert lines[9] == '|      |            | food  |'
    assert lines[10] == '+------+------------+-------+'

    tbl = Table([['abc def', 'bcd', 'xyz'],
                 ['egg', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']],
                max_widths=[4, None, 4])
    lines = tbl.markdown('my caption', 'tbl:label', 'lcr').split('\n')
    assert lines[4] == '+:=====+:==========:+======:+'
    tbl.headerless = True
    lines = tbl.markdown('my caption', 'tbl:label', 'lcr').split('\n')
    assert lines[0] == '+:=====+:==========:+======:+'
    tbl.headerless = False
    lines = tbl.markdown('my caption', 'tbl:label', 'lcr').split('\n')
    assert lines[4] == '+:=====+:==========:+======:+'


def test_Table_markdown_adds_footnote_definitions_to_markdown():
    tbl = Table([['abc def', 'bcd [^bcdNote]', 'xyz'],
                 ['egg [^eggNote]', 'dog walker', 'guppy'],
                 ['bird', 'octopus', 'cat food']])
    notes = {
        'bcdNote': 'a note about bcd',
        'eggNote': 'a note about eggs',
    }
    mkdn = tbl.markdown('my caption', 'tbl:label', footnotes=notes)
    lines = mkdn.split('\n')
    # assert len(lines) == 13
    assert lines[0] == '+----------------+----------------+----------+'
    assert lines[1] == '| abc def        | bcd [^bcdNote] | xyz      |'
    assert lines[2] == '+================+================+==========+'
    assert lines[3] == '| egg [^eggNote] | dog walker     | guppy    |'
    assert lines[4] == '+----------------+----------------+----------+'
    assert lines[5] == '| bird           | octopus        | cat food |'
    assert lines[6] == '+----------------+----------------+----------+'
    assert lines[7] == ''
    assert lines[8] == 'Table: my caption {#tbl:label}'
    assert lines[9] == ''
    assert lines[10] == '[^bcdNote]: a note about bcd'
    assert lines[11] == '[^eggNote]: a note about eggs'
    assert lines[12] == ''
