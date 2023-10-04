from flask import current_app as app


class Purchase:
    def __init__(self, id, uid, pid, time_purchased):
        self.id = id
        self.uid = uid
        self.pid = pid
        self.time_purchased = time_purchased

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, uid, pid, time_purchased
FROM Purchases
WHERE id = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(u, s):
        rows = app.db.execute('''
SELECT *
FROM Purchases
WHERE user_id = :uid
AND time_purchased >= :since
''',
                              uid=u,
                              since=s)
        return [Purchase(*row) for row in rows]
