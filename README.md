# Dojo-Reads
Django application where logged in users can view and add book reviews. A user should also be able to delete his/her own reviews.

Registration and Login Page: http://localhost:8000/
  Validations should work on the Login and Register parts
  
Home Page: http://localhost:8000/books
  Recent Book Reviews:
    Display the last three reviews
    Book title is linked to the book's individual page
    User name is linked to the user's individual page
  Other Books with Reviews:
    Display the list of book titles with existing reviews
    Each Book title is linked to the book's individual page

Add Book and Review Page: http://localhost:8000/add
  Add a New Book Title and a Review:
    When the new book title and review is added, the user will be redirected to the page for that specific book
    
Add Book and Review Page: http://localhost:8000/books/1
  Individual Book:
    User can add anew review
    User can also delete his own review only. A link to delete the review will appear for the looged user review item
    
User Reviews Page: http://localhost:8000/user/1
  User Alias:
    Displays the user data and the count of reviews the user has posted
    Also displays the list of books where the user posted his/her review
