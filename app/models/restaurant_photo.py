from flask import current_app as app
import os

class RestaurantPhotos:
    def __init__(self, rid, logo, restaurant_photo, map, descript):
        self.rid = rid
        self.logo_photo = logo
        self.restaurant_photo = restaurant_photo
        self.map_photo = map
        self.descript = descript
    
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT *
            FROM RestaurantPhotos P
            WHERE P.rid = :id
            ''',
                              id = id)
        return RestaurantPhotos(*(rows[0])) if rows is not None else None


    
    
        
    