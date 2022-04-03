import allure
import pytest

from vkr_project.generator import sample, generate_buzz


@allure.feature('Random dog')
@pytest.mark.parametrize("value", ['foo', 'bar', 'foobar'])
def test_sample_single_word(value):
    word = sample(value)
    assert word in value


def test_sample_multiple_words():
    l = ('foo', 'bar', 'foobar')
    words = sample(l, 2)
    assert len(words) == 2
    assert words[0] in l
    assert words[1] in l
    assert words[0] is not words[1]


def test_generate_buzz_of_at_least_five_words():
    phrase = generate_buzz()
    assert len(phrase.split()) >= 5