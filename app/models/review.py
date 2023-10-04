from flask import current_app as app

class Review:
    def __init__(self, id, firstname, lastname, date, rating, description):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.date = date
        self.rating = rating
        self.description = description

    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, user_id, date, rating, description
            FROM Reviews
            WHERE id = :id
            ''', id=id)
        return Review(*(rows[0])) if rows else None

    @staticmethod
    def register(user_id, date, rating, description):
        try:
            rows = app.db.execute("""
            INSERT INTO Reviews(user_id, date, rating, description)
            VALUES(:user_id, :date, :rating, :description)
            RETURNING id
            """,
            user_id=user_id,
            date=date,
            rating = rating,
            description=description)
            id = rows[0][0]
            return Review.get(id)
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    def get_all(attribute=0, ordering=0):
        # Attribute: 0 - date, 1 - rating
        # Ordering: 0 - DESC, 1 - ASC
        attribute_list = ['date', 'rating']
        ordering_list = ['DESC', 'ASC']

        if(0 <= attribute <= 1 and 0 <= ordering <= 1):
            query = f"""SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description
                        FROM Reviews, Users
                        WHERE Reviews.user_id = Users.id
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""
        else:
            query = """SELECT Reviews.id, Users.firstname, Users.lastname, Reviews.date, Reviews.rating, Reviews.description
                        FROM Reviews, Users
                        WHERE Reviews.user_id = Users.id
                        ORDER BY date DESC"""

        rows = app.db.execute(query)
        
        return [Review(*row) for row in rows]
    