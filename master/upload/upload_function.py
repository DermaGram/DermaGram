from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from utils.imgur_utils import ImgurUtils
from imgurpython import ImgurClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

class SClass:
    def upload_file(self):
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename
        return render_template('upload.html')
