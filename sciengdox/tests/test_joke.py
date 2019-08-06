import sciengdox


def test_joke_is_string():
    s = sciengdox.joke()
    assert isinstance(s, str)
