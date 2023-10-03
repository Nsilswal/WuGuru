from flask import current_app as app

class Recommendation:
    def __init__(self, id, user_id, title, description, time_submitted, popularity):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.time_submitted = time_submitted
        self.popularity = popularity
    
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, user_id, title, description, time_submitted, popularity
            FROM Recommendations
            WHERE id = :id
            ''', id=id)
        return Recommendation(*(rows[0])) if rows else None

    @staticmethod
    def register(user_id, title, description, time_submitted, popularity):
        try:
            rows = app.db.execute("""
            INSERT INTO Recommendations(user_id, title, description, time_submitted, popularity)
            VALUES(:user_id, :title, :description, :time_submitted, :popularity)
            RETURNING id
            """,
            user_id=user_id,
            title=title,
            description=description,
            time_submitted=time_submitted,
            popularity=popularity)
            id = rows[0][0]
            return Recommendation.get(id)
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    def get_all(attribute=2, ordering=0):
        # Attribute: 0 - title, 1 - time_submitted, 2 - popularity
        # Ordering: 0 - DESC, 1 - ASC
        attribute_list = ['title', 'time_submitted', 'popularity']
        ordering_list = ['DESC', 'ASC']

        if(0 <= attribute <= 2 and 0 <= ordering <= 1):
            query = f"""SELECT *
                        FROM Recommendations
                        ORDER BY {attribute_list[attribute]} {ordering_list[ordering]}"""
        else:
            query = """SELECT *
                        FROM Recommendations
                        ORDER BY popularity DESC"""

        rows = app.db.execute(query)

        # rows = app.db.execute('''
        # SELECT *
        # FROM Recommendations
        # ORDER BY :attribute :ordering
        # ''',attribute=attribute, ordering=ordering)
        
        return [Recommendation(*row) for row in rows]
    
    @staticmethod
    def change_popularity(id, amount):
        target = Recommendation.get(id)
        new_popularity = target.popularity + amount
        app.db.execute('''
            UPDATE Recommendations
            SET popularity = :popularity
            WHERE id = :id
            ''', popularity=new_popularity,id=id)

    @staticmethod
    def get_all_by_uid_since(uid, date):
            rows = app.db.execute('''
                SELECT id, user_id, title, description, time_submitted, popularity
                FROM Recommendations
                WHERE id = :uid and time_submitted > :date
                ''', uid=uid, date = date)
            return Recommendation(*(rows)) if rows else None
