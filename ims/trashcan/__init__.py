from Products.CMFCore import utils

from . import can

__version__ = "5.1"


def initialize(context):
    utils.ToolInit(
        "ims.trashcan tool",
        tools=(can.PloneTrashCan,),
        icon="tool.png",
    ).initialize(context)
