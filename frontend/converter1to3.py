from collections import Counter

import pymorphy2

from words import *


def get_gender_by_word(word):
    """Возвращает пол человека"""

    morph = pymorphy2.MorphAnalyzer(path="pymorphy2_dicts_ru/data", lang="ru")
    parsed_word = morph.parse(word)[0]

    return parsed_word.tag.gender


def is_verb(word):
    morph = pymorphy2.MorphAnalyzer(path="pymorphy2_dicts_ru/data", lang="ru")

    word = morph.parse(word)[0]
    pos = word.tag.POS
    return pos in {'INFN', 'VERB'}


def get_gender(text):
    text = correct(text)
    for i in punctuation[1:]:
        text = text.replace('{} '.format(i), ' {} '.format(i))

    cases = []
    words = text.split()
    for i in range(len(text.split())):
        if words[i].lower() == 'я':
            if is_verb(words[i + 1]):
                cases.append(words[i + 1])
            if is_verb(words[i + 2]):
                cases.append(words[i + 2])

    genders = [get_gender_by_word(case) for case in cases]
    res = [i for i in genders if i]
    if len(res):
        return Counter(res).most_common(1)[0][0]
    else:
        return None


def correct(text, add_before_text=None, add_after_text=None):
    """Корректирует входной текст"""

    for i in punctuation[1:]:
        text = text.replace(' {}'.format(i), i)

    for i in punctuation[1:]:
        text = text.replace(i, '{} '.format(i))

    for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        text = text.replace('. {}'.format(i), '.{}'.format(i))

    if add_before_text is not None:
        text = text[0].lower() + text[1:]
        text = add_before_text + text

    if add_after_text is not None:
        text = text + ' ' + add_after_text

    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


def convert(ch, text):
    """метод отыскивающий словосочетания с символом ch, в тексте и меняющий на 3 лицо"""

    for word in sys_list_words:
        text = text.replace(' {}{}'.format(word[0], ch), ' {}{}'.format(word[1], ch))
        text = text.replace('{}{}'.format(word[0].capitalize(), ch), '{}{}'.format(word[1].capitalize(), ch))

    return text


def verbs_to3(text):
    """Склоняет глаголы в 3 лицо"""
    morph = pymorphy2.MorphAnalyzer(path="pymorphy2_dicts_ru/data", lang="ru")

    for i in punctuation[1:]:
        text = text.replace('{} '.format(i), ' {} '.format(i))

    for word in text.split():
        word = morph.parse(word)[0]
        pos = word.tag.POS
        if pos in {'INFN', 'VERB'}:
            if word.tag.tense == 'pres':
                new_word = word.inflect({word.tag.number, '3per'}).word
                text = text.replace('{}'.format(word.word), '{}'.format(new_word))

    text = correct(text)

    return text


def conv_with_gender(text, gender):
    change_words_p = change_words_women_p if gender == 'femn' else change_words_men_p
    change_words = change_words_women if gender == 'femn' else change_words_men

    for ch in punctuation:
        text = convert(ch, text)
        text = verbs_to3(text)
        for pre in pretext:
            for key in change_words_p:
                text = text.replace(key.format(pre, ch), change_words_p[key].format(pre, ch))

        for dic in change_words:
            for key in dic:
                text = text.replace(key.format(ch), dic[key].format(ch))

    return text


def conv1to3(text, gender=None):
    """Конвертирует текст в повествование от 3 лица с учетом пола человека
         gender - male/female
    """

    text = correct(text)
    if not gender:
        gender = get_gender(text)
        if not gender:
            return text
    return conv_with_gender(text, gender)
