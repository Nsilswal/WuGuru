from flask import current_app as app

class Fooditem:
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
        rows = app.db.execute('''
        SELECT id, name, protein, 
        sugars, fats, price,allergens
        FROM fooditems
        WHERE id = :id
        ''', id=id)
        return Fooditem(*(rows[0])) if rows else None

    @staticmethod
    def register(id,name,protein,sugars,fats,price,allergens):
        try:
            rows = app.db.execute("""
            INSERT INTO fooditems
            (id,name,protein,sugars,
            fats,price, allergen))
            VALUES(:id,:title,:protein,:sugars,:fats,:price,:allergens)
            RETURNING id
            """,
            id = id,
            name = name,
            protein = protein,
            sugars = sugars,
            fats = fats,
            price = price,
            allergens = allergens)
            id = rows[0][0]
            return Fooditem.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def get_all(attribute=2, ordering=0):
        attribute_list= ['name','protein','sugars','fats','price','allergens']
        #ordering_list= ['DESC','ASC']

        query = f"""SELECT *
                    FROM fooditems""" 

        # if(0 <= attribute <= 2 and 0 <= ordering <= 1):
        #     query = f"""SELECT *
        #                 FROM fooditems
        #                 ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""

        rows = app.db.execute(query)

        return [Fooditem(*row) for row in rows]
        #return query     

