from io import BytesIO

import odf
import pymorphy2
import pytesseract
from PIL import Image
from docx import Document
from odf.opendocument import load, OpenDocumentText
from odf.text import P
from odf import teletype

from converter1to3 import conv1to3


def open_image(file) -> Image:
    image = Image.open(file)
    return image


def read_image(image: Image) -> str:
    text = pytesseract.image_to_string(image, lang='rus')
    return text


def open_docx(file) -> Document:
    document = Document(file)
    return document


def read_docx(document: Document) -> str:
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return "\n".join(text)


def write_docx(text: str) -> Document:
    document: Document = Document()
    document.add_paragraph(text)
    return document


def save_docx_target(document: Document, target):
    document.save(target)


def save_docx(document: Document) -> BytesIO:
    target_stream = BytesIO()
    document.save(target_stream)
    target_stream.seek(0)
    return target_stream


def open_odt(file) -> str:
    textdoc = load(file)
    allparas = textdoc.getElementsByType(odf.text.P)
    text = "\n".join([teletype.extractText(par) for par in allparas])
    return text


def write_odt(text: str) -> BytesIO:
    textdoc = OpenDocumentText()
    paragraph_element = P()
    teletype.addTextToElement(paragraph_element, text)
    textdoc.text.addElement(paragraph_element, text)
    target_stream = BytesIO()
    textdoc.write(target_stream)
    return target_stream


def convert_text(gender: str, text: str) -> str:
    converted_text = conv1to3(gender, text)
    return converted_text


def get_gender_by_name(name):
    morph = pymorphy2.MorphAnalyzer()
    parsed_word = morph.parse(name)[0]
    return parsed_word.tag.gender
