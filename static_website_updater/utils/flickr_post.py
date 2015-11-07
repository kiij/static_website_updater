POST_FILE_PATH_TEMPLATE = "{date}-flickr-{id}.md"

POST_FILENAME_DATE_FORMAT = "%Y-%m-%d"

POST_TEMPLATE = """---
layout: flickr-photo-post
title: {title}
flickr-photo:
  farm: {farm_id}
  server: {server_id}
  photo_id: {photo_id}
  photo_secret: {photo_secret}
tags:
- flickr_photo

---

{description}

"""


def create_flickr_post_name(photo):
    return "flickr-" + photo.photo_id


def create_flickr_post_body(photo):
    return POST_TEMPLATE.format(
        title=photo.title,
        description=photo.description,
        farm_id=photo.farm_id,
        server_id=photo.server_id,
        photo_id=photo.photo_id,
        photo_secret=photo.photo_secret
    )
