from Products.CMFCore import utils

import permissions
MAX_TRASH_SIZE = 1e9


def initialize(context):
    import trash
    import manager
    import can

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
