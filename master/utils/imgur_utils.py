from imgurpython import ImgurClient
from utils.logging_utils import LoggingUtils
import time
import json
import logging

LoggingUtils.initialize_logger(__name__)

class ImgurUtils:
    _ACCOUNT_NAME  = "DermaGram"
    _CLIENT_ID     = "74ab756d286b81b"
    _CLIENT_SECRET = "06e8cbd50c3388b95681efe0bf17e8578f72c8dd"
    _ACCESS_TOKEN  = "7a58917273a8734cbbe6bc498d78e390b3c2e56e"
    _REFRESH_TOKEN = "463a35741a82af231b5d150deb7be5e69c48c386"

    def __init__(self):
        self._client = ImgurClient(ImgurUtils._CLIENT_ID,
                                   ImgurUtils._CLIENT_SECRET,
                                   ImgurUtils._ACCESS_TOKEN,
                                   ImgurUtils._REFRESH_TOKEN)

    '''
    Takes a float value and converts to a formatted datetime string

    @param: 'epoch' is of type float (e.g. 123456789.0)
    @return: a formatted string (e.g. '2017-10-16 15:56:03')
    '''
    def _get_local_time(self,epoch):
        logger = logging.getLogger(__name__)
        timestamp = str()
        try:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch))
        except Exception as error_msg:
            logger.error(error_msg)
        return timestamp

    '''
    Retrieves all albums for a given account (e.g. DermaGram). For each
    album, checks if the title matches the current user's uuid. This is
    because we name albums based on the user's uuid.

    @return: a unique album.id if match exists; otherwise, None
    '''
    def _get_album_id_by_title(self, username):
        album_id = None
        albums = self._client.get_account_albums(ImgurUtils._ACCOUNT_NAME)
        for album in albums:
            if ( username == album.title ):
                album_id = album.id
                break
        return album_id

    '''
    Retrieves all albums for a given account (e.g. DermaGram). For each album,
    adds the 'title' property to a set.

    @return: a set of unique strings corresponding to album titles.
    '''
    def _get_album_titles_as_set(self):
        album_titles = set()
        albums = self._client.get_account_albums(ImgurUtils._ACCOUNT_NAME)
        for album in albums:
            album_titles.add( str(album.title) )
        return album_titles

    '''
    Retrieves images from Imgur using an album_id. The image's id, title, description
    and datetime are stored in an object 'image_info' and appended to a list 'image_history'

    @return: a list of objects containing info. about each image.
    '''
    def get_images_from_album(self, album_id):
        logger = logging.getLogger(__name__)
        images_data = {
            "carousel": [],
            "table": []
        }
        images = self._client.get_album_images( album_id )

        if images:
            # Sort images in descending chronological order
            images.sort(key=lambda x: x.datetime, reverse=True)
            for image in images:
                #Uncomment to list all properties that may be retrieved from an imgur Image object
                #print dir(image)
                info = self._parse_description(image.description)
                image_info = {
                    'id': str(image.id),
                    'title': str(image.title),
                    'location': info['location'],
                    'classification': info['classification'],
                    'datetime': self._get_local_time(float(image.datetime)),
                }
                images_data['table'].append(image_info)

                images_data['carousel'].append(image.link)
        else:
            logger.warning('No images returned for album_id: {0}.'
                           '\nget_album_images() response: {1}'.format( album_id, images ))
        return images_data

    def _parse_description(self,description):
        info = ""
        try:
            info = json.loads(description)
        except Exception as e:
            print "ERROR: ",e
        return info
    '''
    Checks if album already exists for given uuid. Note: an album's title
    corresponds to the user's uuid.

    @return: boolean True if album exists; otherwise False
    '''
    def _does_album_exist(self, username):
        album_titles = self._get_album_titles_as_set()
        return True if username in album_titles else False

    '''
    Creates a new album where the album's title is the user's uuid.
    An new album id that is created in the process is returned.

    @return: a string variable corresponding to the album's unique id
    '''
    def create_new_album(self, username):
        logger = logging.getLogger(__name__)
        new_album_id = None

        #TODO we need to do check if username already exists as album name
        if ( False ):
            existing_album_id = self._get_album_id_by_title(username)
            logger.error("The uuid {0} already has an album id: {1}".format(
                username, existing_album_id ) )
        else:
            logger.info( "Creating a new album for {0}".format( username ) )
            album_info = {
                "title": username,
                "privacy": "public"
            }
            self._client.create_album(album_info)
            new_album_id = self._get_album_id_by_title(username)

            if new_album_id:
                logger.info("The new album id for user {0} is: {1}".format(
                    username, new_album_id ) )
            else:
                logger.error("There was an error getting the album_id.")

        return new_album_id

    #https://github.com/Imgur/imgurpython/blob/3a285f758bcb8a2ff6aa024b2944f464f50d87d0/examples/upload.py
    def add_image_to_album(self, album_id, title, location, classification, image_path):
        #TODO make this pull correct album and other data from user session
        description = {
            "location": location,
            "classification": classification
        }
        config = {
            'album': album_id,
            'title': title,
            'description': json.dumps(description)
        }
        return self._client.upload_from_path(image_path, config=config, anon=False)