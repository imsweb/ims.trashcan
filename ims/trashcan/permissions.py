from AccessControl.Permission import addPermission

# manage the trash can
ManageTrash = "ims.trashcan: Manage trash can"

addPermission(ManageTrash, ("Manager",))
