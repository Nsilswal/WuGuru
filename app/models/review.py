from flask import current_app as app

class Review:
    def __init__(self, id, user_id, firstname, lastname, date, rating, description, restaurant_id, restaurant, anonymous):
        self.id = id
        self.user_id = user_id
        self.firstname = firstname
        self.lastname = lastname
        self.date = date
        self.rating = rating
        self.description = description
        self.restaurant_id = restaurant_id
        self.restaurant = restaurant
        self.anonymous = anonymous

    @staticmethod
    # get Review with id
    def get(id):
        rows = app.db.execute('''
            SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
            FROM Reviews, Users, Restaurants
            WHERE Reviews.id = :id AND Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
            ''', id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    # create new Review
    def create(user_id, date, rating, description, restaurant_id, anonymous):
        try:
            rows = app.db.execute("""
            INSERT INTO Reviews(user_id, date, rating, description, restaurant_id, anonymous)
            VALUES(:user_id, :date, :rating, :description, :restaurant_id, :anonymous)
            RETURNING id
            """,
            user_id=user_id,
            date=date,
            rating = rating,
            description=description,
            restaurant_id=restaurant_id,
            anonymous=anonymous)
            id = rows[0][0]
            return Review.get(id)
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    # update existing Review date, rating, description, restaurant, and/or whether it is anonymous
    def update(review_id, date, rating, description, restaurant_id, anonymous):
        try:
            app.db.execute("""
            UPDATE Reviews 
            SET date = :date, rating = :rating, description = :description, restaurant_id = :restaurant_id, anonymous = :anonymous
            WHERE Reviews.id = :review_id
            """,
            review_id=review_id,
            date=date,
            rating = rating,
            description=description,
            restaurant_id=restaurant_id,
            anonymous=anonymous)
            return Review.get(review_id)
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    # delete existing Review with id = review_id
    def delete(review_id):
        try:
            rows = app.db.execute("""
            DELETE FROM Reviews
            WHERE Reviews.id = :review_id
            """,
            review_id=review_id)
        except Exception as e:
            # Print error
            print(str(e))
    
    @staticmethod
    # get all Reviews in database, if there are sort parameters order the rows accordingly, else default to sorting by date descending
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
            query = f"""SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
                        ORDER BY {attribute_dict[attribute]} {ordering_dict[ordering]}"""
        else:
            query = """SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id
                        ORDER BY date DESC"""

        rows = app.db.execute(query)
        
        return [Review(*row) for row in rows]
    
    @staticmethod
    # get all Reviews for a certain restaurant in the database, if there are sort parameters order the rows accordingly, else default to sorting by date descending
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
            query = f"""SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.restaurant_id = {restaurant_id}
                        ORDER BY {attribute_dict[attribute]} {ordering_dict[ordering]}"""
        else:
            query = f"""SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.restaurant_id = {restaurant_id}
                        ORDER BY date DESC"""
        
        rows = app.db.execute(query)
        if rows == None:
            return []
        return [Review(*row) for row in rows]

    @staticmethod
    # get all Reviews were the description contains keyword, sorted by date descending
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
                        SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
                        FROM Reviews, Users, Restaurants
                        WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.description LIKE :modified_keyword
                        ORDER BY date DESC
            ''', modified_keyword=modified_keyword)
        return [Review(*row) for row in rows]  
    
    @staticmethod
    # get all Reviews written by user with id = u since date = d, sorted by date descending
    def get_all_by_uid_since(u, d):
        rows = app.db.execute('''
            SELECT Reviews.id, Users.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description, Restaurants.id, Restaurants.name, Reviews.anonymous
            FROM Reviews, Users, Restaurants
            WHERE Reviews.user_id = Users.id AND Reviews.restaurant_id = Restaurants.id AND Reviews.user_id = :uid AND Reviews.date >= :date
            ORDER BY date DESC
            ''', uid=u, date=d)
        return [Review(*row) for row in rows]
