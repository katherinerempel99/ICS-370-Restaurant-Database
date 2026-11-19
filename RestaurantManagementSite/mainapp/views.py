
from decimal import Decimal, InvalidOperation
import json

from django.contrib import messages
from django.db import connection, transaction
from django.shortcuts import render, redirect

from .models import Item, Store

from pathlib import Path


# Home page
def home(request):
    return render(request, "home.html")


# Recipe details page
def recipe_detail(request):
    json_path = Path(__file__).resolve().parent / "Recipes.json"

    with open(json_path, encoding="utf-8") as json_file:
        data = json.load(json_file)

    recipes = data["recipe"]
    context = {"recipes": recipes}

    return render(request, "recipe.html", context)


# Inventory Management page
def inventory_list(request):

    # Handle Add Inventory form submissions
    if request.method == "POST":

        # Handle Delete Inventory submissions
        if request.POST.get("action") == "delete":
            item_id = request.POST.get("itemID", "").strip()
            store_id = request.POST.get("storeID", "").strip()

            try:
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        # Lock matching records while checking for duplicates.
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM Inventory WITH (TABLOCKX, HOLDLOCK)
                            WHERE itemID = %s AND storeID = %s
                            """,
                            [item_id, store_id]
                        )

                        record_count = cursor.fetchone()[0]

                        if record_count != 1:
                            messages.error(
                                request,
                                "Delete canceled: expected exactly one matching inventory record."
                            )
                            return redirect("inventory_list")

                        cursor.execute(
                            """
                            DELETE FROM Inventory
                            WHERE itemID = %s AND storeID = %s
                            """,
                            [item_id, store_id]
                        )

                messages.success(
                    request,
                    "Inventory record deleted successfully."
                )

            except Exception:
                messages.error(
                    request,
                    "Unable to delete inventory. Please try again."
                )

            return redirect("inventory_list")


        item_id = request.POST.get("itemID", "").strip()
        store_id = request.POST.get("storeID", "").strip()
        quantity_text = request.POST.get("quantity", "").strip()

        # Validate selected item
        if not Item.objects.filter(itemid=item_id).exists():
            messages.error(
                request,
                "Please select a valid item."
            )
            return redirect("inventory_list")

        # Validate selected store
        if not Store.objects.filter(storeid=store_id).exists():
            messages.error(
                request,
                "Please select a valid store."
            )
            return redirect("inventory_list")

        # Validate quantity
        try:
            quantity = Decimal(quantity_text)

        except InvalidOperation:
            messages.error(
                request,
                "Please enter a valid quantity."
            )
            return redirect("inventory_list")

        if (
            not quantity.is_finite()
            or quantity < 0
            or quantity > Decimal("999999.99")
            or quantity.as_tuple().exponent < -2
        ):
            messages.error(
                request,
                "Quantity must be between 0 and 999999.99 "
                "with at most two decimal places."
            )
            return redirect("inventory_list")

        # Handle Update Inventory submissions
        if request.POST.get("action") == "update":
            try:
                with transaction.atomic():
                    with connection.cursor() as cursor:
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM Inventory WITH (TABLOCKX, HOLDLOCK)
                            WHERE itemID = %s AND storeID = %s
                            """,
                            [item_id, store_id]
                        )

                        record_count = cursor.fetchone()[0]

                        if record_count != 1:
                            messages.error(
                                request,
                                "Inventory update canceled: expected exactly one matching record."
                            )
                            return redirect("inventory_list")
                        cursor.execute(
                            """
                            UPDATE Inventory
                            SET quantity = %s
                            WHERE itemID = %s AND storeID = %s
                            """,
                            [quantity, item_id, store_id]
                        )

                        updated_count = cursor.rowcount

                if updated_count == 1:
                    messages.success(
                        request,
                        "Inventory quantity updated successfully."
                    )
                elif updated_count == 0:
                    messages.error(
                        request,
                        "Inventory record not found."
                    )
                else:
                    messages.error(
                        request,
                        "Multiple inventory records were updated. "
                        "Please contact an administrator."
                    )

            except Exception:
                messages.error(
                    request,
                    "Unable to update inventory. Please try again."
                )

            return redirect("inventory_list")

        # Check for duplicates and insert inventory
        try:
            with transaction.atomic():

                with connection.cursor() as cursor:

                    # Lock the table during the duplicate check
                    # and insert to prevent concurrent duplicates.
                    cursor.execute(
                        """
                        SELECT COUNT(*)
                        FROM Inventory WITH (TABLOCKX, HOLDLOCK)
                        WHERE itemID = %s AND storeID = %s
                        """,
                        [item_id, store_id]
                    )

                    existing_count = cursor.fetchone()[0]

                    if existing_count > 0:
                        messages.error(
                            request,
                            "This item already has an inventory "
                            "record at the selected store."
                        )
                        return redirect("inventory_list")

                    # Insert the new inventory record
                    cursor.execute(
                        """
                        INSERT INTO Inventory
                            (itemID, storeID, quantity)
                        VALUES (%s, %s, %s)
                        """,
                        [item_id, store_id, quantity]
                    )

            messages.success(
                request,
                "Inventory added successfully."
            )

        except Exception:
            messages.error(
                request,
                "Unable to save inventory. Please try again."
            )

        return redirect("inventory_list")

    # Retrieve available items and stores
    items = Item.objects.all().order_by("itemname")
    stores = Store.objects.all().order_by("storeid")

    # Retrieve current inventory records
    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT
                i.itemID,
                it.itemName,
                i.storeID,
                s.address,
                i.quantity
            FROM Inventory AS i
            INNER JOIN Item AS it
                ON i.itemID = it.itemID
            INNER JOIN Store AS s
                ON i.storeID = s.storeID
            ORDER BY s.storeID, it.itemName
            """
        )

        columns = [col[0] for col in cursor.description]

        inventory_records = [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    context = {
        "items": items,
        "stores": stores,
        "inventory_records": inventory_records,
    }

    return render(request, "inventory.html", context)
