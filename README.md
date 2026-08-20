# Book Tracker
#### Video Demo: https://www.youtube.com/watch?v=DaOQATqvEjY
#### Description:

This is a Python program created to help users keep track of their reading.

## About the Project

In the program, users can add books to three different lists:

- **Want to Read**
- **Reading**
- **Finished Reading**

The books are saved in CSV files, so the information is not lost when the program is closed. When a book is moved to another list, it is automatically removed from the previous one.

I also connected the program to the Open Library API to check if the book entered by the user really exists. If the book cannot be found or the title was entered incorrectly, the program asks the user to try again.

The program also checks if the dates entered are valid. When a book is moved from the **Reading** list to the **Finished Reading** list, it calculates how many days the user spent reading it. The user can also give the book a rating from 0 to 5 stars.

It is also possible to add a book directly to the **Finished Reading** list. In this case, the program cannot calculate the reading days, so it shows a dash (`-`) instead.

## Libraries Used

At the top of the code are the libraries used in the project.

- **Rich** was used to format the menu and book lists, making them more visually appealing to the user.
- **CSV** was used to store the lists of added books together with information such as the author and date.
- **Datetime** was used to validate and standardize the dates entered by the user.
- **Requests** was used to access the Open Library API.
- **JSON** was used to handle the data returned by the API.

## How the Program Works

### The `main()` Function

The `main()` function calls the `menu()` function and stores the selected option in a variable called `c`.

Different functions are then called by `main()` depending on the value returned by `menu()` to the variable `c`.

### The `menu()` Function

The `menu()` function has seven options:

1. Add a book to the **Want to Read** list.
2. Add a book to the **Reading** list.
3. Add a book to the **Finished Reading** list.
4. View the **Want to Read** list.
5. View the **Reading** list.
6. View the **Finished Reading** list.
7. Close the program.

If the user selects an invalid number, they are asked to enter a valid number again. This continues until a valid number is returned to the `main()` function.

## Getting and Searching for a Book

### The `get_book()` Function

The `get_book()` function is called by `main()` if the user selects option 1, 2, or 3.

This function is responsible for asking the user to enter the author's name and the book title. This continues until an existing book can be returned after being validated as `True` by the `book_search()` function.

To check whether a book exists, the `book_search()` function is used inside `get_book()`.

### The `book_search()` Function

The `book_search()` function receives the author's name and book title entered by the user. This information is then passed to the Open Library API, which checks whether the book exists.

If the book is not found or there is a connection error with the API, the function returns `False`. This causes the `get_book()` function to ask the user for the information again.

The `get_book()` and `book_search()` functions are separated so that `book_search()` can be tested later. In this way, the logic that searches for a book is separated from the user input.

## Getting and Validating a Date

### The `get_date()` Function

If the user selects option 2 or 3 from the menu, the `get_date()` function is called by `main()`.

The `get_date()` function asks the user to enter a date in the `ddmmyyyy` format. The date is then checked using the `validate_date()` function.

### The `validate_date()` Function

The date passed to `validate_date()` is first analyzed to check whether it contains one of the three accepted separators. A date without a separator is also accepted.

After the separator has been checked, the `datetime` library is used to check whether the date is valid.

If it is a valid date, it is formatted into one standard format, `dd/mm/yyyy`, and returned.

If the date is not valid, `None` is returned. This causes `get_date()` to ask the user to enter a new date.

## Menu Options

### Option 1: Add a Book to “Want to Read”

When option 1 is selected, the user chooses to add a new book to the **Want to Read** list.

The `main()` function passes the information returned by `get_book()` to the `adding_books()` function.

The `adding_books()` function is responsible for opening the `want_to_read.csv` file and adding the new book to the list.

### Option 2: Add a Book to “Reading”

When option 2 is selected, the book is added to the **Reading** list.

The information collected by the `get_date()` and `get_book()` functions is passed to the `reading()` function.

