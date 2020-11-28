import pymorphy2
from collections import Counter

pretext = [
    ' в ', 'В ', ' без ', 'Без ', ' до ', 'До ', ' из ', 'Из ', ' к ', 'К ',
    ' на ', 'На ', ' по ', 'По ', ' от ', 'От ', ' перед ', 'Перед ', ' при ', 'При ',
    ' через ', 'Через ', ' с ', 'С ', ' у ', 'У ', ' за ', 'За ', ' над ', 'Над ',
    ' об ', 'Об ', ' под ', 'Под ', ' про ', 'Про ', ' для ', 'Для ', ' ради ', 'Ради ',
    ' сквозь ', 'Сквозь ', ' между ', 'Между ', ' из-под ', 'Из-под ', ' из-за ', 'Из-за ',
    ' по-над ', 'По-над ', ' по-за ', 'По-за ', ' вблизи ', 'Вблизи ', ' вглубь ', 'Вглубь ',
    ' вдоль ', 'Вдоль ', ' возле ', 'Возле ', ' около ', 'Около ', ' вокруг ', 'Вокруг ',
    ' впереди ', 'Впереди ', ' после ', 'После ', ' в течение ', 'В течение ',
    ' в продолжение ', 'В продолжение ', ' в отличи от ', 'В отличи от ',
    ' в заключение ', 'В заключение ', ' в связи с ', 'В связи с ',
    ' в целях ', 'В целях ', ' за счет ', 'За счет ', ' в виде ', 'В виде ',
    ' по причине ', 'По причине ', ' наподобие ', 'Наподобие ', ' вроде ', 'Вроде ',
    ' подобно ', 'Подобно ', ' как ', 'Как ', ' вследствие ', 'Вследствие ',
    ' вслед ', 'Вслед ', ' внутри ', 'Внутри ', ' навстречу ', 'Навстречу ',
    ' посредством ', 'Посредством ', ' в роли ', 'В роли ',
    ' в зависимости от ', 'В зависимости от ', ' путем ', 'Путем ',
    ' насчет ', 'Насчет ', ' по поводу ', 'По поводу ', ' ввиду ', 'Ввиду ',
    ' по случаю ', 'По случаю ', ' вслед за ', 'Вслед за ', ' хотя ', 'Хотя ',
    ' благодаря ', 'Благодаря ', ' несмотря на ', 'Несмотря на ', ' спустя ', 'Спустя ']
punctuation = [
    ' ', '.', ',', ':', ';', '!', '?', '(', ')', '-']
change_words_men_p = {'{}меня{}': '{}него{}',
                      '{}мною{}': '{}ним{}'}
change_words_men = [
    {' обо мне{}': ' о нём{}', 'Обо мне{}': 'О нём{}', ' со мною{}': ' с ним{}',
     'Со мною{}': 'С ним{}', 'Со мной{}': 'С ним{}', ' ко мне{}': ' к нему{}',
     'Ко мне{}': 'К нему{}', ' при мне{}': ' при нём{}',
     'При мне{}': 'При нём{}', ' на мне{}': ' на нём{}',
     'На мне{}': 'На нём{}', ' в моем{}': ' в его{}',
     'В моем{}': 'В его{}', ' в моём{}': ' в его{}',
     'В моём{}': 'В его{}', ' с моих{}': ' с его{}',
     'С моих{}': 'С его{}', ' со мной{}': ' с ним{}',
     ' у меня{}': ' у него{}',
     'У меня{}': 'У него{}'},
    {' я{}': ' он{}', 'Я{}': 'Он{}', ' меня{}': ' его{}',
     'Меня{}': 'Его{}', ' мной{}': ' им{}',
     'Мной{}': 'Им{}', ' мне{}': ' ему{}',
     'Мне{}': 'Ему{}', ' мои{}': ' его{}',
     'Мои{}': 'Его{}', ' моих{}': ' его{}',
     'Моих{}': 'Его{}', ' моё{}': ' его{}',
     'Моё{}': 'Его{}', ' мое{}': ' его{}',
     'Мое{}': 'Его{}', ' мой{}': ' его{}',
     'Мой{}': 'Его{}', ' моя{}': ' его{}',
     'Моя{}': 'Его{}', ' моим{}': ' его{}',
     'Моим{}': 'Его{}', ' моей{}': ' его{}',
     'Моей{}': 'Его{}', ' моего{}': ' его{}',
     'Моего{}': 'Его{}'}]
change_words_women_p = {'{}меня{}': '{}неё{}',
                        '{}мною{}': '{}ней{}',
                        '{}мной{}': '{}ней{}'}
