\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

\COPY Recommendations FROM 'Recommendations.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.recommendations_id_seq',
                            (SELECT MAX(id)+1 FROM Recommendations),
                            false);
                            
\COPY RecPhotos FROM 'RecPhotos.csv' WITH DELIMITER ',' NULL '' CSV
\COPY RecTags FROM 'RecTags.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Restaurants FROM 'Restaurants.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.restaurants_id_seq',
                         (SELECT MAX(id)+1 FROM Restaurants),
                         false);

\COPY Reviews FROM 'Reviews.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.reviews_id_seq',
                         (SELECT MAX(id)+1 FROM Reviews),
                         false);     

\COPY fooditems FROM 'fooditems.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.fooditems_id_seq',
                         (SELECT MAX(id)+1 FROM fooditems),
                         false); 

\COPY RecFoods FROM 'RecFoods.csv' WITH DELIMITER ',' NULL '' CSV