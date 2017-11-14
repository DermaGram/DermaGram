from flask import session
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

    def upload_image(self, image, location, classification):
        image_link = ""
        if not image:
            return image_link

        try:
            self._refresh_temp_folder()
            photo_set = UploadSet(self._set_name, IMAGES)
            photo_set.save(image)
            filename = os.listdir(self._destination_file_path)
            print "FILENAME: ",filename
            image_path = os.path.join( self._destination_file_path, filename[0] )
            # Upload image to imgur
            imgur = ImgurUtils()
            #TODO make 'location' a selection from a drop down list, not free form text
            img = imgur.add_image_to_album(session['album_id'], image.filename, location, classification, image_path)
            image_link = img['link']
            print "IMG: ",image_link
            # Delete image from _distribution_file_path
            self._rm_files_temp_folder()
        except Exception as e:
            print "Error: ",e
            return image_link

        return image_link

    @staticmethod
    def _create_upload_photo_set(set_name):
        return UploadSet(set_name, IMAGES)

    def _refresh_temp_folder(self):
        if not os.path.isdir(self._destination_file_path):
            print "NO DIR: ",self._destination_file_path
            os.mkdir(self._destination_file_path)
        else:
            self._rm_files_temp_folder()

    def _rm_files_temp_folder(self):
        for file in os.listdir(self._destination_file_path):
            print "rm file: ", file
            try:
                os.remove(os.path.join(self._destination_file_path,file))
            except Exception as e:
                print "Error: ", e

