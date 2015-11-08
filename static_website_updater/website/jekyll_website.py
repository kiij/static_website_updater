import os

POST_FILENAME_DATE_FORMAT = "%Y-%m-%d"
POST_FILENAME_FORMAT = "{date}-{name}.md"


class JekyllWebsite(object):
    def __init__(self, git):
        self.git = git

    def get_path(self):
        return self.git.get_path()

    def get_site_path(self):
        return os.path.join(self.get_path(), "_site")

    def build(self):
        orig_wd = os.getcwd()
        os.chdir(self.get_path())
        os.system(["bundle", "install"])
        os.system(["bundle", "exec", "jekyll", "build"])
        #os.chdir(orig_wd)

        return os.path.join(self.get_path(), "_site")

    def remove_all_posts(self, fname_filter=None):
        path = self.git.get_path()
        posts_path = os.path.join(path, "_posts")
        for f in os.listdir(posts_path):
            if (not fname_filter) or (fname_filter and fname_filter(f)):
                self.git.delete_file(os.path.join("_posts", f))

    def add_post(self, date, post_name, post_contents):
        date_string = date.strftime(POST_FILENAME_DATE_FORMAT)
        fname = POST_FILENAME_FORMAT.format(
            date=date_string,
            name=post_name
        )
        fname = os.path.join("_posts", fname)
        self.git.add_file(fname, post_contents)
        return fname