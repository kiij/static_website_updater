from abc import ABCMeta, abstractmethod


class BaseContentProvider(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def cleanup(self, jekyll_project): pass

    @abstractmethod
    def add_content(self, jekyll_project): pass