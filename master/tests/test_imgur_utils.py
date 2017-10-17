
#TODO: setup pytest
#TODO: add readme explaining how to use these functions to unit test imgur_utils

'''
The following tests should be used w/ pytest
to fully test all code in imgur_utils
'''
def test_get_image_history(self):
    images = self.get_image_history()
    for image in images:
        # TODO add check here that id == expected_id, etc.
        print 'Id: ', image['id'], \
            '\nTitle: ', image['title'], \
            '\nDescription: ', image['description'], \
            '\nDatetime: ', image['datetime']