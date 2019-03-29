import plone.api
from AccessControl.SecurityInfo import ClassSecurityInfo
from DateTime import DateTime
from OFS.Folder import Folder
from permissions import ManageTrash
from plone.rfc822.interfaces import IPrimaryFieldInfo
from six import StringIO
from trash import TrashedItem

from . import MAX_TRASH_SIZE

try:
    from ims.upload.content import Chunk, ChunkedFile
except NameError:
    class Chunk(object):
        pass


def generate_id(start_id):
    now = DateTime()
    time_str = '%s.%s' % (now.strftime('%Y-%m-%d'), str(now.millis())[7:])
    return start_id + '-' + time_str


class PloneTrashCan(Folder):
    """Plone Trash Can"""
    security = ClassSecurityInfo()
    disposal_frequency = 7

    manage_options = [{'label': 'Trash Can', 'action': 'manage_main'},
                      {'label': 'Configuration', 'action': 'manage_propertiesForm'}]

    _properties = ({'id': 'disposal_frequency', 'type': 'int', 'mode': 'w'},)

    @staticmethod
    def trashable(ob):
        """ Don't trash anything too large. Only works on primary field objects """
        if isinstance(ob, Chunk):
            return False
        elif isinstance(ob, ChunkedFile):
            return False

        try:
            primary_field = IPrimaryFieldInfo(ob)
        except TypeError:
            return True
        else:
            if primary_field and primary_field.value and primary_field.value.size > MAX_TRASH_SIZE:
                return False
            return True

    def trash(self, ob):
        """ trash the item """
        if self.trashable(ob):
            id = generate_id(ob.getId())
            title = ob.Title()
            data = self.zexpickle(ob)
            opath = '/'.join(ob.getPhysicalPath()[:-1])
            _trash = TrashedItem(id, title, data, opath)
            self._setObject(id, _trash, suppress_events=True)

    def restore(self, id):
        """ restore the item to its original path
            if it exists, otherwise root """
        _trash = self[id]
        data = _trash.data.open("r").read()
        opath = _trash.path
        try:
            source = self.restrictedTraverse(opath)
        except KeyError:  # Path is invalid, likely the container was moved or deleted. Restore to root
            source = plone.api.portal.get()
        ob = self.unzexpickle(data)
        source._setObject(id[:-18], ob)
        self._delObject(id)

    def zexpickle(self, ob):
        """ pickle + add zexp wrapper """
        f = StringIO()
        ob._p_jar.exportFile(ob._p_oid, f)
        data = f.getvalue()
        return data

    def unzexpickle(self, data):
        """ unpickle + remove zexp wrapper """
        f = StringIO()
        f.write(data)

        # we HAVE to skip the first four characters, which are just
        # 'ZEXP', because _importDuringCommit does length validation
        # with the assumption that the file stream is already at this
        # point, not at SOF
        f.seek(4)

        conn = self._p_jar
        import transaction as t

        return_oid_list = []
        conn._import = f, return_oid_list
        conn._register()

        t.savepoint(optimistic=True)
        if return_oid_list:
            return conn.get(return_oid_list[0])
        else:
            return None

    security.declareProtected(ManageTrash, 'deleteExpired')

    def deleteExpired(self):
        """Delete all of the content that is expired
           Content expires when it is older than X days, where X is the disposal_frequency property
        """
        expiredDate = DateTime() - self.disposal_frequency
        for trash in self.objectValues():
            # "or not trash.created()" is to handle legacy items
            if expiredDate > trash.created() or not trash.created():
                self._delObject(trash.getId())

    security.declareProtected(ManageTrash, 'manage_restore')

    def manage_restore(self, id, REQUEST=None):
        """Attempts to copy the trashed item to its original path"""
        self.restore(id)

        msg = u'%s has been restored.' % id
        if REQUEST is not None:
            return self.manage_main(self, REQUEST, manage_tabs_message=msg)

    __call__ = deleteExpired
