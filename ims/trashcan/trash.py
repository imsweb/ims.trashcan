__author__  = """Eric Wohnlich"""
__docformat__ = 'plaintext'

from Products.CMFCore.utils import getToolByName
from OFS.Folder import Folder
from AccessControl import ClassSecurityInfo
from permissions import ManageTrash
from Globals import InitializeClass, DTMLFile
from Products.Archetypes.ReferenceEngine import Reference
from Products.Archetypes.Referenceable import Referenceable
from Products.Archetypes.exceptions import ReferenceException
from DateTime import DateTime

class TrashRelationClass(Reference):
  relationship = 'Trash Relationship'  

class PloneTrashCan(Folder):
    """Plone Trash Can"""
    security = ClassSecurityInfo()
    disposal_frequency=7

    manage_options = [{'label':'Trash Can','action':'manage_main'},
                      {'label':'Configuration','action':'manage_propertiesForm'}]
    
    _properties=({'id':'disposal_frequency','type':'int','mode':'w'},)
      
    security.declarePublic('copyToTrash')
    def copyToTrash(self, object, REQUEST):
      """Copy the object to the Trash Can"""
      folder = self.getTrashWrapper(object)
      cp=None
      if REQUEST and REQUEST.has_key('__cp'):
        cp=REQUEST['__cp']
      try:
        object.manage_beforeDelete(object,object.aq_inner.aq_parent)
      except AttributeError:
        # has no manage_beforeDelete functions
        pass
      parent=object.aq_inner.aq_parent
      ob=parent.manage_copyObjects(ids=[object.getId()])
      folder.manage_pasteObjects(ob)
      try:
        folder.addReference(object.getParentNode(),relationship=TrashRelationClass.relationship,relation=TrashRelationClass)
      except ReferenceException:
        pass # what can we do?
      folder.setOrigPath('/'.join(object.getParentNode().getPhysicalPath()))
      
      self._unindexAfterCopy()
      
      if cp:
        REQUEST.set('__cp',cp)
      
    security.declarePrivate('_unindexAfterCopy')
    def _unindexAfterCopy(self):
      cat = getToolByName(self,'portal_catalog')
      portal = getToolByName(self,'portal_url').getPortalObject()
      trash_path = '%s/portal_trash_can' % '/'.join(portal.getPhysicalPath())
      
      brains = cat(path=trash_path)
      for brain in brains:
        try:
          brain.getObject().unindexObject()
        except KeyError:
          pass
      
    security.declarePublic('getTrashWrapper')
    def getTrashWrapper(self,object):
      """Returns a wrapper for this item"""
      if object.getId() not in self.objectIds():
        # create the Trashed Item Wrapper
        from DateTime import DateTime
        from random import random
        now=DateTime()
        time='%s.%s' % (now.strftime('%Y-%m-%d'), str(now.millis())[7:])
        rand=str(random())[2:6]
        obj_id = '%s-%s' % (object.getId(),time+rand)
        self.manage_addProduct['PloneTrashCan'].manage_addTrashedItem(obj_id)
        return self.restrictedTraverse(obj_id)
      else:
        return self.restrictedTraverse(object.getId())
        
    security.declareProtected(ManageTrash, 'deleteExpired')
    def deleteExpired(self):
      """Delete all of the content that is expired
         Content expires when it is older than X days, where X is the disposal_frequency property
      """
      from DateTime import DateTime
      expiredDate = DateTime()-self.disposal_frequency
      cat = getToolByName(self,'portal_trash_catalog')
      expired = cat(created={'query':expiredDate,'range':'max'})
      self.manage_delObjects(ids=[e.id for e in expired if e.id in self.objectIds()])
    
    __call__ = deleteExpired
        
manage_addTrashedItemForm=DTMLFile('www/trashedItemAdd', GLOBALS)

