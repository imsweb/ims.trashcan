from zope.interface import Interface
from zope.schema import Bytes, TextLine

class ITrashedItem(Interface):
    """ deleted item with trash wrapper """
    id = TextLine(
           title=u"ID",
           description=u"ID",)

    Title = TextLine(
           title=u"Title",
           description=u"Original title",)
  
    data = Bytes(
          title=u"Data",
          description=u"The fake zexp file",)

    path = TextLine(
           title=u"Path",
           description=u"The path to its restore point",)