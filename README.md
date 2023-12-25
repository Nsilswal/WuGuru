Demo Video:
Video Outline (with timestamps):
1. Home Page and Outline – (00:00)
2. Restaurants as a Guest – (00:38)
3. Food Items as a Guest – (02:29)
4. Reviews as a Guest – (03:27)
5. Recommendations as a Guest – (05:18)
6. Cross Comparisons as a Guest – (07:15)
7. Logging In + Modifying User Data – (09:36)
8. Restaurants Attributes as Admin (User) – (10:43)
9. Restaurant Food Items as Admin (User) – (12:01)
10. Reviews as Logged In User – (13:31)
11. Recommendations as Logged In User – (15:37)
12. SQL Injection Prevention – (17:27)
Link to video:
https://youtu.be/Glc2zEvpeCE
Team Members:
Alec Liu, Mia Malden, Celina Ma, Nirvan Silswal, Jeffery Tan, Allison Taub
Summary of Progress:
Users
● Users can update all information except the id. Ensure that email is unique among all
users.
● Create administrator accounts that allow for owners of restaurants to adjust the menus of
their restaurants as well as the attributes of their restaurants.
Restaurants
● Created a unique homepage for each restaurant that includes extra information:
restaurant description, pictures, a notification for whether the restaurant is currently
open, a full menu, and all user reviews
Food Items
● Guests/users can search food items by restaurant name.
● Users (restaurant admin) can create new food items for sale and change the menu item
information (via add and delete options).
Reviews
● Summary ratings for reviews; after any query, the review page displays the resulting
number of reviews and the average rating.
● Guests/users can search reviews by keyword.
● A logged in user can update/delete reviews that they wrote (they cannot do so for
reviews other users have written). The link to this interface is in the user account view.
● Ability to leave reviews anonymously. Anonymous reviews will hide the user’s name
when displayed.
Recommendations
● Guests/users can view advanced information about a specific recommendation:
associated foods and nutritional summaries.
● Guests/users can see information about trending food items based on # of total
mentions and total popularity (w/ SQL views)
● Users can update an existing owned recommendation, inputting new fields or attaching
additional photos, food items, tags, etc.
● Users can delete an existing owned recommendation.
Cross Comparisons
● Guests/users can see a table of the top 5 most frequently compared food items, table
also maintains reciprocity (food1 vs food2 should have the same frequency as food2 vs
food1), table also updates with each comparison.
● Guests/users can generate scatter plots to visualize the relationship between two
categories.
