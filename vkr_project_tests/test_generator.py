import pytest

from vkr_project.generator import sample, generate_buzz



@pytest.mark.parametrize("value", ['foo', 'bar', 'foobar'])
def test_sample_single_word(value):
    word = sample(value)
    assert word in value


@pytest.mark.parametrize("value", ['foo', 'bar', 'foobar'])
def test_sample_multiple_words(value):
    words = sample(value, 2)
    assert len(words) == 2
    assert words[0] in value
    assert words[1] in value
    # assert words[0] is not words[1]

@pytest.mark.parametrize("value", ['foo', 'bar', 'foobar', 423,42,34,23,4,23,4234,23,4,23,4,23,42,4534,523,412,34,123,412,34,123,41234])
def test_generate_buzz_of_at_least_five_words(value):
    phrase = generate_buzz()
    assert len(phrase.split()) >= 5