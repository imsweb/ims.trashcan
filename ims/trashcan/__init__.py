from Products.CMFCore import utils
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.CMFCore.DirectoryView import registerDirectory
from OFS import Folder

from config import *
import permissions

registerDirectory('skins', GLOBALS)

def initialize(context):
    import trash, manager, catalog, can

    utils.ToolInit(
      '%s Tool' % PROJECTNAME,
      tools=(can.PloneTrashCan,catalog.TrashCatalog),
      icon='tool.png', ).initialize(context)
        
    context.registerClass(
        manager.PloneTrashManager,
        constructors=(manager.manage_addPloneTrashManagerForm,
                      manager.manage_addPloneTrashManager),
        icon='tool.png',
        )
