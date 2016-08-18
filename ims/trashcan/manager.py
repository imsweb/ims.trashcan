from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
import plone.api
from Products.CMFCore.permissions import ManagePortal
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager
from zope.component.hooks import setSite

manage_addPloneTrashManagerForm = PageTemplateFile(
    'www/trashManagerAdd', globals())


def manage_addPloneTrashManager(self, id, title='', REQUEST=None):
    """Adds a new PloneTrashManager object with id *id*.
    """
    id = str(id)
    ob = PloneTrashManager(id, title)
    self._setObject(id, ob)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(self.absolute_url() + '/manage_main')

add = manage_addPloneTrashManager


class PloneTrashManager(SimpleItem, PropertyManager):
    """Plone Trash Manager"""
    security = ClassSecurityInfo()
    meta_type = 'Plone Trash Manager'
    manage_main = PageTemplateFile(
        'www/manage_trashManager', globals())
    index_html = None

    manage_options = ({'label': 'Manage', 'action': 'manage_main'},
                      ) + PropertyManager.manage_options

    _properties = ()

    def __init__(self, id='', title=''):
        """Initialize a new PloneTrashManager instance
        """
        self.id = id
        self.title = title

    security.declareProtected(ManagePortal, 'manage_takeOutTrash')
    def manage_takeOutTrash(self):
        """Crawls through the portals and deletes expired trash"""
        context = self.restrictedTraverse('/')
        self.site_crawl(context)

    security.declareProtected(ManagePortal, 'site_crawl')
    def site_crawl(self, context):
        """Recursive method to get each portal"""
        for portal in context.objectValues('Plone Site'):
            setSite(portal)
            try:
                can = plone.api.portal.get_tool('portal_trash_can')
            except plone.api.exc.InvalidParameterError:
                pass # not installed
            else:
                can()
        for folder in context.objectValues('Folder'):
            self.site_crawl(folder)

    __call__ = manage_takeOutTrash

InitializeClass(PloneTrashManager)