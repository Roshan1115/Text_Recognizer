from application import app, dropzone
from flask import render_template, request, redirect, url_for, session
from .forms import QRCodeData
import secrets
import os

# OCR
import cv2
import pytesseract
from PIL import Image
import numpy as np
# pip install gTTS
from gtts import gTTS

# import utils
from . import utils


@app.route("/")
def index():
    return render_template("index.html")

# file_location = ""
# print("Bahar")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    print("tests")
    if request.method == 'POST':

        print("posttttttt")

        # set a session value
        sentence = ""

        f = request.files.get('file')
        print(f.filename)
        filename, extension = f.filename.split(".")
        generated_filename = secrets.token_hex(10) + f".{extension}"

        print(generated_filename)

        file_location = os.path.join(app.config['UPLOADED_PATH'], generated_filename)

        print(file_location)
        f.save(file_location)


        # OCR here
        # pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

        tessdata_config = r'--oem 1 --psm 7 tessdata_best'


        img = cv2.imread(file_location)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 7)


        boxes = pytesseract.image_to_string(img)
        print(boxes)
    
        # for i, box in enumerate(boxes.splitlines()):
        #     if i == 0:
        #         continue

        #     box = box.split()
        #     # print(box)

        #     # only deal with boxes with word in it.
        #     if len(box) == 12:
        #         sentence += box[11] + " "
       
        # print(sentence)
        session["sentence"] = boxes

        # delete file after you are done working with it
        os.remove(file_location)    

        return redirect("/decoded/")

    else:
        # print("test2")
        return render_template("upload.html", title="Home")


# print(file_location)



@app.route("/decoded", methods=["GET", "POST"])
def decoded():

    sentence = session.get("sentence")
    print(sentence)

    # print(lang)
    lang, _ = utils.detect_language(sentence)
    # print(lang, conf)
    

    form =QRCodeData() 

    if request.method == "POST":
        generated_audio_filename = secrets.token_hex(10) + ".mp4"
        text_data = form.data_field.data
        translate_to = form.language.data
        # print("Data here", translate_to)

  
        translated_text = utils.translate_text(text_data, translate_to)
        print(translated_text)
        tts = gTTS(translated_text, lang=translate_to)



        file_location = os.path.join(
                            app.config['AUDIO_FILE_UPLOAD'], 
                            generated_audio_filename
                        )

        # save file as audio
        tts.save(file_location)

        # return redirect("/audio_download/" + generated_audio_filename)

        form.data_field.data = translated_text

        return render_template("decoded.html", 
                        title="Decoded", 
                        form=form, 
                        lang=utils.languages.get(lang),
                        audio = True,
                        file = generated_audio_filename
                    )


    # form.data_field.data = sentence
    form.data_field.data = sentence

    # set the sentence back to defautl blank
    # sentence = ""
    session["sentence"] = ""

    return render_template("decoded.html", 
                            title="Decoded", 
                            form=form, 
                            lang=utils.languages.get(lang),
                            audio = False
                        )



