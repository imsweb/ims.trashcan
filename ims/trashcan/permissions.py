from Products.CMFCore import permissions as CMFCorePermissions
import config

# manage the trash can
ManageTrash = "%s: Manage trash can" % config.PROJECTNAME

CMFCorePermissions.setDefaultRoles(ManageTrash, ('Manager',))
