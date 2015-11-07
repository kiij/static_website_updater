from collections import namedtuple

import flickrapi

FlickrPhoto = namedtuple('FlickrPhoto', 'title description timestamp farm_id server_id photo_id photo_secret')


class FlickrPhotoset(object):
    def __init__(self, api_key, api_secret, user_id, photoset_id):
        self.flickr = flickrapi.FlickrAPI(
            api_key, api_secret, format='parsed-json', store_token=False)
        self.user_id = user_id
        self.photoset_id = photoset_id

    def get_photos(self):
        photoset_response = self.flickr.photosets.getPhotos(
            user_id=self.user_id, photoset_id=self.photoset_id)
        photos = []
        for photoset_photo in photoset_response['photoset']['photo']:
            photo_response = self.flickr.photos.getInfo(photo_id=photoset_photo['id'])

            photo = FlickrPhoto(
                title=photoset_photo['title'],
                description=photo_response['photo']['description']['_content'],
                timestamp=int(photo_response['photo']['dates']['posted']),
                farm_id=photoset_photo['farm'],
                server_id=photoset_photo['server'],
                photo_id=photoset_photo['id'],
                photo_secret=photoset_photo['secret']
            )
            photos.append(photo)

        return photos
