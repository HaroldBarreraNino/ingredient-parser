import pytest

from ingredient_parser import PreProcessor


@pytest.fixture
def p():
    """Define an empty PreProcessor object to use for testing the PreProcessor
    class methods.
    """
    return PreProcessor("", defer_pos_tagging=True)


class TestPreProcessor_replace_string_numbers:
    def test_spaces(self, p):
        """
        The string number, surrounded by spaces, is converted to a numeral
        """
        input_sentence = "Zest of one orange"
        assert p._replace_string_numbers(input_sentence) == "Zest of 1 orange"

    def test_start(self, p):
        """
        The string number, at the start of the sentence and followed by a space,
        is converted to a numeral
        """
        input_sentence = "Half of a lime"
        assert p._replace_string_numbers(input_sentence) == "Half of a lime"

    def test_parens(self, p):
        """
        The string number, at the beginning of a phrase inside parentheses,
        s converted to a numeral
        """
        input_sentence = "2 cups (three 12-ounce bags) frozen raspberries"
        assert (
            p._replace_string_numbers(input_sentence)
            == "2 cups (3 12-ounce bags) frozen raspberries"
        )

    def test_hyphen(self, p):
        """
        The string number, with a hyphen appended without a space,
        is converted to a numeral
        """
        input_sentence = "1 pound potatoes, peeled and cut into five-inch cubes"
        assert (
            p._replace_string_numbers(input_sentence)
            == "1 pound potatoes, peeled and cut into 5-inch cubes"
        )

    def test_substring(self, p):
        """
        The string number, appearing as a substring of another word,
        is not converted to a numeral
        """
        input_sentence = (
            "1 pound skinless, boneless monkfish fillets"  # "one" inside "boneless"
        )
        assert (
            p._replace_string_numbers(input_sentence)
            == "1 pound skinless, boneless monkfish fillets"
        )
