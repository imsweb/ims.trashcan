from Products.CMFCore import utils, DirectoryView
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from OFS import Folder

from config import *
import permissions

DirectoryView.registerDirectory(SKINS_DIR, GLOBALS)


def initialize(context):
    import trash, manager, catalog

    utils.ToolInit(
      '%s Tool' % PROJECTNAME,
      tools=(trash.PloneTrashCan,catalog.TrashCatalog),
      icon='tool.png', ).initialize(context)

    context.registerClass(
        trash.TrashedItem,
        constructors=(trash.manage_addTrashedItemForm,
                      trash.manage_addTrashedItem),
        icon='tool.png',
        )
        
    context.registerClass(
        manager.PloneTrashManager,
        constructors=(manager.manage_addPloneTrashManagerForm,
                      manager.manage_addPloneTrashManager),
        icon='tool.png',
        )