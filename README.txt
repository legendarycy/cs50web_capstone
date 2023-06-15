==================================================================================
========================1. Distinctiveness and Complexity:========================
==================================================================================

This application is primarily an e-commerce platform, but it has distinct features that set it apart.

Firstly, it dynamically generates theater layouts for each movie and timeslot by using data from multiple database tables. The Halls table provides information about the hall number, as well as the number of columns and rows within each hall. The Tickets table contains details about the seats that have been sold or reserved. If a seat is already reserved or sold, it will be displayed in gray, while available seats will appear in blue. Seats reserved by the user will be highlighted in light blue, and the user can easily click on them again to unreserve.

The application allows real-time seat reservations. Before confirming a reservation, the application checks the seat availability through a GET request. Reservations are held for 10 minutes, even if the user navigates away from the page. If the user doesn't complete the transaction within that time, the seats will be released.

For each movie, there is also a review section where users can rate the movie using a star scale. By clicking on a star, the user can indicate their rating. For example, if they want to give a movie a rating of 4 out of 5 stars, they can click on the 4th star, which will light up that star and all the preceding ones.

Furthermore, the application generates a unique QR code for each transaction, containing information about all the purchased seats. Each transaction can only include seats from a single movie session. The user can access and revisit this QR code within their profile page.

==================================================================================
=================================2. File Content==================================
==================================================================================

views.py: Contains view functions that handle the loading of pages and APIs.

models.py: Defines eight different models:

User: Stores user authentication data.
Halls: Stores information about each hall, such as hall number, number of rows, and columns of seats.
Movies: Stores data for each movie, including title, duration, release date, etc.
Movie_Hall_Allocation: Tracks the assignment of halls to play specific movies on particular dates and times.
Reviews: Stores review data, including the reviewer's information, content, timestamp, and rating given.
Tickets: Registers ticket data, including sold and reserved tickets, along with corresponding transaction entries.
Transaction: Stores the QR code for each successfully completed transaction.
Templates: Contains six HTML files, with layout.html serving as the base template.

static folder: Contains the CSS file for the entire project, as well as three JavaScript files for index.html, movie_page.html, and profile.html, respectively.

index.js: Sends a GET request to load the list of movies when users visit the home page.
movie_page.js: Responsible for fetching data on a specific movie that the user has clicked on, handling seat reservation/purchase, and review writing.
profile.js: Responsible for loading past transaction data.
scheduled_tasks.py: Contains a function that runs every 10 seconds using apscheduler. Its purpose is to free up seats that have been reserved for more than 30 seconds. Note that in practice, the window should be larger, but it is set to 30 seconds for testing purposes.

==================================================================================
==============================3. How to run the app:==============================
==================================================================================

To run this project, follow the steps below:

Step 1: Open Anaconda Prompt and navigate to the directory where 'manage.py' is located. Then, run the following command: python manage.py runserver

Step 2: Open another Anaconda Prompt and navigate to the same directory as before. Run the following command: python scheduled_tasks.py

==================================================================================
=================================4. Functionalities===============================
==================================================================================

Carousel banner: The administrator can log in to the admin panel and add or remove banners. Each time the page is loaded, the banners are dynamically retrieved from the 'Highlights' model.

Ticket booking: Users can reserve seats by clicking on them. When a seat is reserved, it turns light blue for the reservation holder and gray for other users, indicating its unavailability. If a user doesn't complete the purchase within 30 seconds, the seats are freed up (the 30-second window is set for demonstration purposes, the actual time window should be longer). This prevents conflicts when multiple users try to purchase the same tickets simultaneously. This functionality is implemented using the apscheduler package, so the server needs to run simultaneously with the 'scheduled_tasks.py' script.

QR Code tickets: Once purchased, tickets are generated as QR codes, encoding the column and row numbers of the selected seats, as well as the transaction time. The QR code is displayed immediately after the transaction is completed. Users can show the QR code to the usher for admission. Alternatively, users can visit the profile page by clicking on their username in the navigation bar. On the profile page, users can view the list of their historical transactions and view/hide the corresponding QR code tickets by clicking a button.

Movie review: Users can click on a 5-star rating scale to award a rating to a movie and provide a text review. The reviews are displayed in chronological order, with newer reviews at the top.

Administration: All webpage elements are dynamically generated from various models. Administrators can easily alter page elements through the admin page.
