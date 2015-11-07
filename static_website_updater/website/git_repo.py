import tempfile

import os
from git import Repo, Actor


class GitRepository(object):
    def __init__(self, remote, author_name, author_email):
        self.remote = remote
        self.repo = None
        self.author = Actor(author_name, author_email)

    def clone(self):
        tempdir = tempfile.mkdtemp()
        self.repo = Repo.clone_from(self.remote, tempdir)

    def switch_branch(self, branch_name):
        self.repo.git.checkout(branch_name)

    def delete_file(self, filename):
        index = self.repo.index
        index.remove([filename])
        os.remove(os.path.join(self.get_path(), filename))

    def add_file(self, filename, file_contents):
        new_file_path = os.path.join(self.repo.working_tree_dir, filename)

        f = open(new_file_path, 'w')
        f.write(file_contents)
        f.close()

        return new_file_path

    def commit_files(self, file_paths, message):
        index = self.repo.index
        index.add(file_paths)
        if index.diff('HEAD'):
            index.commit(message, author=self.author).type
            return True
        else:
            return False

    def push(self):
        self.repo.remotes.origin.push()

    def get_path(self):
        return self.repo.working_tree_dir

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO clean up repository here
        pass