-- Feel free to modify this file to match your development goal.
-- Here we only create 3 tables for demo purpose.

CREATE TABLE Users (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL
);

CREATE TABLE Restaurants (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) NOT NULL,
    floor INT,
    MobileOrder BOOLEAN,
    OpeningTime TIME,
    ClosingTime TIME,
    OwnID INT NOT NULL
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

CREATE TABLE Recommendations (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    time_submitted timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
    popularity INT NOT NULL
);

CREATE TABLE RecPhotos (
    rec_id INT NOT NULL REFERENCES Recommendations(id),
    filename VARCHAR(100) NOT NULL,
    PRIMARY KEY(rec_id, filename)
);

CREATE TABLE RecTags (
    rec_id INT NOT NULL REFERENCES Recommendations(id),
    tag_name VARCHAR(100) NOT NULL
);

CREATE TABLE fooditems (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    sugars FLOAT NOT NULL,
    fats FLOAT NOT NULL,
    calories INT NOT NULL,
    allergens VARCHAR(50) NOT NULL,
    restaurantID INT NOT NULL,
    diet VARCHAR(100)
);

CREATE TABLE Reviews (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    user_id INT NOT NULL REFERENCES Users(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    rating INT NOT NULL,
    description VARCHAR(300) NOT NULL,
    restaurant_id INT NOT NULL REFERENCES Restaurants(id)
);