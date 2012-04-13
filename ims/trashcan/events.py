from zope import interface, component
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

def trashEventHandler(ob,event):
    """ Item is deleted - trash it!"""
    portal = component.queryUtility(ISiteRoot)
    if portal:
      can = getToolByName(portal,'portal_trash_can',None)

      if can: # it might not be installed!
        can.trash(ob)

def trashAdded(ob,event):
    """Index"""
    cat = getToolByName(ob,'portal_trash_catalog',None)
    if cat:
      cat.indexObject(ob)

def trashRemoved(ob,event):
    """Unindex"""
    cat = getToolByName(ob,'portal_trash_catalog',None)
    if cat:
      cat.unindexObject(ob)