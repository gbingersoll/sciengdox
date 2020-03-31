from sciengdox.units import pq, Q_, ureg


def test_pq_outputs_markdown(capsys):
    pq(Q_(10, 'm/s^2'))
    assert capsys.readouterr().out == '10.000 m/s^2^\n'


def test_pq_outputs_with_default_precision(capsys):
    pq(Q_(9.12345678, 'm/s^2'))
    assert capsys.readouterr().out == '9.123 m/s^2^\n'


def test_pq_outputs_with_provided_precision(capsys):
    pq(Q_(9.12345678, 'm/s^2'), precision=0)
    assert capsys.readouterr().out == '9 m/s^2^\n'
    pq(Q_(9.12345678, 'm/s^2'), precision=5)
    assert capsys.readouterr().out == '9.12346 m/s^2^\n'


def test_pq_outputs_scientific_notation(capsys):
    pq(Q_(1234000000.12345678, 'm/s^2'), scientific=True)
    assert capsys.readouterr().out == '1.23e+09 m/s^2^\n'
