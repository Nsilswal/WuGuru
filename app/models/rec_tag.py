from flask import current_app as app
import os

class Rec_Tag:
    def __init__(self, rec_id, tag_name):
        self.rec_id = rec_id
        self.tag_name = tag_name
    
    @staticmethod
    def get_all_for_entry(rec_id):
        rows = app.db.execute("""SELECT *
                              FROM RecTags
                              WHERE rec_id = :rec_id""",
                              rec_id=rec_id)
        if rows == None:
            return []
        return [Rec_Tag(*row) for row in rows]
    
    @staticmethod
    def register(rec_id, tags):
        try:
            for tag_name in tags:
                rows = app.db.execute("""
                INSERT INTO RecTags
                VALUES(:rec_id, :tag_name)
                """,
                rec_id=rec_id,
                tag_name=tag_name)
        except Exception as e:
            # Print error
            print(str(e))
            return None
        
    