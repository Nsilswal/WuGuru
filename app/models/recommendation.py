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
            title=tile,
            description=description,
            time_submitted=time_submitted,
            popularity=popularity)
            id = rows[0][0]
        except Exception as e:
            # Print error
            print(str(e))
            return None
    
    @staticmethod
    def get_all():
        rows = app.db.execute('''
        SELECT *
        FROM Recommendations
        ''')
        return [Recommendation(*row) for row in rows]
