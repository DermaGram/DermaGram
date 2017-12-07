from flask import session
from imgur_utils import ImgurUtils


class Upload(object):

    @classmethod
    def upload_image(cls, image_name, image, location, classification):
        image_link = ""
        if not image:
            return image_link

        try:
            imgur = ImgurUtils()
            img = imgur.add_image_to_album(session['album_id'], image_name, location, classification, image)
            image_link = img['link']
        except Exception as e:
            print "Error: ",e
            return image_link

        return image_link
