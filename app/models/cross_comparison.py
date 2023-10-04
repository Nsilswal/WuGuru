from flask import current_app as app


class CrossComparison:
    def __init__(self,id,name,protein,sugars,fats,price,allergens):
        self.id=id
        self.name = name
        self.protein = protein
        self.sugars = sugars
        self.fats = fats
        self.price = price
        self.allergens = allergens

    @staticmethod
    def get(id):
        return "returned get static method in cross_comparison.py"
        # rows = app.db.execute('''
        # SELECT id, name, protein, 
        # sugars, fats, price,allergens
        # FROM fooditems
        # WHERE id = :id
        # ''', id=id)
        # return Fooditem(*(rows[0])) if rows else None

