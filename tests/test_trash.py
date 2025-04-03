from plone import api
from plone.app.textfield.value import RichTextValue

from plone.namedfile.file import NamedBlobFile


class TestTrashCan:
    def test_document(self, portal, can):
        with api.env.adopt_roles(["Manager"]):
            page = api.content.create(id="page1", type="Document", title="My page", container=portal)
            page.text = RichTextValue("some text")
            api.content.delete(page)
            assert len(can.objectIds()) == 1

    def test_file(self, portal, can):
        with api.env.adopt_roles(["Manager"]):
            _file = api.content.create(id="file1", type="File", title="My file", container=portal)
            api.content.delete(_file)
            assert len(can.objectIds()) == 1

    def test_file_limit(self, portal, can):
        with api.env.adopt_roles(["Manager"]):
            _file = api.content.create(id="file1", type="File", title="My file", container=portal)
            _file.file = NamedBlobFile()
            _file.file.data = "hello, world"
            _file.file.__dict__["size"] = 1e10  # fake it
            api.content.delete(_file)
        assert len(can.objectIds()) == 0
