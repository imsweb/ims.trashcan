from Products.CMFCore.utils import getToolByName
import transaction

def empty_trash():
  import logging
  from ims.cronmanager.startup import startup
  context = startup()
  logger = logging.getLogger('ims.trashcan')

  def siteCrawl(context):
    for portal in context.objectValues('Plone Site'):
      trashman = getToolByName(portal,'portal_trash_can',None)
      if trashman:
        logger.info('emptying trash for: %s' % '/'.join(portal.getPhysicalPath()))
        trashman()
        transaction.commit()
    for folder in context.objectValues('Folder'):
      siteCrawl(folder)
  siteCrawl(context)