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
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
            SELECT id, user_id, title, description, time_submitted, popularity
            FROM Recommendations
            WHERE title LIKE :modified_keyword OR description LIKE :modified_keyword
            ''', modified_keyword=modified_keyword)
        return [Recommendation(*row) for row in rows]  
      
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
    def get_all(attribute='Trending', ordering='Descending'):
        attribute_dict = {
            "Title": "title",
            "Recent Posts": "time_submitted",
            "Trending" : "popularity"
        }
        ordering_dict = {
            "Ascending": "ASC",
            "Descending" : "DESC"
        }

        if(attribute in attribute_dict and ordering in ordering_dict):
            query = f"""SELECT *
                        FROM Recommendations
                        ORDER BY {attribute_dict[attribute]} {ordering_dict[ordering]}"""
        else:
            query = """SELECT *
                        FROM Recommendations
                        ORDER BY popularity DESC"""

        rows = app.db.execute(query)
        
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
    def get_all_by_uid_since(u, d):
            rows = app.db.execute('''
                SELECT *
                FROM Recommendations
                WHERE user_id = :uid and time_submitted > :date
                ''', uid=u, date = d)
            return [Recommendation(*row) for row in rows]
