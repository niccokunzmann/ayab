
def test_import():
    import ayab
    print(ayab.__file__)
    assert ayab.__version__
