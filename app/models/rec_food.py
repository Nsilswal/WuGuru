from flask import current_app as app

class Rec_Food:
    def __init__(self, rec_id, food_id):
        self.rec_id = rec_id
        self.food_id = food_id
    
    @staticmethod
    def get_all_names_for_entry(rec_id):
        rows = app.db.execute("""SELECT fooditems.name, Restaurants.name
                              FROM RecFoods, fooditems, Restaurants
                              WHERE RecFoods.rec_id = :rec_id AND RecFoods.food_id = fooditems.id AND fooditems.restaurantID = Restaurants.id""",
                              rec_id=rec_id)
        if len(rows) == 0:
            return ['None Attached']
        foods = [f'{item[0]} from {item[1]}' for item in rows]
        return foods
    
    @staticmethod
    def register(rec_id, food_ids):
        try:
            for food in food_ids:
                rows = app.db.execute("""
                INSERT INTO RecFoods
                VALUES(:rec_id, :food_id)
                """,
                rec_id=rec_id,
                food_id=food)
        except Exception as e:
            # Print error
            print(str(e))
            return None
        
    