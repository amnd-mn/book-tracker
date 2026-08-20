from rich.console import Console
from rich.table import Table
import csv
from datetime import datetime
import requests
import json

#Book Tracker
def main():
    c = menu()
    if c == 1:
        adding_books(*get_book())

    elif c == 2:
        start_date = get_date()
        author, title = get_book()
        reading(start_date, author, title)

    elif c == 3:
        end_date = get_date()
        author, title = get_book()
        rate = getting_rate()
        read_list(end_date, author, title, rate * "⭐")

    elif c == 4:
        wish_list()

    elif c == 5:
        show_reading()

    elif c == 6:
        show_read()

    elif c == 7:
        print("Have a good read!")




# shows the user the options and return the selected option
def menu():
    menu = Table(title= "Book Tracker", caption= "Please select a number", show_lines=True, style="white")

    menu.add_column("Menu Options", style="pink1")
    menu.add_row("1. Add a new book to the 'Want to Read' list.")
    menu.add_row("2. Add book to the 'Reading' list")
    menu.add_row("3. Add book to the 'Finished Reading' list and rate it")
    menu.add_row("4. See the 'Want to Read' list.")
    menu.add_row("5. See the 'Reading' list.")
    menu.add_row("6. See the 'Finished Reading' list.")
    menu.add_row("7. Exit.")

    console = Console()
    console.print(menu)

    while True:
        try:
            choice = int(input("Type your option: "))
            if choice >= 1 and choice <= 7:
                    return choice
            else:
                print("Enter a number from the available options")
        except ValueError:
            print("Enter a number from the available options")

# checks if the book exists
def book_search(a, t):
    try:
        response = requests.get("https://openlibrary.org/search.json?author=", params={"author": a, "title": t})
        result = response.json()
        if len(result["docs"]) > 0:
            return True
        else:
            print("Book not found! ")
            return False
    except requests.RequestException :
        print("Connection error! Please try again later!")
        return False

#checks if the date is in a valid format and return the date
def validate_date(d):
    try:
        date = d
        if ("/" in date or "-" in date or "." in date) and len(date) == 10:
            date = date.replace(".", "").replace("-", "").replace("/", "")
            date = datetime.strptime(date, "%d%m%Y")
            if date:
                date = date.strftime("%d/%m/%Y")
                return date

        elif len(date) == 8:
            date = datetime.strptime(d, "%d%m%Y")
            if date:
                date = date.strftime("%d/%m/%Y")
                return date
    except:
        return None

# asks the user for a rate from 0 to 5
def getting_rate():
    while True:
        try:
            rate = int(input("Enter a rate between 0 and 5: "))
            if rate >= 0 and rate <= 5:
                return rate
            else:
                print("Enter a number between 0 and 5")
        except ValueError:
            print("Enter a number between 0 and 5")

# calculate the time needed to finish the book
def time_reading(end, start):
    try:
        end_date = datetime.strptime(end, "%d/%m/%Y")
        start_date = datetime.strptime(start, "%d/%m/%Y")

        if end_date > start_date:
            result = end_date - start_date
            return f"{result.days} days"

        elif end_date == start_date:
            return "0 days"

        else:
            return "-"

    except (ValueError):
        return "ValueError"

# add new books to the csv file books list
def adding_books(author, title):

    with open("want_to_read.csv", "a") as file:
        add_book= csv.DictWriter(file, fieldnames=["author", "title"])
        add_book.writerow({"author": author, "title": title})

# asks for the right input
def get_book():
    while True:
        try:
            author = input("Enter the author's name: ").strip()
            title = input("Enter the book title: ").strip()
            result = book_search(author, title)
            if result:
                return author, title
            else:
                print("Try again! ")
        except:
            print("Try again!")



# it opens the "Want to Read" list
def wish_list():

    unread_books = Table(title= "Want to Read", show_lines=True, style="white")
    unread_books.add_column("Author", style="pink1")
    unread_books.add_column("Title", style="pink1")

    with open("want_to_read.csv", "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            author = line["author"]
            title = line["title"]
            unread_books.add_row(author, title)

    console2 = Console()
    console2.print(unread_books)

# moves the books from want to read to reading
def reading(start_date, author, title):


    with open("reading.csv", "a") as file:
        add_book= csv.DictWriter(file, fieldnames=["start date","author", "title"])
        add_book.writerow({"start date": start_date, "author": author, "title": title})

    books = []
    with open("want_to_read.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["title"] == title:
                continue
            else:
                books.append({"author": row["author"], "title": row["title"]})

    with open("want_to_read.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["author", "title"])
        writer.writeheader()
        for book in books:
            writer.writerow(book)

# adds a book to the list of already read book, rate it and removes from reading
def read_list(end_date, author, title, rate):

    start = None
    books = []
    with open("reading.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row["title"] == title:
                start = row["start date"]
            else:
                books.append({"start date": row["start date"], "author": row["author"], "title": row["title"]})

    with open("reading.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=["start date", "author", "title"])
        writer.writeheader()
        for book in books:
            writer.writerow(book)

    if start is None or end_date is None:
        days = "-"
    else:
        days = time_reading(end_date, start)

    with open("read.csv", "a") as file:
            add_book= csv.DictWriter(file, fieldnames=["end date", "author", "title", "rate", "days reading"])
            add_book.writerow({"end date": end_date, "author": author, "title": title, "rate": rate, "days reading": days})



# it shows the list "Reading"
def show_reading():

    reading = Table(title= "Reading", show_lines=True, style="white")
    reading.add_column("Start Date", style="pink1")
    reading.add_column("Author", style="pink1")
    reading.add_column("Title", style="pink1")

    with open("reading.csv", "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            start_date = line["start date"]
            author = line["author"].title()
            title = line["title"].title()

            reading.add_row(start_date, author, title)

    console2 = Console()
    console2.print(reading)

# it shows the list of "Read Books" and its rate
def show_read():

    finished_books = Table(title= "Finished Reading", show_lines=True, style="white")
    finished_books.add_column("End Date", style="pink1")
    finished_books.add_column("Author", style="pink1")
    finished_books.add_column("Title", style="pink1")
    finished_books.add_column("Rate", style="pink1")
    finished_books.add_column("Days Reading", style="pink1")

    with open("read.csv", "r") as f:
        reader = csv.DictReader(f)
        for line in reader:
            end_date = line["end date"]
            author = line["author"].title()
            title = line["title"].title()
            rate = line["rate"]
            days_reading = line["days reading"]

            finished_books.add_row(end_date, author, title, rate, days_reading)

    console2 = Console()
    console2.print(finished_books)

# asks the user for a valid date format
def get_date():
    while True:
        try:
            date = input("Type a valid date (ddmmyyyy): ")
            result = validate_date(date)
            if result != None:
                return result
        except:
            print("Not Valid! ")





if __name__ == "__main__":
    main()
