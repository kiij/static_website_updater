import os

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from static_website_updater.publishers.base import BasePublisher


class S3Publisher(BasePublisher):
    def __init__(self, aws_access_key, aws_secret_key, bucket_name):
        self.conn = S3Connection(aws_access_key, aws_secret_key)
        self.bucket = self.conn.get_bucket(bucket_name)

    def _delete_contents_of_bucket(self):
        bucket_list_result_set = self.bucket.list()
        self.bucket.delete_keys([key.name for key in bucket_list_result_set])

    def publish(self, jekyll_website):
        # First, clear the bucket
        self._delete_contents_of_bucket()

        # construct the upload file list
        source_path = jekyll_website.get_site_path()
        upload_file_names = []
        print source_path
        for root, dirs, files in os.walk(source_path, topdown=False):
            for name in files:
                fname = os.path.join(root, name)
                upload_file_names.append((fname, fname.replace(source_path, "")))

        # start uploading
        for filename, key_id in upload_file_names:
            sourcepath = filename
            destpath = key_id

            k = Key(self.bucket)
            k.key = destpath
            print '- Uploading %s as %s' % \
                  (sourcepath, destpath)
            k.set_contents_from_filename(sourcepath)
