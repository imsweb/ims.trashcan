from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import importObjects
from ims.trashcan.config import *

def importCatalogTool(portal, context):
    """Import catalog tool.
    """
    tool = getToolByName(portal, 'portal_trash_catalog')

    importObjects(tool, '', context)

def importVarious(context):
    """Miscellanous steps import handle
    """
    
    portal = context.getSite()
    importCatalogTool(portal,context)