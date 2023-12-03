from flask import current_app as app

class Fooditem:
    def __init__(self,id,name,price,protein,sugars,fats,calories, allergens, restaurantID, diet, rname='test'):
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
        self.rname = rname

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
            SELECT * FROM 
                (SELECT fooditems.id, fooditems.name, 
                        fooditems.protein, fooditems.sugars, fooditems.fats, 
                        fooditems.price, fooditems.allergens, 
                        fooditems.calories, fooditems.restaurantID, fooditems.diet, r.name as rname
                FROM fooditems
                JOIN Restaurants r
                ON r.id = fooditems.restaurantID) AS H
            WHERE H.name ILIKE :modified_keyword OR H.diet ILIKE :modified_keyword OR H.rname ILIKE :modified_keyword
            
            ''', modified_keyword=modified_keyword)
        return [Fooditem(*row) for row in rows] 

    @staticmethod
    def get_all(attribute=6, ordering=0):
        attribute_list= ['id','name','protein','sugars','fats','price','allergens','calories','restaurantID','diet']
        ordering_list= ['DESC','ASC']

        if(0 <= attribute <= 6 and 0 <= ordering <= 1):
            query = f"""SELECT 
                        fooditems.id, fooditems.name, 
                        fooditems.protein, fooditems.sugars, fooditems.fats, 
                        fooditems.price, fooditems.allergens, 
                        fooditems.calories, fooditems.restaurantID, fooditems.diet, r.name AS rname
                    FROM 
                        fooditems
                    JOIN
                        Restaurants r
                    ON
                        r.id = fooditems.restaurantID
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}""" 
        else:
            query = f"""SELECT 
                        fooditems.id, fooditems.name, 
                        fooditems.protein, fooditems.sugars, fooditems.fats, 
                        fooditems.price, fooditems.allergens, 
                        fooditems.calories, fooditems.restaurantID, fooditems.diet, r.name AS rname
                    FROM 
                        fooditems
                    JOIN
                        Restaurants r
                    ON
                        r.id = fooditems.restaurantID
                        ORDER BY name DESC"""
        # if(0 <= attribute <= 2 and 0 <= ordering <= 1):
        #     query = f"""SELECT *
        #                 FROM fooditems
        #                 ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""

        rows = app.db.execute(query)

        return [Fooditem(*row) for row in rows]
        #return query    
    
    @staticmethod
    def update_fi(id,name,protein,sugars,fats,price,calories,allergens, diet):
        try:
            app.db.execute("""
            UPDATE fooditems 
            SET name = :name, protein = :protein, sugars = :sugars, fats = :fats, price = :price, allergens = :allergnes, calories = :calories, diet = :diet
            WHERE fooditems.id = :id
            """,
            id = id,
            name = name,
            protein = protein,
            sugars = sugars,
            fats = fats,
            price = price,
            calories = calories,
            allergens = allergens,
            diet = diet)
            return Fooditem.get(id)
        except Exception as e:
            # Print error
            print(str(e))
            return None

    @staticmethod
    def generate_full_pairings():
        results = app.db.execute("""
                SELECT fooditems.id, fooditems.name, Restaurants.name
                FROM fooditems, Restaurants
                WHERE fooditems.restaurantID = Restaurants.id""") 
        pairings = [(f'{item[0]}', f'{item[2]}: {item[1]}') for item in results]
        return pairings
        