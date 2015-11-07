from datetime import datetime

from static_website_updater.content_providers.base import BaseContentProvider
from static_website_updater.utils.flickr_post import create_flickr_post_body, create_flickr_post_name


class FlickrContentProvider(BaseContentProvider):
    def __init__(self, flickr_photoset):
        self.flickr_photoset = flickr_photoset

    def cleanup(self, jekyll_project):
        jekyll_project.remove_all_posts(
            lambda fname: fname.endswith(".md") and "-flickr-" in fname)

    def add_content(self, jekyll_project):
        photos = self.flickr_photoset.get_photos()
        file_paths = set()
        for photo in photos:
            date = datetime.utcfromtimestamp(photo.timestamp)
            filename = jekyll_project.add_post(
                date=date,
                post_name=create_flickr_post_name(photo),
                post_contents=create_flickr_post_body(photo))
            file_paths.add(filename)
        return file_paths
