from flask_uploads import UploadSet, IMAGES, configure_uploads
import os


class FileUtils:

    def __init__(self):
        self.destination_file_path = '/home/dermagram/static/img'

    def get_upload_set(self):
        return UploadSet('photos', IMAGES)

    def initialize_app_image_storage(self,app, photo_set):
        app.config['UPLOADED_PHOTOS_DEST'] = self.destination_file_path
        configure_uploads(app, photo_set)

    def get_image_file_path(self):
        filename = os.listdir(self.destination_file_path)
        image_file_path = os.path.join(self.destination_file_path, filename[0])
        return image_file_path

    def refresh_temp_folder(self):
        if not os.path.isdir(self.destination_file_path):
            print "NO DIR: ", self.destination_file_path
            os.mkdir(self.destination_file_path)
        else:
            self.rm_files_temp_folder()

    def rm_files_temp_folder(self):
        for file in os.listdir(self.destination_file_path):
            print "rm file: ", file
            try:
                os.remove(os.path.join(self.destination_file_path, file))
            except Exception as e:
                print "Error: ", e
