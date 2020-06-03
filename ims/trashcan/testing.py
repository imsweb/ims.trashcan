from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting, applyProfile
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
import ims.trashcan
import collective.js.jqueryui


class TrashcanSiteLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configuration_context):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.js.jqueryui)
        self.loadZCML(package=ims.trashcan)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ims.trashcan:default')


TRASHCAN_SITE_FIXTURE = TrashcanSiteLayer()

INTEGRATION = IntegrationTesting(
    bases=(TRASHCAN_SITE_FIXTURE,),
    name="ims.trashcan:Integration"
)

FUNCTIONAL = FunctionalTesting(
    bases=(TRASHCAN_SITE_FIXTURE,),
    name="ims.trashcan:Functional"
)
