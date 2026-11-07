
from django.db import models


class MenuCategory(models.Model):
    id = models.IntegerField(primary_key=True)
    category = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'MenuCategory'

    def __str__(self):
        return self.category


class Item(models.Model):
    itemid = models.CharField(
        db_column='itemID',
        primary_key=True,
        max_length=8
    )
    itemname = models.CharField(
        db_column='itemName',
        max_length=64
    )
    allergyinfo = models.CharField(
        db_column='allergyInfo',
        max_length=64,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'Item'

    def __str__(self):
        return self.itemname


class Menu(models.Model):
    menuid = models.CharField(
        db_column='menuID',
        primary_key=True,
        max_length=8
    )
    category = models.ForeignKey(
        MenuCategory,
        models.DO_NOTHING,
        db_column='category'
    )
    servingsize = models.CharField(
        db_column='servingSize',
        max_length=64,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'Menu'

    def __str__(self):
        return self.menuid


class Recipe(models.Model):
    recipeid = models.CharField(
        db_column='recipeID',
        primary_key=True,
        max_length=8
    )
    recipename = models.CharField(
        db_column='recipeName',
        max_length=64,
        blank=True,
        null=True
    )

    class Meta:
        managed = False
        db_table = 'Recipe'

    def __str__(self):
        return self.recipename or self.recipeid
