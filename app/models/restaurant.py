from flask import current_app as app


class Restaurants:
    def __init__(self, id, name, floor, MobileOrder, OpeningTime, ClosingTime):
        self.id = id
        self.name = name
        self.floor = floor
        self.MobileOrder = MobileOrder
        self.OpeningTime = OpeningTime
        self.ClosingTime = ClosingTime

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, name, floor, MobileOrder, OpeningTime, ClosingTime
            FROM Restaurants
            WHERE id = :id
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
        # Attribute: 0 - id, 1-name, 2 - floor, 3 - Mobile, 4-Open, 5-Close
        # Ordering: 0 - ASC, 1 - DESC
        attribute_list = ['id', 'name', 'floor', 'MobileOrder', 'OpeningTime', 'ClosingTime']
        ordering_list = ['ASC', 'DESC']

        if(0 <= attribute <= 5 and 0 <= ordering <= 1):
            query = f"""SELECT *
                        FROM Restaurants
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""
        else:
            query = """SELECT *
                        FROM Restaurants
                        ORDER BY name DESC"""

        rows = app.db.execute(query)

        
        return [Restaurants(*row) for row in rows]
    

    @staticmethod
    def get_menu(id):
        rows = app.db.execute('''
            SELECT
                r.name AS restaurant_name,
                f.name AS food_item_name,
                f.price
            FROM
                Restaurants r
            INNER JOIN
                Sells s
            ON
                r.id = s.rid
            INNER JOIN
                fooditems f
            ON
                s.fid = f.id;
            WHERE r.id = :id
            ''',
                              id=id)
        return [Restaurants(*row) for row in rows]
