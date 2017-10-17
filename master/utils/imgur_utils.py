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
