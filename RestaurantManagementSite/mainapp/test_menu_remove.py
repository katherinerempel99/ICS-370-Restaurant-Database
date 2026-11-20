
from unittest import TestCase
from unittest.mock import MagicMock, patch

from django.db import DatabaseError
from django.http import HttpResponse
from django.test import RequestFactory

from .MenuRemove import remove_menu, remove_menu_view
import json
import tempfile
from pathlib import Path

from .MenuRemove import remove_recipe

class MenuRemoveTests(TestCase):
    """Tests for the Menu removal database logic."""

    @patch("mainapp.MenuRemove.transaction.atomic")
    @patch("mainapp.MenuRemove.connection.cursor")
    def test_remove_existing_menu(self, mock_cursor, mock_atomic):
        cursor = MagicMock()
        mock_cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = ("M101",)

        result = remove_menu("M101")

        self.assertTrue(result)
        self.assertEqual(cursor.execute.call_count, 4)

        # Confirm the final query deletes the Menu record.
        self.assertIn(
            "DELETE FROM Menu WHERE menuID = %s",
            cursor.execute.call_args.args[0],
        )

    @patch("mainapp.MenuRemove.transaction.atomic")
    @patch("mainapp.MenuRemove.connection.cursor")
    def test_remove_nonexistent_menu(self, mock_cursor, mock_atomic):
        cursor = MagicMock()
        mock_cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = None

        result = remove_menu("M999")

        self.assertFalse(result)
        self.assertEqual(cursor.execute.call_count, 1)

    def test_reject_invalid_menu_id(self):
        with self.assertRaises(ValueError):
            remove_menu("")

        with self.assertRaises(ValueError):
            remove_menu("INVALID123456")

    @patch("mainapp.MenuRemove.transaction.atomic")
    @patch("mainapp.MenuRemove.connection.cursor")
    def test_database_error_propagates(self, mock_cursor, mock_atomic):
        cursor = MagicMock()
        mock_cursor.return_value.__enter__.return_value = cursor
        cursor.fetchone.return_value = ("M101",)

        cursor.execute.side_effect = [
            None,
            None,
            DatabaseError("Deletion failed"),
        ]

        with self.assertRaises(DatabaseError):
            remove_menu("M101")

        self.assertTrue(mock_atomic.return_value.__exit__.called)


class MenuRemoveViewTests(TestCase):
    """Tests for the Menu removal Django view."""

    def setUp(self):
        self.factory = RequestFactory()

        # Simulate an authenticated staff member.
        self.staff_user = MagicMock()
        self.staff_user.is_authenticated = True
        self.staff_user.is_staff = True

    @patch("mainapp.MenuRemove.redirect")
    @patch("mainapp.MenuRemove.messages.success")
    @patch("mainapp.MenuRemove.remove_menu")
    def test_successful_removal(
        self, mock_remove, mock_success, mock_redirect
    ):
        mock_remove.return_value = True
        mock_redirect.return_value = HttpResponse(status=302)

        request = self.factory.post("/menu/remove/M101/")
        request.user = self.staff_user

        response = remove_menu_view(request, "M101")

        self.assertEqual(response.status_code, 302)
        mock_remove.assert_called_once_with("M101")
        mock_success.assert_called_once()

    @patch("mainapp.MenuRemove.redirect")
    @patch("mainapp.MenuRemove.messages.error")
    @patch("mainapp.MenuRemove.remove_menu")
    def test_nonexistent_menu(
        self, mock_remove, mock_error, mock_redirect
    ):
        mock_remove.return_value = False
        mock_redirect.return_value = HttpResponse(status=302)

        request = self.factory.post("/menu/remove/M999/")
        request.user = self.staff_user

        response = remove_menu_view(request, "M999")

        self.assertEqual(response.status_code, 302)
        mock_remove.assert_called_once_with("M999")
        mock_error.assert_called_once()

    @patch("mainapp.MenuRemove.remove_menu")
    def test_get_request_not_allowed(self, mock_remove):
        request = self.factory.get("/menu/remove/M101/")
        request.user = self.staff_user

        response = remove_menu_view(request, "M101")

        self.assertEqual(response.status_code, 405)
        mock_remove.assert_not_called()

    @patch("mainapp.MenuRemove.redirect")
    @patch("mainapp.MenuRemove.remove_menu")
    def test_non_staff_user_cannot_remove(
        self, mock_remove, mock_redirect
    ):
        request = self.factory.post("/menu/remove/M101/")

        request.user = MagicMock()
        request.user.is_authenticated = True
        request.user.is_staff = False

        response = remove_menu_view(request, "M101")

        self.assertEqual(response.status_code, 302)
        mock_remove.assert_not_called()

    @patch("mainapp.MenuRemove.redirect")
    @patch("mainapp.MenuRemove.remove_menu")
    def test_unauthenticated_user_cannot_remove(
        self, mock_remove, mock_redirect
    ):
        request = self.factory.post("/menu/remove/M101/")

        request.user = MagicMock()
        request.user.is_authenticated = False
        request.user.is_staff = False

        response = remove_menu_view(request, "M101")

        self.assertEqual(response.status_code, 302)
        mock_remove.assert_not_called()

class MenuRemoveJSONTests(TestCase):
    """Tests for removing recipes from JSON."""

    def test_remove_existing_recipe(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "Recipes.json"

            data = {
                "recipe": [
                    {"id": "R101", "name": "Chicken Alfredo"},
                    {"id": "R102", "name": "Beef Tacos"}
                ]
            }

            file_path.write_text(
                json.dumps(data),
                encoding="utf-8"
            )

            result = remove_recipe("R101", file_path)

            self.assertTrue(result)

            updated = json.loads(
                file_path.read_text(encoding="utf-8")
            )

            self.assertEqual(len(updated["recipe"]), 1)
            self.assertEqual(updated["recipe"][0]["id"], "R102")

    def test_remove_nonexistent_recipe(self):
        with tempfile.TemporaryDirectory() as folder:
            file_path = Path(folder) / "Recipes.json"

            data = {
                "recipe": [
                    {"id": "R101", "name": "Chicken Alfredo"}
                ]
            }

            file_path.write_text(
                json.dumps(data),
                encoding="utf-8"
            )

            result = remove_recipe("R999", file_path)

            self.assertFalse(result)

            updated = json.loads(
                file_path.read_text(encoding="utf-8")
            )

            self.assertEqual(len(updated["recipe"]), 1)