change_words_women = [
    {' обо мне{}': ' о ней{}', 'Обо мне{}': 'О ней{}', ' со мною{}': ' с ней{}',
     'Со мною{}': 'С ней{}', ' со мной{}': ' с ней{}',
     'Со мной{}': 'С ней{}', ' ко мне{}': ' к ней{}',
     'Ко мне{}': 'К ней{}', ' при мне{}': ' при ней{}',
     'При мне{}': 'При ней{}', ' на мне{}': ' на ней{}',
     'На мне{}': 'На ней{}', ' в моем{}': ' в ее{}',
     'В моем{}': 'В ее{}', ' в моём{}': ' в ее{}',
     'В моём{}': 'В ее{}', ' с моих{}': ' с ее{}',
     'С моих{}': 'С ее{}', ' у меня{}': ' у нее{}',
     'У меня{}': 'У нее{}'},
    {' я{}': ' она{}', 'Я{}': 'Она{}', ' меня{}': ' её{}',
     'Меня{}': 'Её{}', ' мне{}': ' ей{}',
     'Мне{}': 'Ей{}', ' мои{}': ' её{}',
     'Мои{}': 'Её{}', ' моё{}': ' ее{}',
     'Моё{}': 'Ее{}', ' мое{}': ' ее{}',
     'Мое{}': 'Ее{}', ' моих{}': ' её{}',
     'Моих{}': 'Её{}', ' мой{}': ' её{}',
     'Мой{}': 'Её{}', ' моя{}': ' её{}',
     'Моя{}': 'Её{}', ' моим{}': ' её{}',
     'Моим{}': 'Её{}', ' моей{}': ' её{}',
     'Моей{}': 'Её{}', ' мной{}': ' ей{}',
     'Мной{}': 'Ей{}', ' моего{}': ' её{}',
     'Моего{}': 'Её{}'}]
sys_list_words = [['о нём', 'о том'],
                  ['о ней', 'о той'],
                  ['о нас', 'о них'],
                  ['о них', 'о тех'],
                  ['у нас', 'у них'],
                  ['в нашем', 'в их'],
                  ['он', 'тот'],
                  ['она', 'та'],
                  ['оно', 'то'],
                  ['они', 'те'],
                  ['его', 'того'],
                  ['её', 'той'],
                  ['ее', 'той'],
                  ['ему', 'тому'],
                  ['ей', 'той'],
                  ['ею', 'тою'],
                  ['их', 'тех'],
                  ['него', 'того'],
                  ['неё', 'той'],
                  ['нее', 'той'],
                  ['них', 'тех'],
                  ['нему', 'тому'],
                  ['ней', 'той'],
                  ['нею', 'тою'],
                  ['ним', 'тем'],
                  ['ними', 'теми'],
                  ['ими', 'теми'],
                  ['нами', 'ими'],
                  ['мы', 'они'],
                  ['нас', 'их'],
                  ['им', 'тем'],
                  ['к нам', 'к ним'],
                  ['нам', 'им'],
                  ['нашей', 'их'],
                  ['наше', 'их'],
                  ['наш', 'их'],
                  ['нашего', 'их'],
                  ['наши', 'их'],
                  ['наших', 'их'],
                  ['нашем', 'их'],
                  ['аккомпаниирую', 'аккомпаниирует'],
                  ['буду', 'будет'],
                  ['будим', 'будят'],
                  ['ведем', 'ведут'],
                  ['веду', 'ведет'],
                  ['возьму', 'возьмет'],
                  ['вставляю', 'вставляет'],
                  ['выполняю', 'выполняет'],
                  ['выезжаю', 'выезжает'],
                  ['вернусь', 'вернется'],
                  ['вижу', 'видит'],
                  ['владею', 'владеет'],
                  ['видимся', 'видятся'],
                  ['встретимся', 'встретятся'],
                  ['говорю', 'говорит'],
                  ['делаю', 'делает'],
                  ['думаю', 'думает'],
                  ['еду', 'едет'],
                  ['живу', 'живёт'],
                  ['знаю', 'знает'],
                  ['занимаю', 'занимает'],
                  ['замещаю', 'замещает'],
                  ['занимаюсь', 'занимается'],
                  ['завожу', 'заводит'],
                  ['забираю', 'забирает'],
                  ['заверяю', 'заверяет'],
                  ['издаю', 'издает'],
                  ['исполняю', 'исполняет'],
                  ['ищу', 'ищет'],
                  ['имею', 'имеет'],
                  ['идем', 'идут'],
                  ['идём', 'идут'],
                  ['иду', 'идёт'],
                  ['контролирую', 'контролирует'],
                  ['курирую', 'курирует'],
                  ['куплю', 'купит'],
                  ['могу', 'может'],
                  ['нахожусь', 'находится'],
                  ['направляю', 'направляет'],
                  ['нуждаюсь', 'нуждается'],
                  ['общаемся', 'общаются'],
                  ['определяем', 'определяют'],
                  ['осматриваю', 'осматривает'],
                  ['оцениваю', 'оценивает'],
                  ['оборудую', 'оборудует'],
                  ['отрабатываю', 'отрабатывает'],
                  ['отношусь', 'относится'],
                  ['оформляю', 'оформляет'],
                  ['оставляю', 'оставляет'],
                  ['обмениваю', 'обменивает'],
                  ['помню', 'помнит'],
                  ['признаю', 'признает'],
                  ['поддерживаю', 'поддерживает'],
                  ['поддерживаем', 'поддерживают'],
                  ['проживаю', 'проживает'],
                  ['поеду', 'поедет'],
                  ['позвоню', 'позвонит'],
                  ['поясняю', 'поясняет'],
                  ['печатаю', 'печатает'],
                  ['принимаю', 'принимает'],
                  ['посещаю', 'посещает'],
                  ['поговорю', 'поговорит'],
                  ['передаю', 'передает'],
                  ['подвожу', 'подводит'],
                  ['подписываю', 'подписывает'],
                  ['получаю', 'получает'],
                  ['прихожу', 'приходит'],
                  ['предполагаю', 'предполагает'],
                  ['провожу', 'проводит'],
                  ['произвожу', 'производит'],
                  ['продумываю', 'продумывает'],
                  ['переводимся', 'переводятся'],
                  ['приступлю', 'приступит'],
                  ['пишу', 'пишет'],
                  ['прошу', 'просит'],
                  ['представляю', 'представляет'],
                  ['поздороваемся', 'поздороваются'],
                  ['понимаю', 'понимает'],
                  ['пойдем', 'пойдут'],
                  ['полагаю', 'полагает'],
                  ['покупаю', 'покупает'],
                  ['перевожу', 'переводит'],
                  ['проживаем', 'проживают'],
                  ['прохожу', 'проходит'],
                  ['работаю', 'работает'],
                  ['регистрирую', 'регистрирует'],
                  ['руководствуемся', 'руководствуются'],
                  ['руковожу', 'руководит'],
                  ['разговариваю', 'разговаривает'],
                  ['раскаиваюсь', 'раскаивается'],
                  ['смогу', 'сможет'],
                  ['состою', 'состоит'],
                  ['составляю', 'составляет'],
                  ['сдаю', 'сдаёт'],
                  ['сообщу', 'сообщит'],
                  ['совмещаю', 'совмещает'],
                  ['собираю', 'собирает'],
                  ['сплю', 'спит'],
                  ['созваниваемся', 'созваниваются'],
                  ['сможем', 'смогут'],
                  ['свяжусь', 'свяжется'],
                  ['ставлю', 'ставит'],
                  ['трачу', 'тратит'],
                  ['устроюсь', 'устроется'],
                  ['указываю', 'указывает'],
                  ['участвую', 'участвует'],
                  ['употребляю', 'употребляет'],
                  ['формирую', 'формирует'],
                  ['хочу', 'хочет'],
                  ['храню', 'хранит'],
                  ['храним', 'хранят'],
                  ['являюсь', 'является'],
                  ['являемся', 'являются']]


