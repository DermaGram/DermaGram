from imgurpython import ImgurClient
from utils.logging_utils import LoggingUtils
import time
import logging

LoggingUtils.initialize_logger(__name__)

class ImgurUtils:
    _ACCOUNT_NAME  = "DermaGram"
    _CLIENT_ID     = "74ab756d286b81b"
    _CLIENT_SECRET = "06e8cbd50c3388b95681efe0bf17e8578f72c8dd"
    _ACCESS_TOKEN  = "7a58917273a8734cbbe6bc498d78e390b3c2e56e"
    _REFRESH_TOKEN = "463a35741a82af231b5d150deb7be5e69c48c386"

    def __init__(self,uniqueUserId, albumId):
        self._client = ImgurClient(ImgurUtils._CLIENT_ID,
                                   ImgurUtils._CLIENT_SECRET,
                                   ImgurUtils._ACCESS_TOKEN,
                                   ImgurUtils._REFRESH_TOKEN)
        self._user_info = {
            'uuid': uniqueUserId,
            'album_id': albumId
        }

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
    def _get_album_id_by_title(self):
        album_id = None
        albums = self._client.get_account_albums(ImgurUtils._ACCOUNT_NAME)
        for album in albums:
            if ( self._user_info['uuid'] == album.title ):
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
    def get_image_history(self):
        logger = logging.getLogger(__name__)
        image_history = []
        images = self._client.get_album_images(self._user_info['album_id'])

        if images:
            for image in images:
                #Uncomment to list all properties that may be retrieved from an imgur Image object
                #print dir(image)
                image_info = {
                    'id': str(image.id),
                    'title': str(image.title),
                    'description': str(image.description),
                    'datetime': self._get_local_time(float(image.datetime))
                }
                image_history.append(image_info)
        else:
            logger.warning('No images returned for album_id: {0}.'
                           '\nget_album_images() response: {1}'.format( self._user_info['album_id'], images ))
        return image_history

    '''
    Checks if album already exists for given uuid. Note: an album's title
    corresponds to the user's uuid.

    @return: boolean True if album exists; otherwise False
    '''
    def _does_album_exist(self):
        album_titles = self._get_album_titles_as_set()
        return True if self._user_info['uuid'] in album_titles else False

    '''
    Creates a new album where the album's title is the user's uuid.
    An new album id that is created in the process is returned.

    @return: a string variable corresponding to the album's unique id
    '''
    def create_new_album(self):
        logger = logging.getLogger(__name__)
        new_album_id = None

        if ( self._does_album_exist() ):
            existing_album_id = self._get_album_id_by_title()
            logger.error("The uuid {0} already has an album id: {1}".format(
                self._user_info['uuid'], existing_album_id ) )
        else:
            logger.info( "Creating a new album for {0}".format( self._user_info['uuid'] ) )
            album_info = {
                "title": self._user_info['uuid'],
                "privacy": "public"
            }
            self._client.create_album(album_info)
            new_album_id = self._get_album_id_by_title()

            if new_album_id:
                logger.info("The new album id for user {0} is: {1}".format(
                    self._user_info['uuid'], new_album_id ) )
            else:
                logger.error("There was an error getting the album_id.")

        return new_album_id
