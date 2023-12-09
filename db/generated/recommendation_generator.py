# The recommendation_generator file is a collection of utility functions to generate data for recommendations.
import random
import csv

# Generate a random date
def generate_date():
    # Generate random values for year, month, day, hour, minute, and second
    year = random.randint(2023, 2023)  # Set the desired year
    month = random.randint(1, 10)
    day = random.randint(1, 28)  # Be aware of valid day values for each month
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    # Format the random values as a date-time string
    date_time_str = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    return date_time_str

# Generate a placeholder with a random date and popularity
def generate_recommendations():
    for i in range(96, 1050):
        id = i
        user_id = random.randint(1, 99)
        title = f'Sample Title {i}'
        description = f'Sample Description'
        date = generate_date()
        popularity = random.randint(1, 30)
        row = f'{id},{user_id},{title},{description},{date},{popularity}'
        print(row)
    
# Generate random tags associated with recommendations
def generate_tags():
    for i in range(1, 1000):
        id = i
        chance = random.random()
        if chance < .75:
            print(f'{id},Breakfast')
        chance = random.random()
        if chance < .75:
            print(f'{id},Lunch')
        chance = random.random()
        if chance < .75:
            print(f'{id},Dinner')
        chance = random.random()
        if chance < .75:
            print(f'{id},Snack')

# Generate pairings between recommendations and existing photos (placeholders)
def generate_photos():
    for i in range(1, 1000):
        id = i
        chance = random.random()
        if chance < .33:
            print(f'{id},food1.avif')
        elif chance < .66:
            print(f'{id},food2.jpeg')
        else:
            print(f'{id},food3.png')

# Generate pairings between recommendations and existing foods
def generate_attached_foods():
    counter = 0
    rec_id = 0
    while counter < 4000:
        num_foods = random.randint(1, 4)
        for j in range(num_foods):
            food_id = random.randint(1, 800)
            print(f'{rec_id},{food_id}')
            counter += 1
        rec_id += 1
        if rec_id > 1000:
            rec_id = 1

# Regenerate recommendations, replacing titles 
def regen_recommendations():
    with open('generated_titles.txt', 'r') as file:
        lines = file.readlines()

    new_titles = [line.strip() for line in lines]

    with open('../data/Recommendations.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        rows = [row for row in csv_reader]    

    for i in range(len(new_titles)):
        rows[i][2] = new_titles[i]
    
    with open('new_recs.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in rows:
            csv_writer.writerow(row)

# regen_recommendations()

# generate_recommendations()
# generate_photos()
# generate_tags()
# generate_attached_foods()