def is_verb(word):
    """Определяет, является ли слово глаголом"""
    morph = pymorphy2.MorphAnalyzer()

    word = morph.parse(word)[0]
    pos = word.tag.POS
    return pos in {'INFN', 'VERB'}


def get_gender_by_word(word):
    """Возвращает пол человека по глаголу"""

    morph = pymorphy2.MorphAnalyzer()
    parsed_word = morph.parse(word)[0]

    return parsed_word.tag.gender


def get_gender(text):
    """Возвращает пол человека по тексту"""
    text = correct(text)
    for i in punctuation[1:]:
        text = text.replace('{} '.format(i), ' {} '.format(i))

    cases = []
    words = text.split()
    for i in range(len(text.split())):
        if words[i].lower() == 'я':
            if is_verb(words[i+1]):
                cases.append(words[i+1])
            if is_verb(words[i+2]):
                cases.append(words[i+2])

    genders = [get_gender(case) for case in cases]
    res = [i for i in genders if i]

    return Counter(res).most_common(1)[0][0]


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
    """Склоняет глагол в 3 лицо"""

    for i in punctuation[1:]:
        text = text.replace('{} '.format(i), ' {} '.format(i))

    for word in text.split():
        morph = pymorphy2.MorphAnalyzer()
        word = morph.parse(word)[0]
        pos = word.tag.POS
        if pos in {'INFN', 'VERB'}:
            if word.tag.tense == 'pres':
                new_word = word.inflect({word.tag.number, '3per'}).word
                text = text.replace('{}'.format(word.word), '{}'.format(new_word))

    text = correct(text)

    return text


def _to_men(text):
    for ch in punctuation:
        text = convert(ch, text)
        text = verbs_to3(text)
        for predlog in pretext:
            for key in change_words_men_p:
                text = text.replace(key.format(predlog, ch), change_words_men_p[key].format(predlog, ch))

        for dic in change_words_men:
            for key in dic:
                text = text.replace(key.format(ch), dic[key].format(ch))

    return text


def _to_women(text):
    for ch in punctuation:
        text = convert(ch, text)
        text = verbs_to3(text)
        for predlog in pretext:
            for key in change_words_women_p:
                text = text.replace(key.format(predlog, ch), change_words_women_p[key].format(predlog, ch))

        for dic in change_words_women:
            for key in dic:
                text = text.replace(key.format(ch), dic[key].format(ch))

    return text


def conv1to3(text, gender):
    """Конвертирует текст в повествование от 3 лица с учетом пола человека"""

    text = correct(text)
    if gender == 'male':
        return _to_men(text)
    elif gender == 'female':
        return _to_women(text)