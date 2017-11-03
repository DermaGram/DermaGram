from flask import Flask, render_template, request
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os

app = Flask(__name__)
photos = UploadSet('photos', IMAGES)

class Upload:
    def upload_file(self):
        if request.method == 'POST' and 'photo' in request.files:
            filename = photos.save(request.files['photo'])
            return filename
        return render_template('upload.html')
