import pytest

PACKAGE_NAME = "ims.trashcan"


class TestUninstall:
    @pytest.fixture(autouse=True)
    def uninstalled(self, installer):
        installer.uninstall_product(PACKAGE_NAME)

    def test_product_uninstalled(self, installer):
        """Test if package is cleanly uninstalled."""
        assert installer.is_product_installed(PACKAGE_NAME) is False
