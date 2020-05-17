from model.Classes import clean_fragments


def test_clean_fragment():
    test_string = """31.3.2020";"S MARKET KUOPIO";"KORTTIOSTO";"'KUOPIO FIN";"-26,21"""
    test_fragments = test_string.split(";")

    expected = ["31.3.2020", "S MARKET KUOPIO", "KORTTIOSTO", "KUOPIO FIN", "-26.21"]
    actual = clean_fragments(test_fragments)

    assert actual == expected
