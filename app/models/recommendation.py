# Recommendation is a model representing the central information for a particular recommendation.
from flask import current_app as app
import humanize

class Recommendation:
    # Constructor
    def __init__(self, id, user_id, title, description, time_submitted, popularity):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.time_submitted = humanize.naturaltime(time_submitted)
        self.popularity = popularity
    
    # Get a recommendation, given an ID
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT id, user_id, title, description, time_submitted, popularity
            FROM Recommendations
            WHERE id = :id
            ''', id=id)
        return Recommendation(*(rows[0])) if rows else None

    # Get recommendation that contain a keyword in the title or description
    @staticmethod
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
            SELECT id, user_id, title, description, time_submitted, popularity
            FROM Recommendations
            WHERE title LIKE :modified_keyword OR description LIKE :modified_keyword
            ''', modified_keyword=modified_keyword)
        return [Recommendation(*row) for row in rows]  
      
    # Register a new recommendation
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
    
    # Update a particular recommendation
    @staticmethod
    def update(rec_id, new_title, new_description, new_time_submitted):
        try:
            rows = app.db.execute("""
            UPDATE Recommendations
            SET title=:new_title, description=:new_description,time_submitted=:new_time_submitted
            WHERE id = :rec_id""",
            new_title=new_title,
            new_description=new_description,
            new_time_submitted=new_time_submitted,
            rec_id=rec_id)
            return rows
        except Exception as e:
            print(str(e))
            return None

    # Delete a recommendation       
    @staticmethod
    def delete(rec_id):
        try:
            rows = app.db.execute("""
            DELETE FROM RecPhotos
            WHERE rec_id = :rec_id""",
            rec_id=rec_id)

            rows = app.db.execute("""
            DELETE FROM RecTags
            WHERE rec_id = :rec_id""",
            rec_id=rec_id)

            rows = app.db.execute("""
            DELETE FROM Recommendations
            WHERE id = :rec_id""",
            rec_id=rec_id)
            
            return True
        except Exception as e:
            print(str(e))
            return None
    
    @staticmethod
    def get_all(attribute='Popularity', ordering='Descending'):
        attribute_dict = {
            "Title": "title",
            "Date Posted": "time_submitted",
            "Popularity" : "popularity"
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
    
    # Modify the popularity of a particular recommendation
    @staticmethod
    def change_popularity(id, amount):
        target = Recommendation.get(id)
        new_popularity = target.popularity + amount
        app.db.execute('''
            UPDATE Recommendations
            SET popularity = :popularity
            WHERE id = :id
            ''', popularity=new_popularity,id=id)

    # Get all recommendations by a user since a given date
    @staticmethod
    def get_all_by_uid_since(user, date):
            rows = app.db.execute('''
                SELECT *
                FROM Recommendations
                WHERE user_id = :uid and time_submitted > :date
                ''', uid=user, date=date)
            return [Recommendation(*row) for row in rows]
    
    # Get all recommendations with a particular tag
    @staticmethod
    def get_all_for_tag(tag_name):
        rows = app.db.execute("""SELECT Recommendations.id, user_id, title, description, time_submitted, popularity
                              FROM Recommendations,RecTags
                              WHERE RecTags.tag_name = :tag_name AND id = rec_id""",
                              tag_name=tag_name)
        if rows == None:
            return []
        return [Recommendation(*row) for row in rows]
