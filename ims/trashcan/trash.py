from zope.interface import Interface, implements
from OFS.ObjectManager import ObjectManager
import plone.api
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from ZODB.blob import Blob
from DateTime import DateTime

from ims.trashcan.interfaces import ITrashedItem

class TrashedItem(ObjectManager):
    implements(ITrashedItem)
    manage_main = PageTemplateFile('www/manage_trashedItem', globals())
    _created = ''

    def __init__(self, id, title='', data=None, path=''):
        self.id = id
        self.data = Blob(data)
        self.path = path
        self.Title = title
        self._created = DateTime()

    def manage_properties(self):
        return {
            'title': self.Title,
            'created': plone.api.portal.get_localized_time(self._created, long_format=True),
            'id': self.id,
        }

    def created(self):
        return self._created

    def getId(self):
        """ needed for indexing """
        return self.id
