from Products.CMFCore import utils
from OFS import Folder

from config import *
import permissions



def initialize(context):
    import trash
    import manager
    import can

    utils.ToolInit(
        '%s Tool' % PROJECTNAME,
        tools=(can.PloneTrashCan,),
        icon='tool.png', ).initialize(context)

    context.registerClass(
        manager.PloneTrashManager,
        constructors=(manager.manage_addPloneTrashManagerForm,
                      manager.manage_addPloneTrashManager),
        icon='tool.png',
    )
