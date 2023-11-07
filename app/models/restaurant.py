from flask import current_app as app


class Restaurants:
    def __init__(self, id, name, rating, floor, MobileOrder, OpeningTime, ClosingTime):
        self.id = id
        self.name = name
        self.rating = rating
        self.floor = floor
        self.MobileOrder = MobileOrder
        self.OpeningTime = OpeningTime
        self.ClosingTime = ClosingTime

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
    def register(id, name, floor, MobileOrder, OpeningTime, ClosingTime):
        try:
            rows = app.db.execute("""
            INSERT INTO Restaurants
            (id, name, floor, MobileOrder, OpeningTime, ClosingTime))
            VALUES(:id,:name,:floor,:MobileOrder,:OpeningTime,:ClosingTime)
            RETURNING id
            """,
            id = id,
            name = name,
            floor = floor,
            MobileOrder = MobileOrder,
            OpeningTime = OpeningTime,
            ClosingTime = ClosingTime)
            id = rows[0][0]
            return Restaurants.get(id)
        except Exception as e:
            print(str(e))
            return None
        

    @staticmethod
    def get_all(attribute=1, ordering=0):
        # Attribute: 0 - id, 1-name, 2 - rating, 3-floor, 4 - Mobile, 5-Open, 6-Close
        # Ordering: 0 - ASC, 1 - DESC
        attribute_list = ['id', 'name', 'rating', 'floor', 'MobileOrder', 'OpeningTime', 'ClosingTime']
        ordering_list = ['ASC', 'DESC']

        if(0 <= attribute <= 6 and 0 <= ordering <= 1):
            query = f"""SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""
        else:
            query = """SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY name DESC"""

        rows = app.db.execute(query)

        
        return [Restaurants(*row) for row in rows]
    
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
    
    def get_rating(id):
        rows = app.db.execute('''
            SELECT
                r.id,
                AVG(Reviews.rating)
            FROM
                Restaurants r
            LEFT JOIN
                Reviews
            ON
                r.id = Reviews.restaurant_ID
            WHERE r.id = :id
            ''',
                              id=id)
        return [Restaurants(*row) for row in rows]
 
   
