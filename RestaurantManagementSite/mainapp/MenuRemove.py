
from django.db import connection, transaction

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
import json
from pathlib import Path

def remove_menu(menu_id):
    """
    Remove a menu entry and its related records.

    Does not delete shared recipes or inventory items.
    Returns True if the menu entry was removed,
    or False if the menu ID does not exist.
    """
    menu_id = str(menu_id).strip()

    if not menu_id or len(menu_id) > 8:
        raise ValueError("Enter a valid menu ID.")

    with transaction.atomic():
        with connection.cursor() as cursor:
            # Lock the menu entry while checking whether it exists.
            cursor.execute(
                """
                SELECT menuID
                FROM Menu WITH (UPDLOCK, HOLDLOCK)
                WHERE menuID = %s
                """,
                [menu_id],
            )

            if cursor.fetchone() is None:
                return False

            # Remove related records before deleting the menu.
            cursor.execute(
                "DELETE FROM MenuDescription WHERE menuID = %s",
                [menu_id],
            )

            cursor.execute(
                "DELETE FROM MenuItem WHERE menuID = %s",
                [menu_id],
            )

            cursor.execute(
                "DELETE FROM Menu WHERE menuID = %s",
                [menu_id],
            )

    return True

@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def remove_menu_view(request, menu_id):
    """
    Handle a menu removal request from the website.
    """
    try:
        removed = remove_menu(menu_id)

        if removed:
            messages.success(request, "Menu item removed successfully.")
        else:
            messages.error(request, "Menu item was not found.")

    except ValueError as error:
        messages.error(request, str(error))

    except Exception:
        messages.error(request, "Unable to remove the menu item.")

    return redirect("menu_list")
    
def remove_recipe(recipe_id, file_path=None):
    """Remove a recipe from Recipes.json by its ID."""

    if file_path is None:
        file_path = Path(__file__).resolve().parent / "Recipes.json"

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    recipes = data["recipe"]

    for recipe in recipes:
        if recipe["id"] == recipe_id:
            recipes.remove(recipe)

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)

            return True

    return False