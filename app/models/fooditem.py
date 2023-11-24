from flask import current_app as app

class Fooditem:
    def __init__(self,id,name,price,protein,sugars,fats,calories, allergens, restaurantID, diet):
        self.id=id
        self.name = name
        self.protein = protein
        self.sugars = sugars
        self.fats = fats
        self.price = price
        self.allergens = allergens
        self.restaurantID = restaurantID
        self.diet = diet
        self.calories = calories

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, name, protein, 
        sugars, fats, price,allergens,calories,restaurantID, diet
        FROM fooditems
        WHERE id = :id
        ''', id=id)
        return Fooditem(*(rows[0])) if rows else None

    @staticmethod
    def register(id,name,price,protein,sugars,fats,calories, allergens, restaurantID, diet):
        try:
            rows = app.db.execute("""
            INSERT INTO fooditems
            (id,name,protein,sugars,
            fats,price,allergens, calories,restaurantID,diet))
            VALUES(:id,:title,:protein,:sugars,:fats,:price,:allergens,:calories,:restaurantID,:diet)
            RETURNING id
            """,
            id = id,
            name = name,
            protein = protein,
            sugars = sugars,
            fats = fats,
            price = price,
            calories = calories,
            allergens = allergens,
            restaurantID = restaurantID,
            diet = diet)
            id = rows[0][0]
            return Fooditem.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
            SELECT id,name,protein,sugars,
            fats,price,allergens, calories,restaurantID,diet
            FROM fooditems
            WHERE name ILIKE :modified_keyword OR diet ILIKE :modified_keyword
            ''', modified_keyword=modified_keyword)
        return [Fooditem(*row) for row in rows] 

    @staticmethod
    def get_all(attribute=6, ordering=0):
        attribute_list= ['id','name','protein','sugars','fats','price','allergens','calories','restaurantID','diet']
        ordering_list= ['DESC','ASC']

        if(0 <= attribute <= 6 and 0 <= ordering <= 1):
            query = f"""SELECT *
                        FROM fooditems
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}""" 
        else:
            query = """SELECT *
                        FROM fooditems
                        ORDER BY name DESC"""
        # if(0 <= attribute <= 2 and 0 <= ordering <= 1):
        #     query = f"""SELECT *
        #                 FROM fooditems
        #                 ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""

        rows = app.db.execute(query)

        return [Fooditem(*row) for row in rows]
        #return query     

