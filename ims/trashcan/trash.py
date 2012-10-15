from zope.interface import Interface, implements
from OFS.ObjectManager import ObjectManager
from Globals import DTMLFile
from ims.trashcan.interfaces import ITrashedItem
from ZODB.blob import Blob
from DateTime import DateTime

class TrashedItem(ObjectManager):
    implements(ITrashedItem)
    manage_main = DTMLFile('www/manage_trashedItem', globals())

    def __init__(self,id,title='',data=None,path=''):
      self.id=id
      self.data = Blob(data)
      self.path = path
      self.Title = title
      self._created = DateTime()
      
    def created(self):
      return self._created

    def getId(self):
      """ needed for indexing """
      return self.id