from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ManagePortal as permission
from Products.CMFCore.utils import getToolByName
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
import Globals

manage_addPloneTrashManagerForm = Globals.DTMLFile('www/trashManagerAdd', globals())
def manage_addPloneTrashManager(self, id, title='', REQUEST=None):
    """Adds a new PloneTrashManager object with id *id*.
    """
    id = str(id)
    ob = PloneTrashManager(id, title)
    self._setObject(id, ob)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')

add = manage_addPloneTrashManager

class PloneTrashManager(SimpleItem,PropertyManager):
    """Plone Trash Manager"""
    security = ClassSecurityInfo()
    meta_type = 'Plone Trash Manager'
    manage=manage_main = Globals.DTMLFile('www/manage_trashManager', globals())
    manage_main._setName('manage_main')
    index_html = None

    manage_options=({'label':'Manage','action':'manage_main'},)+PropertyManager.manage_options

    _properties=()

    def __init__(self, id='', title=''):
        """Initialize a new PloneTrashManager instance
        """
        self.id = id
        self.title = title

    security.declareProtected(permission,'manage_takeOutTrash')
    def manage_takeOutTrash(self):
      """Crawls through the portals and deletes expired trash"""
      context=self.restrictedTraverse('/')
      self.siteCrawl(context)

    security.declareProtected(permission,'siteCrawl')
    def siteCrawl(self,context):
      """Recursive method to get each portal"""
      for portal in context.objectValues('Plone Site'):
        trashman = getToolByName(portal,'portal_trash_can',None)
        if trashman:
          trashman()
      for folder in context.objectValues('Folder'):
        self.siteCrawl(folder)

    __call__ = manage_takeOutTrash

Globals.InitializeClass(PloneTrashManager)