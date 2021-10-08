from madonna.madonna import hello


def test_silly_placeholder():
    """
    Test for silly placeholder in
    madonna.py
    """

    want = "Hello madonna"
    got = hello()

    assert got == want
