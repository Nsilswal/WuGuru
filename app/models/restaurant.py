from flask import current_app as app
from datetime import datetime, time


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
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime,
                              r.ownedBY
            FROM Restaurants r, Reviews
            WHERE r.id = :id AND r.id = Reviews.restaurant_id
            GROUP BY r.id
            ''',
                              id = id)
        return Restaurants(*(rows[0])) if rows is not None else None
    
    @staticmethod
    def register(id, name, floor, MobileOrder, OpeningTime, ClosingTime, OwnedBY):
        try:
            rows = app.db.execute("""
            INSERT INTO Restaurants
            (id, name, floor, MobileOrder, OpeningTime, ClosingTime, OwnedBY))
            VALUES(:id,:name,:floor,:MobileOrder,:OpeningTime,:ClosingTime,:OwnedBY)
            RETURNING id
            """,
            id = id,
            name = name,
            floor = floor,
            MobileOrder = MobileOrder,
            OpeningTime = OpeningTime,
            ClosingTime = ClosingTime,
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
        attribute_list = ['id', 'name', 'rating', 'floor', 'MobileOrder', 'OpeningTime', 'ClosingTime', 'ownedBY']
        ordering_list = ['ASC', 'DESC']

        if(0 <= attribute <= 6 and 0 <= ordering <= 1):
            query = f"""SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime, r.ownedBY
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]},
                        name ASC"""
        else:
            query = """SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime, r.ownedBY
                        FROM Restaurants r, Reviews
                        WHERE r.id = Reviews.restaurant_id
                        GROUP BY r.id
                        ORDER BY name ASC"""

        rows = app.db.execute(query)

        
        return [Restaurants(*row) for row in rows]

    @staticmethod
    def get_if_open(id, current_time):
        current_time_time = current_time.time()
        query = '''
            SELECT *
            FROM Restaurants r
            WHERE r.id = :id AND :current_time >= r.OpeningTime AND :current_time <= r.ClosingTime
        '''

        rows = app.db.execute(query, current_time=current_time_time, id=id)

        if rows:
            return True  # The restaurant is open
        else:
            return False  # The restaurant is closed
   

    @staticmethod
    def changeFloor(rest, newFloor):
        app.db.execute('''
            UPDATE Restaurants
            SET floor = :floor
            WHERE id = :id
            ''', floor= newFloor,id=rest)
    @staticmethod
    def changeOpenTime(rest, newOpenTime):
        app.db.execute('''
            UPDATE Restaurants
            SET OpeningTime = :OpenTime
            WHERE id = :id
            ''', OpenTime= newOpenTime,id=rest)
    @staticmethod
    def changeCloseTime(rest, newCloseTime):
        app.db.execute('''
            UPDATE Restaurants
            SET ClosingTime = :CloseTime
            WHERE id = :id
            ''', CloseTime= newCloseTime,id=rest)
    @staticmethod
    def changeMobileOrder(rest, newMO):
        app.db.execute('''
            UPDATE Restaurants
            SET MobileOrder = :MobileOrder
            WHERE id = :id
            ''', MobileOrder= newMO,id=rest)
            
    @staticmethod
    def edit(floor, mo, open, close, id):
        if (mo == 1):
            mobor = True
        else:
            mobor = False
        Restaurants.changeFloor(id, floor)
        Restaurants.changeMobileOrder(id, mobor)
        Restaurants.changeOpenTime(id, open)
        Restaurants.changeCloseTime(id, close)
        return True

 
   
