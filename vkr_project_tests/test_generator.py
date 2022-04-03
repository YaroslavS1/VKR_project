# -*- coding: utf-8 -*-
 # @ Время: 17.08.2008 10:10
# @Author  : WangJuan
# @File    : test_case.py
import allure
import pytest


@allure.step ("Добавление строки: {0}, {1}") # Шаг теста, параметры функции могут быть автоматически получены с помощью механизма форматирования
def str_add(str1, str2):
    print('hello')
    if not isinstance(str1, str):
        return "%s is not a string" % str1
    if not isinstance(str2, str):
        return "%s is not a string" % str2
    return str1 + str2

@allure.feature('test_module_01')
@allure.story('test_story_01')
@allure.severity('blocker')
@allure.issue("http://www.baidu.com")
@allure.testcase("http://www.testlink.com")
def test_case():
    str1 = 'hello'
    str2 = 'world'
    assert str_add(str1, str2) == 'helloworld'


if __name__ == '__main__':
    pytest.main(['-s', '-q', '--alluredir', './report/xml'])