def manage_addTrashedItem(self, id, title='', REQUEST=None):
  """Adds a new Trashed Item Wrapper"""
  id = str(id)
  ob = TrashedItem(id, title)
  self._setObject(id, ob)
  
  if REQUEST is not None:
      REQUEST['RESPONSE'].redirect(self.absolute_url()+'/manage_main')

add = manage_addTrashedItem
        
class TrashedItem(Folder,Referenceable):
    """Trashed Item"""
    portal_type = meta_type = 'Trashed Item'
    manage=manage_main = DTMLFile('www/manage_trashedItem', GLOBALS)
    manage_main._setName('manage_main')
    security = ClassSecurityInfo()
    origpath = ''
    created = ''

    manage_options = ({'label':'Trashed Item','action':'manage_main'},)

    def __init__(self, id='', title=''):
        """Initialize a new TrashedItem instance
        """
        self.created = DateTime()
        self.id = id
        self.title = title
        
    security.declarePublic('CreationDate')
    def CreationDate(self):
      return self.created is None and 'Unknown' or self.created.ISO()

    security.declarePublic('setOrigPath')
    def setOrigPath(self, p):
      self.origpath = p
      
    security.declarePublic('getOrigPath')
    def getOrigPath(self):
      return self.origpath
    
    def _verifyObjectPaste(self, object, validate_src=1):
      return True;
      
    def manage_copyTrash(self, REQUEST=None):
      """Copies the trashed item to the clip board"""
      if self.objectIds():
        ob = self.objectIds()[0]
        self.manage_copyObjects(ob, REQUEST)
        
      if REQUEST is not None:
        msg = 'Copied item'
        return self.manage_main(self, REQUEST, manage_tabs_message=msg)
        
    def manage_copyToReference(self, REQUEST=None):
      """Copies the trashed item to its original source via a reference"""
      msg = 'Source no longer exists, or source is the root'
      clipboard = self.saveClipboard(REQUEST)
      if self.objectIds():
        ob = self.objectIds()[0]
        self.manage_copyObjects(ob, REQUEST)
        
        refs = [r for r in self.getRefs(relationship='Trash Relationship') if r]
        if refs:
          ref = refs[0]
          ref.manage_pasteObjects(REQUEST['__cp'])
          msg = '%s restored' % ob
        
      if REQUEST is not None:
        self.restoreClipboard(clipboard,REQUEST)
        return self.manage_main(self, REQUEST, manage_tabs_message=msg)
        
    def manage_copyToPath(self, REQUEST=None):
      """Attempts to copy the trashed item to its original path"""
      msg=''
      clipboard = self.saveClipboard(REQUEST)
      if self.objectIds():
        ob = self.objectIds()[0]
        self.manage_copyObjects(ob, REQUEST)
        
        try:
          source = self.restrictedTraverse(self.getOrigPath())
          source.manage_pasteObjects(REQUEST['__cp'])
          msg = '%s restored to %s' % (ob,self.getOrigPath())
        except KeyError:
          msg='Path is invalid'
        except ValueError:
          msg='Disallowed to paste object to this path'
        
      if REQUEST is not None:
        self.restoreClipboard(clipboard,REQUEST)
        return self.manage_main(self, REQUEST, manage_tabs_message=msg)
        
    def saveClipboard(self,REQUEST):
      """If we are going to copy/paste to a path, or using a reference, we can save and restore the
         current clipboard data
      """
      if REQUEST is not None:
        clipboard = REQUEST.get('__cp','')
        return clipboard
        
    def restoreClipboard(self,clipboard,REQUEST):
      """If we are going to copy/paste to a path, or using a reference, we can save and restore the
         current clipboard data
      """
      if REQUEST is not None and clipboard:
        REQUEST.set('__cp',clipboard)
        
    def manage_afterAdd(self, item, container):
      cat = getToolByName(self,'portal_trash_catalog')
      cat.indexObject(self)
        
    def manage_beforeDelete(self, item, container):
      cat = getToolByName(self,'portal_trash_catalog')
      cat.unindexObject(self)
      
InitializeClass(TrashedItem)