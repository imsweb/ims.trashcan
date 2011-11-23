General

 The **PloneTrashCan** works by inserting a new line into the **object_delete.cpy** and **folder_delete.cpy** scripts.  These scripts are already a wrapper for the common Zope method **manage_delObjects**. These controller scripts mostly handle redirection.  The lines we insert copy the object before it is deleted and sends it to the **PloneTrashCan (portal_trash_can)**.

 There are two things we need to handle here.

 1. We need to know when the object is deleted (the modified date will not, and should not, be updated on this copy)

 2. We need to be prepared for objects with the same id to be deleted.  They may have deleted it, recreated it, and deleted it again, or they may have just deleted two items from separate folders that had the same id.

 For these reasons, we "wrap" our object in a **PloneTrashedItem** object.  A **PloneTrashedItem** is a folderish content type, but it should include only one item - a copy of the object we deleted.  The **PloneTrashedItem** will have an id similar to the id of the object deleted, but with a date/random-value appended to it, so that we do not try to create two **PloneTrashedItems** with the same id.  This class also lets us override the **verifyCopyObject** method of Zope's default Folder, which insists that most Plone content types cannot be copied to it.  The **PloneTrashedItem** is also not an Archetypes content type, and will not be cataloged (we want the end-users to be completely ignorant of this trash can's existance).

Catalogs and Indexing

 There is a **PloneTrashCatalog (portal_trash_catalog)**  that exists to allow a speedy lookup of what items have expired.  It only stores ids and creation dates.  When we copy an object before deletion into the **PloneTrashCan** we must unindex the new copy from portal_catalog and index it in portal_trash_catalog.  We also unindex it from the latter when it gets removed from the **PloneTrashCan**.

Restoring Trashed Content

 There are three ways to restore trashed content, all of which are performed in the ZMI from the **PloneTrashedItem** (do noy try copying the **PloneTrashedItem** itself - this will give unintended results!)

 1. Copy - This copies the object to the Zope clipboard (using cookies), similar to how anything else is copied in the ZMI.  You should be able to paste it anywhere it is allowed.

 2. Copy to Referenced Container - The **PloneTrashedItem** creates a reference to the original container when it can, thanks to the Archetypes product.  The container must inherit from the Referenceable class, otherwise this option will not be available.  Almost all content on Plone sites is made with Archetypes, so they all subclass this, but the Plone Site itself does not.  For this reason, a reference cannot be made to the container of an object originally on the Plone root.  For all other content, this should be the preferred method of restoring content.  If you delete ObjA from FolderB, and FolderB gets moved somewhere else on the site, FolderB will keep its same UID (unique id).  When you try to restore the content, it will know that FolderB has moved, and put it there.

 3. Copy to Original Path - The original Zope path of the deleted content's container is also stored, mainly to be used if restoring by reference does not work.  The Plone Site may not be referenceable, but we should know its path (unless the Plone Site itself gets moved...)

 If the deleted content's *container* is later deleted, you will probably have to use the first method.  The simple "Copy" is a good fall back option.

Automating

 Calling **$portal_url/plone_trash_can** will call the **deleteExpired** method, which deletes all expired content.  Expired content is defined as all content older than X days before the time **deleteExpired** is called, where X is set by the **disposal_frequency** property of the **PloneTrashCan**.

 We can automate this process by having a Cron job make the above call.  But we will surely have multiple portals in one Zope instance, all of which have a **PloneTrashCan**.  For this reason, there is a **PloneTrashManager** which can be added in the Zope instance (outside of any portal) that crawls through that Zope instance, finding all Plone Sites with a **PloneTrashCan**, and emptying the expired trash on those sites.  Each portal is allowed to have a different **disposal_frequency**.