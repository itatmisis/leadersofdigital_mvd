import json
import os

from flask import Flask, render_template, request, send_file, make_response
from flaskwebgui import FlaskUI

from utils import open_image, read_image, write_docx, read_docx, open_docx, save_docx, convert_text, open_odt, write_odt

app = Flask(__name__)
ui = FlaskUI(app, width=1324, height=728)


@app.route("/")
def index():
    return render_template("main.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    mimetype = f.content_type
    print(mimetype)
    if mimetype == "image/jpeg0" or mimetype == "image/png":
        image = open_image(f)
        extracted_text = read_image(image)
        document = write_docx(extracted_text)
        print("okay")
        return send_file(document, as_attachment=True, attachment_filename="report.docx")
    elif mimetype == "audio/mpeg" or mimetype == "audio/wav":
        f.filename = "sound.wav"
        f.save(f.filename)
        stream = os.popen('python3 test_ffmpeg.py ' + f.filename)
        output = stream.read()
        print(output)
        text = ''
        with open('res.json') as json_file:
            data = json.load(json_file)
            text = data['text']
            print(data['text'])
        extracted_text = text
        processed_text = convert_text(extracted_text)
        print(extracted_text + ';' + processed_text)
        response = make_response(extracted_text + ';' + processed_text, 200)
        response.mimetype = "text/plain"
        return response

    elif mimetype == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document = open_docx(f)
        extracted_text = read_docx(document)
        processed_text = convert_text(extracted_text)
        new_document = write_docx(processed_text)
        stream = save_docx(new_document)
        print("okay")
        return send_file(stream, as_attachment=True, attachment_filename="report1to3.docx")
    elif mimetype == "application/vnd.oasis.opendocument.text":
        extracted_text = open_odt(f)
        processed_text = convert_text(extracted_text)
        stream = write_odt(processed_text)
        print("okay")
        return send_file(stream, as_attachment=True, attachment_filename="report1to3.odt")


@app.route('/submit', methods=['POST'])
def submit():
    extracted_text = request.form["text"]
    processed_text = convert_text(extracted_text)
    response = make_response(processed_text, 200)
    response.mimetype = "text/plain"
    return response


if __name__ == "__main__":
    ui.run()
