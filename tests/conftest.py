from ims.trashcan.testing import FUNCTIONAL_TESTING
from ims.trashcan.testing import INTEGRATION_TESTING
from pytest_plone import fixtures_factory
import pytest
from plone import api

pytest_plugins = ["pytest_plone"]

globals().update(
    fixtures_factory((
        (FUNCTIONAL_TESTING, "functional"),
        (INTEGRATION_TESTING, "integration"),
    ))
)


@pytest.fixture
def can(portal):
    return api.portal.get_tool("portal_trash_can")
