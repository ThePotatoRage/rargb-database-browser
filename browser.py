import sqlite3
from tabulate import tabulate
import os
from art import *

list_of_dicts = []
magnet_hash = ''
search_category = ''
category_name = ''
size = ''
torrent_title = ''

# Prompt user to choose a CATEGORY for the search
while True:
    tprint("RARBG-DB", font="big")
    print("---------------------------------------------------------------")
    print("Welcome to the RARBG Database Browser!\n\n")
    while True:
        cat_choice = input("1. Movies\n"
                           "2. TV Shows\n"
                           "3. Games\n"
                           "4. XXX\n\n"
                           "Choose a category from the above list (1-4):\n")
        if cat_choice == '1':
            search_category = '%movies%'
            category_name = 'movie'
            break
        elif cat_choice == '2':
            search_category = '%tv%'
            category_name = 'tv show'
            break
        elif cat_choice == '3':
            search_category = '%games%'
            category_name = 'game'
            break
        elif cat_choice == '4':
            search_category = '%xxx%'
            category_name = 'porn'
            break
        else:
            print("Invalid input. Please input a NUMBER, between 1 and 4.\n")

    # Prompt user to choose a TITLE NAME for the search
    while True:
        search_title = '%' + input(f"\nWhich {category_name} are you searching for? (insert a title name):\n") + '%'
        search_title = search_title.replace(" ", ".")

        # Connect to the SQLite database
        conn = sqlite3.connect('rarbg_db.sqlite')
        cursor = conn.cursor()

        # Execute the SELECT statement with a WHERE clause to filter the column
        cursor.execute("SELECT hash, title, dt, size, cat FROM items WHERE title LIKE ? AND cat LIKE ?", (search_title,
                                                                                                          search_category))

        # Fetch all the rows returned by the query
        rows = cursor.fetchall()
        if not rows:
            print("Your search did not match any titles. Try again?")
        else:
            break

    # Iterate over the rows, create dicts and add to list of dicts
    for row in rows:
        date = row[2].split(' ')[0]
        try:
            size = f'{round(float(row[3]) / 1e+9, 2)}' + 'GB'
        except TypeError as TE:
            print(TE)
            size = "NoInfo"
            pass
        finally:
            row_dict = {
                "id": rows.index(row),
                "title": row[1],
                "date": date,
                "size": size
            }
            list_of_dicts.append(row_dict)

    # Create a table from the results and print it.
    table = tabulate(list_of_dicts, headers='keys')
    print("\nHere are your search results:\n")
    print(table)

    # Prompt user to choose a torrent from the results table
    user_choice = input(f"\nPlease choose a torrent from above list (insert id number):\n")
    for row in rows:
        if rows.index(row) == int(user_choice):
            magnet_hash = row[0]
            torrent_title = row[1]
            break

    # Create a magnet link with the chosen torrent, and launch the created link
    magnet_link = f'magnet:?xt=urn:btih:{magnet_hash}'
    print(f"\nLaunching your default torrent client and loading '{torrent_title}' torrent...\nEnjoy and remember RARBG!")
    os.startfile(magnet_link)

    # Close the cursor and the database connection
    cursor.close()
    conn.close()

    # Prompt user to choose to quit or to restart script
    restart = input("\n\nEnter 'R' to restart script, enter 'Q' or any other key to quit:\n"
                    "")
    if restart == 'R':
        print('\n\n\n---------------------------------------------------------------')
        os.system('cls')
        pass
    elif restart == 'r':
        print('\n\n\n---------------------------------------------------------------')
        os.system('cls')
        pass
    else:
        break