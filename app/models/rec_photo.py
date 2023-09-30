from flask import current_app as app
import os

class Rec_Photo:
    def __init__(self, rec_id, filename):
        self.rec_id = rec_id
        self.filename = filename
    
    @staticmethod
    def get_all(rec_id):
        rows = app.db.execute("""SELECT *
                              FROM RecPhotos
                              WHERE rec_id = :rec_id""",
                              rec_id=rec_id)
        if rows == None:
            return []
        return [Rec_Photo(*row) for row in rows]
    
    @staticmethod
    def register(rec_id, photo):
        filename = photo.filename
        try:
            if filename:
                target_directory = 'photos'  
                if not os.path.exists(target_directory):
                    os.makedirs(target_directory)

                file_path = os.path.join(target_directory, filename)
                photo.save(file_path)

                rows = app.db.execute("""
                INSERT INTO RecPhotos
                VALUES(:rec_id, :filename)
                """,
                rec_id=rec_id,
                filename=filename)
        except Exception as e:
            # Print error
            print(str(e))
            return None
        
    