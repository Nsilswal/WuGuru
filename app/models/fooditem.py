from flask import current_app as app

class Fooditem:
    def __init__(self,id,name,price,protein,sugars,fats,calories, allergens, restaurantID, diet, rname='test'):
        self.id=id
        self.name = name
        self.price = price
        self.protein = protein
        self.sugars = sugars
        self.fats = fats
        self.allergens = allergens
        self.restaurantID = restaurantID
        self.diet = diet
        self.calories = calories
        self.rname = rname

    @staticmethod
    def get(id):
        rows = app.db.execute('''
        SELECT id, name, price protein, 
        sugars, fats, allergens,calories,restaurantID, diet
        FROM fooditems
        WHERE id = :id
        ''', id=id)
        return Fooditem(*(rows[0])) if rows else None

    @staticmethod #to add food item to database
    def register(name,fats,protein,sugars,price,calories, allergens, restaurantID, diet):
        try:
            rows = app.db.execute("""
            INSERT INTO fooditems
            (name,price,protein,sugars,
            fats,allergens, calories,restaurantID,diet)
            VALUES(:name,:price,:protein,:sugars,:fats,:allergens,:calories,:restaurantID,:diet)
            RETURNING id
            """,
            name = name,
            price = price,
            protein = protein,
            sugars = sugars,
            fats = fats,
            calories = calories,
            allergens = allergens,
            restaurantID = restaurantID,
            diet = diet)
            id = rows[0][0]
            return Fooditem.get(id)
        except Exception as e:
            print(str(e))
            return None

    @staticmethod #remove food item from database -> can only process if user is logged in & they are an admin of the restaurant whose food they want to remove
    def delete_fi(name,restaurantID):
        try:
            rows = app.db.execute("""
            DELETE FROM fooditems
            WHERE name = :name AND restaurantID = :restaurantID
            """,
            name = name,
            restaurantID = restaurantID)
        except Exception as e:
            # Print error
            print(str(e))

    @staticmethod #search method, joining fooditems with restaurants to get restaurantID displayed as restaurant name
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
            SELECT * FROM 
                (SELECT fooditems.id, fooditems.name, fooditems.price,
                        fooditems.protein, fooditems.sugars, fooditems.fats, 
                        fooditems.allergens, 
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
                        fooditems.id, fooditems.name, fooditems.price,
                        fooditems.protein, fooditems.sugars, fooditems.fats, 
                        fooditems.allergens, 
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
    
    @staticmethod #method not in use
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
        