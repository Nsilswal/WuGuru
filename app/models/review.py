from flask import current_app as app

class Review:
    def __init__(self, id, firstname, lastname, date, rating, description, restaurant):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.date = date
        self.rating = rating
        self.description = description
        self.restaurant = restaurant

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.name
            FROM Reviews, Users, Restaurants
            WHERE Reviews.id = :id AND Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
            ''', id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    def create(user_id, date, rating, description, restaurant_id):
        try:
            rows = app.db.execute("""
            INSERT INTO Reviews(user_id, date, rating, description, restaurant_id)
            VALUES(:user_id, :date, :rating, :description, :restaurant_id)
            RETURNING id
            """,
            user_id=user_id,
            date=date,
            rating = rating,
            description=description,
            restaurant_id=restaurant_id)
            id = rows[0][0]
            return Review.get(id)
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    def get_all(attribute='Date', ordering='Descending'):
        attribute_dict = {
            "Date": "date",
            "Rating": "rating"
        }
        ordering_dict = {
            "Ascending": "ASC",
            "Descending" : "DESC"
        }

        if(attribute in attribute_dict and ordering in ordering_dict):
            query = f"""SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.name
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
                        ORDER BY {attribute_dict[attribute]} {ordering_dict[ordering]}"""
        else:
            query = """SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.name
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
                        ORDER BY date DESC"""

        rows = app.db.execute(query)
        
        return [Review(*row) for row in rows]
    
    @staticmethod
    def get_all_for_restaurant(restaurant_id, attribute = 'Date', ordering = 'Descending'):
        attribute_dict = {
            "Date": "date",
            "Rating": "rating"
        }
        ordering_dict = {
            "Ascending": "ASC",
            "Descending" : "DESC"
        }
        if(attribute in attribute_dict and ordering in ordering_dict):
            query = f"""SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.name
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.restaurant_id = {restaurant_id}
                        ORDER BY {attribute_dict[attribute]} {ordering_dict[ordering]}"""
        else:
            query = f"""SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.name
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.restaurant_id = {restaurant_id}
                        ORDER BY date DESC"""
        
        rows = app.db.execute(query)
        if rows == None:
            return []
        return [Review(*row) for row in rows]
    