from django.test import TestCase

# Create your tests here.

from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from .views import inventory_list


class InventoryValidationTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @patch("mainapp.views.Store.objects.filter")
    @patch("mainapp.views.Item.objects.filter")
    def test_negative_quantity_is_rejected(
        self, mock_item_filter, mock_store_filter
    ):
        # Simulate valid item and store selections.
        mock_item_filter.return_value.exists.return_value = True
        mock_store_filter.return_value.exists.return_value = True

        request = self.factory.post(
            "/inventory/",
            {
                "itemID": "I102",
                "storeID": "S101",
                "quantity": "-5",
            },
        )

        # RequestFactory does not automatically attach messages.
        from django.contrib.messages.storage.fallback import FallbackStorage

        request.session = {}
        request._messages = FallbackStorage(request)

        response = inventory_list(request)

        # Invalid quantities should redirect to Inventory Management.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/inventory/")

        # No database write should be attempted.
        mock_item_filter.assert_called_once()
        mock_store_filter.assert_called_once()


    @patch("mainapp.views.Store.objects.filter")
    @patch("mainapp.views.Item.objects.filter")
    def test_quantity_above_maximum_is_rejected(
        self, mock_item_filter, mock_store_filter
    ):
        mock_item_filter.return_value.exists.return_value = True
        mock_store_filter.return_value.exists.return_value = True

        request = self.factory.post(
            "/inventory/",
            {
                "itemID": "I102",
                "storeID": "S101",
                "quantity": "1000000.00",
            },
        )

        from django.contrib.messages.storage.fallback import FallbackStorage

        request.session = {}
        request._messages = FallbackStorage(request)

        response = inventory_list(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/inventory/")


    @patch("mainapp.views.Store.objects.filter")
    @patch("mainapp.views.Item.objects.filter")
    def test_quantity_with_three_decimal_places_is_rejected(
        self, mock_item_filter, mock_store_filter
    ):
        mock_item_filter.return_value.exists.return_value = True
        mock_store_filter.return_value.exists.return_value = True

        request = self.factory.post(
            "/inventory/",
            {
                "itemID": "I102",
                "storeID": "S101",
                "quantity": "12.345",
            },
        )

        from django.contrib.messages.storage.fallback import FallbackStorage

        request.session = {}
        request._messages = FallbackStorage(request)

        response = inventory_list(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/inventory/")


    @patch("mainapp.views.Store.objects.filter")
    @patch("mainapp.views.Item.objects.filter")
    def test_invalid_item_is_rejected(
        self, mock_item_filter, mock_store_filter
    ):
        # Simulate an item that does not exist.
        mock_item_filter.return_value.exists.return_value = False

        request = self.factory.post(
            "/inventory/",
            {
                "itemID": "INVALID",
                "storeID": "S101",
                "quantity": "10.00",
            },
        )

        from django.contrib.messages.storage.fallback import FallbackStorage

        request.session = {}
        request._messages = FallbackStorage(request)

        response = inventory_list(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/inventory/")

        # The invalid item should be rejected before checking the store.
        mock_item_filter.assert_called_once_with(itemid="INVALID")
        mock_store_filter.assert_not_called()


    @patch("mainapp.views.Store.objects.filter")
    @patch("mainapp.views.Item.objects.filter")
    def test_invalid_store_is_rejected(
        self, mock_item_filter, mock_store_filter
    ):
        # Simulate a valid item but an invalid store.
        mock_item_filter.return_value.exists.return_value = True
        mock_store_filter.return_value.exists.return_value = False

        request = self.factory.post(
            "/inventory/",
            {
                "itemID": "I102",
                "storeID": "INVALID",
                "quantity": "10.00",
            },
        )

        from django.contrib.messages.storage.fallback import FallbackStorage

        request.session = {}
        request._messages = FallbackStorage(request)

        response = inventory_list(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/inventory/")

        mock_item_filter.assert_called_once_with(itemid="I102")
        mock_store_filter.assert_called_once_with(storeid="INVALID")