from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.utils import importObjects
from ims.trashcan.config import *

def importVarious(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('imstrashcan_various.txt') is None:
        return
    
    portal = context.getSite()