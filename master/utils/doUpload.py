from flask import request, session
from flask_uploads import UploadSet, IMAGES, configure_uploads
from imgur_utils import ImgurUtils
import os


class Upload:

    def __init__(self):
        self._destination_key_name = 'UPLOADED_PHOTOS_DEST'
        self._destination_file_path = 'static/img'
        self._set_name = 'photos'
        self._upload_photo_set = self._create_upload_photo_set( self._set_name )

    #TODO may need to rethink this depending on how we initialize other app stuff (like imgur client)
    def initialize_app_upload(self, app):
        app.config[self._destination_key_name] = self._destination_file_path
        configure_uploads(app, self._upload_photo_set)

    def upload_image(self, album_id, image):
        if not image:
            return False

        try:
            # Temp save  image to _destribution_file_path
            self._upload_photo_set.save(image)
            # Prepend _distribution_file_path to image name
            image_path = "{0}/{1}".format( self._destination_file_path, image.filename )
            # Upload image to imgur
            imgur = ImgurUtils()
            imgur.add_image_to_album(session['album_id'], image_path)
            # Delete image from _distribution_file_path
            os.remove(image_path)
        except Exception as e:
            print "Error: ",e
            return False

        return True

    @staticmethod
    def _create_upload_photo_set(set_name):
        return UploadSet(set_name, IMAGES)

