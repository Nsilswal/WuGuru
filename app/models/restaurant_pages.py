from flask import current_app as app
import os

class Restaurant_page:
    def __init__(self, rid, name, rating, floor, mobile, open_time, close_time, logo, restaurant_photo, map, descript):
        self.rid = rid
        self.name = name
        self.rating = rating
        self.floor = floor
        self.mobile = mobile
        self.open_time = open_time
        self.close_time = close_time
        self.logo_photo = logo
        self.restaurant_photo = restaurant_photo
        self.map_photo = map
        self.descript = descript
    
    @staticmethod
    def get(id):
        rows = app.db.execute('''
            SELECT r.id, r.name, AVG(Reviews.rating) AS rating,
                              r.floor, r.MobileOrder, r.OpeningTime, r.ClosingTime, 
                              P.logo_photo, P.restaurant_photo, P.map_photo, P.descript
            FROM Restaurants r, Reviews, Restaurant_page P
            WHERE r.id = :id AND r.id = Reviews.restaurant_id AND r.id= P.rid
            GROUP BY r.id
            ''',
                              id = id)
        return Restaurant_page(*(rows[0])) if rows is not None else None


    
    
        
    