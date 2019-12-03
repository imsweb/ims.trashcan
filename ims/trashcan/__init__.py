from Products.CMFCore import utils

from . import can
from . import manager


def initialize(context):
    utils.ToolInit(
        'ims.trashcan tool',
        tools=(can.PloneTrashCan,),
        icon='tool.png', ).initialize(context)

    context.registerClass(
        manager.PloneTrashManager,
        constructors=(manager.manage_addPloneTrashManagerForm,
                      manager.manage_addPloneTrashManager),
        icon='tool.png',
    )
