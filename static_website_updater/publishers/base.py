from abc import ABCMeta, abstractmethod


class BasePublisher(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def publish(self, jekyll_website): pass