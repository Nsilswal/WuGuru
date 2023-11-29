from flask import current_app as app
from datetime import datetime

class Restaurants:
    def __init__(self, id, name, rating, floor, MobileOrder, OpeningTime, ClosingTime,OwnedBy):
        self.id = id
        self.name = name
        self.rating = rating
        self.floor = floor
        self.MobileOrder = MobileOrder
        self.OpeningTime = OpeningTime
        self.ClosingTime = ClosingTime
        self.ownedBY = OwnedBy

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime
            FROM Restaurants r, Reviews
            WHERE r.id = :id AND r.id = Reviews.restaurant_id
            GROUP BY r.id
            ''',
                              id = id)
        return Restaurants(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def register(id, name, floor, MobileOrder, OpeningTime, ClosingTime, OwnID, OwnedBY):
        try:
            rows = app.db.execute("""
            INSERT INTO Restaurants
            (id, name, floor, MobileOrder, OpeningTime, ClosingTime, OwnID, OwnedBY))
            VALUES(:id,:name,:floor,:MobileOrder,:OpeningTime,:ClosingTime,:OwnID, :OwnedBY)
            RETURNING id
            """,
            id = id,
            name = name,
            floor = floor,
            MobileOrder = MobileOrder,
            OpeningTime = OpeningTime,
            ClosingTime = ClosingTime,
            OwnID = OwnID,
            OwnedBY = OwnedBY)
            id = rows[0][0]
            return Restaurants.get(id)
        except Exception as e:
            print(str(e))
            return None
        

    @staticmethod
    def get_all(attribute=1, ordering=0):
        # Attribute: 0 - id, 1-name, 2 - rating, 3-floor, 4 - Mobile, 5-Open, 6-Close, 7-OwnID, 8-ownedBY
        # Ordering: 0 - ASC, 1 - DESC
        attribute_list = ['id', 'name', 'rating', 'floor', 'MobileOrder', 'OpeningTime', 'ClosingTime', 'OwnID', 'ownedBY']
        ordering_list = ['ASC', 'DESC']

        if(0 <= attribute <= 6 and 0 <= ordering <= 1):
            query = f"""SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime, r.OwnID, r.ownedBY
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]},
                        rating DESC"""
        else:
            query = """SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime, r.OwnID, r.ownedBY
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY name ASC"""

        rows = app.db.execute(query)

        
        return [Restaurants(*row) for row in rows]

    @staticmethod
    def get_open_restaurants():
        current_time = datetime.now().strftime('%H:%M:%S')
        
        query = '''
            SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                   r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime
            FROM Restaurants r, Reviews
            WHERE r.id = Reviews.restaurant_id
            GROUP BY r.id
            HAVING :current_time >= r.OpeningTime AND :current_time <= r.ClosingTime
        '''

        rows = app.db.execute(query, current_time=current_time)

        return [Restaurants(*row) for row in rows]
    '''
    def format_time(time_string):
        try:
            time_obj = datetime.strptime(time_string, '%H:%M:%S')
            return time_obj.strftime('%H:%M')
        except ValueError:
            return time_string

    app.jinja_env.filters['format_time'] = format_time
    
    '''
    

    #Instead of get menu, link to a filter of food items done by Mia
    @staticmethod
    def get_menu(id):
        rows = app.db.execute('''
            SELECT
                r.id as restaurant_id,
                r.name AS restaurant_name,
                f.name AS food_item_name,
                f.price
            FROM
                Restaurants r
            LEFT JOIN
                fooditems f
            ON
                r.id = s.restaurantID
            WHERE r.id = :id
            ''',
                              id=id)
        return [Restaurants(*row) for row in rows]
    
    def get_reviews(id):
        rows = app.db.execute('''
            SELECT
                r.name AS restaurant_name,
                rev.rating AS food_item_name,
                rev.description
            FROM
                Restaurants r
            LEFT JOIN
                Reviews rev
            ON
                r.id = rev.restaurant_ID
            WHERE r.id = :id
            ''',
                              id=id)
        return [Restaurants(*row) for row in rows]
    

 
   