The `reading()` function adds the book to the `reading.csv` file. It also checks whether the book was previously stored in the `want_to_read.csv` file.

If the book is found in `want_to_read.csv`, it is removed from that file. The book is then kept only in the **Reading** list, together with:

- The reading start date
- The author's name
- The book title

### Option 3: Mark a Book as Read

Option 3 is used to mark a book as read.

In addition to using the information returned by `get_date()` and `get_book()`, the `getting_rate()` function is also called by `main()`.

#### The `getting_rate()` Function

The `getting_rate()` function asks the user to enter an integer from 0 to 5. This number represents the user's rating of the book.

The value is stored in a variable called `rate` inside `main()`. It is then converted into star emojis when it is passed as an argument to the `read_list()` function.

If the user enters an invalid value, they are asked to enter a new value. This continues until a valid rating is entered.

The information saved in the variables is then passed to the `read_list()` function.

#### The `read_list()` Function

The `read_list()` function checks whether the book marked as read was stored in the `reading.csv` file.

If the book is found, it is removed from `reading.csv`. The reading start date is also saved in a variable called `start`.

If the book is not found in the `reading.csv` file, the `start` variable remains with the value `None`.

The value stored in `start` and the value passed in the `end_date` argument are then passed to the `time_reading()` function.

The result returned by `time_reading()` is stored in a variable called `days`.

#### The `time_reading()` Function

The `time_reading()` function calculates how many days the user took to read the book.

If the reading start date and end date are the same, the function returns:

`"0 days"`

If the end date is later than the start date, the number of reading days is calculated.

If the start date is later than the end date or the start date does not exist, the function returns:

`"-"`

Finally, `read_list()` uses the values stored in `end_date`, `author`, `title`, `rate`, and `days` to add the book to the list of finished books.

### Option 4: View the “Want to Read” List

If option 4 is selected in `menu()`, the books stored in the `want_to_read.csv` file are shown.

For this, the `wish_list()` function is called by `main()`.

The function opens the file and creates a table containing the books from the **Want to Read** list. The table is formatted using the Rich library to make it look nicer and easier to read.

The following information is shown:

- Author
- Book title

### Option 5: View the “Reading” List

If option 5 is selected in `menu()`, the books stored in the `reading.csv` file are shown.

For this, the `show_reading()` function is called by `main()`.

The function opens the `reading.csv` file and creates a table containing the books that the user is currently reading. The table is also formatted using the Rich library.

The following information is shown:

- Reading start date
- Author
- Book title

### Option 6: View the “Finished Reading” List

If option 6 is selected in `menu()`, the `show_read()` function is called by `main()`.

The function opens the file containing the finished books and creates a table using the Rich library.

The table shows:

- The finishing date
- The author
- The book title
- The rating converted into star emojis
- The number of days it took to finish the book

### Option 7: Close the Program

Finally, option 7 closes the program and prints the following message on the screen:

`Have a good read!`

## Testing

In the test file, three functions were tested:

- `validate_date()`
- `book_search()`
- `time_reading()`

### Testing `validate_date()`

The `validate_date()` function was tested using dates in the accepted formats.

When a valid date is provided, it is returned in the standard `dd/mm/yyyy` format.

Formats that are not accepted were also tested. In these cases, `None` is returned.

### Testing `book_search()`

The `book_search()` function was also tested.

For this test, a mock API response and a JSON dictionary were created. This means that the real Open Library API does not need to be contacted during the test.

For `True` to be returned, the list returned by the mocked JSON response must contain at least one element.

If the returned list is empty, `False` is returned.

### Testing `time_reading()`

The last function tested was `time_reading()`.

Different dates were provided to check:

- If the number of reading days is calculated correctly in normal cases.
- If `"-"` is returned when the start date is later than the end date.
- If `"0 days"` is returned when the start and end dates are the same.
- If a `ValueError` is raised when the dates are invalid or use formats that are not accepted.
