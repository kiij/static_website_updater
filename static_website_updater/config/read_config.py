import json

from static_website_updater.content_providers.flickr import FlickrContentProvider
from static_website_updater.exceptions.exceptions import InvalidConfigError
from static_website_updater.publishers.s3 import S3Publisher
from static_website_updater.utils.flickr import FlickrPhotoset
from static_website_updater.website.git_repo import GitRepository


def read_config_from_file(fname):
    try:
        with open(fname) as file:
            data = json.load(file)
    except IOError:
        raise InvalidConfigError(
            message="Could not read configuration file: " + fname
        )
    return data


def create_git_from_config(config):
    if 'git' not in config:
        raise InvalidConfigError("Could not find git settings in configuration file")
    return GitRepository(
        remote=config['git']['remote'],
        author_name=config['git']['author name'],
        author_email=config['git']['author email']
    )


def create_content_providers_from_config(config):
    if 'content providers' not in config:
        raise InvalidConfigError("Could not find content providers in configuration file")

    content_providers = []
    for content_provider_config in config['content providers']:
        if not content_provider_config['type']:
            raise InvalidConfigError(
                message="Found content provider with no type specified")

        type = content_provider_config['type'].lower()
        parameters = content_provider_config['parameters']
        if type == "flickr":
            content_providers.append(
                FlickrContentProvider(
                    FlickrPhotoset(
                        api_key=parameters['api key'],
                        api_secret=parameters['api secret'],
                        user_id=parameters['user id'],
                        photoset_id=parameters['photoset id']
                    )
                )
            )
        else:
            raise InvalidConfigError(
                message="Unrecognized content provider type: " + type)
    return content_providers


def create_publishers_from_config(config):
    if 'content providers' not in config:
        raise InvalidConfigError("Could not find publishers in configuration file")

    publishers = []
    for publisher_config in config['publishers']:
        if not publisher_config['type']:
            raise InvalidConfigError(
                message="Found publisher with no type specified")

        type = publisher_config['type'].lower()
        parameters = publisher_config['parameters']
        if type == "s3":
            publishers.append(
                S3Publisher(
                    aws_access_key=parameters['aws access key'],
                    aws_secret_key=parameters['aws secret key'],
                    bucket_name=parameters['bucket name']
                )
            )
        else:
            raise InvalidConfigError(
                message="Unrecognized publisher type: " + type)
    return publishers
