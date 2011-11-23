from Products.CMFCore.CatalogTool import CatalogTool, ICatalogTool
from Products.CMFCore.utils import SimpleRecord
from Products.CMFPlone.utils import safe_callable
from AccessControl import ClassSecurityInfo
from zope.interface import Interface, implements, providedBy

class TrashCatalog(CatalogTool):
    """Trash Catalog"""
    implements(ICatalogTool)
    id = 'portal_trash_catalog'
    portal_type = meta_type = 'Trash Catalog'