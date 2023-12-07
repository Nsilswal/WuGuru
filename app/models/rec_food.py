# Rec_Food is a model representing food items attached within a particular recommendation.

from flask import current_app as app

class Rec_Food:
    # Constructor
    def __init__(self, rec_id, food_id):
        self.rec_id = rec_id
        self.food_id = food_id
    
    # Generate table information - each food's name and nutrition facts, as well as totals for each nutrient category
    @staticmethod
    def generate_summary_for_rec(rec_id):
        rows = app.db.execute("""
                              WITH FoodChart(rest, name, c, p, s, f) as 
                              (SELECT Restaurants.name, fooditems.name, calories, protein, sugars, fats
                              FROM RecFoods, fooditems, Restaurants
                              WHERE RecFoods.rec_id = :rec_id AND RecFoods.food_id = fooditems.id AND fooditems.restaurantID = Restaurants.id)
                              (SELECT '~', 'Meal Totals', SUM(c), SUM(p), SUM(s), SUM(f) FROM FoodChart) UNION (SELECT * FROM FoodChart)""",
                              rec_id=rec_id)
        rows.sort(key=lambda x : x[0])
        return rows
        
    # Register a list of new foods for a particular recommendation
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
        
    # Return the most attached foods (foods appearing in the most recommendations)
    @staticmethod
    def get_most_attached():
        rows = app.db.execute("""
                    SELECT *
                    FROM MostAttachedFood
                       """)
        return rows
    
    # Return the most popular foods (foods receiving the most recommendations)
    @staticmethod
    def get_most_popular():
        rows = app.db.execute("""
                    SELECT *
                    FROM MostPopularFood
                       """)
        return rows