from flask import current_app as app

class FoodComparison:
    def __init__(self, id, food1, food2, frequency):
        self.id = id
        self.food1 = food1
        self.food2 = food2
        self.frequency = frequency

    @staticmethod
    def getTop5():
        rows = app.db.execute('''
            SELECT id, food1, food2, frequency
            FROM FoodComparisons
            ORDER BY frequency DESC
            LIMIT 5
        ''')
        return rows if rows else None
    
    @staticmethod
    def create(food1, food2, frequency):
            rows = app.db.execute("""
            INSERT INTO FoodComparisons
            (food1, food2, frequency)
            VALUES (:food1, :food2, :frequency)
            RETURNING id
            """, food1=food1, food2=food2, frequency=frequency)
            id = rows[0][0]
            return id

    @staticmethod
    def delete(id):
        try:
            app.db.execute("""
            DELETE FROM FoodComparisons
            WHERE id = :id
            """, id=id)
        except Exception as e:
            print(str(e))
    
    @staticmethod
    def add_or_increment(food1, food2):
        # First ensure food1 is > food2
        if food2 > food1:
            temp = food1
            food1 = food2
            food2 = temp
        
        # Check if the comparison already exists

        existing_comparison = app.db.execute('''
            SELECT id, frequency
            FROM FoodComparisons
            WHERE (food1 = :food1 AND food2 = :food2) OR (food1 = :food2 AND food2 = :food1)
        ''', food1=food1, food2=food2)


        if existing_comparison:
            # Increment the frequency
            updated_frequency = existing_comparison[0][1] + 1
            app.db.execute('''
                UPDATE FoodComparisons
                SET frequency = :frequency
                WHERE id = :id
            ''', id=existing_comparison[0][0], frequency=updated_frequency)
        else:
            # Add a new row with frequency 1
            FoodComparison.create(food1=food1, food2=food2, frequency=1)
        
    @staticmethod
    def search_by_keyword(keyword):
        modified_keyword = f'%{keyword}%'
        rows = app.db.execute('''
            SELECT * FROM FoodComparisons
            WHERE food1 ILIKE :modified_keyword OR food2 ILIKE :modified_keyword
            ''', modified_keyword=modified_keyword)
        return rows

    
    

