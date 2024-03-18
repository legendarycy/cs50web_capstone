# CS50 Capstone Project: Movie-booking Website

## How to run:

To run this project, follow the steps below:

1. Open Anaconda Prompt and navigate to the directory where 'manage.py' is located. Then, run the following command: `python manage.py runserver`.
2. Open another Anaconda Prompt and navigate to the same directory as before. Run the following command: `python scheduled_tasks.py`.

## Introduction

This was my first web application in Django and was submitted as my capstone project for the CS50 Web Development module. As my inaugural venture into Django, this project represents a significant milestone in my learning journey. While selecting the project topic, I was looking for something distinct from the typical choices like news sites or social media platforms. Inspired by the renowned local movie theatre chain, Golden Village, I set out to create a digital platform that encapsulates the essence of its services while incorporating innovative functionalities.

In this document, I will introduce my project, following the MVT structure commonly used in vanilla Django projects. I will begin by discussing the models, followed by the view functions, and conclude with the templates. This sequential approach will provide a comprehensive overview of the project's architecture and implementation.

## Project Goal

The goals of this project are as follows:
- Create a Django web application mirroring Golden Village's services.
- Implement standard CRUD operations for seamless data management.
- Integrate seat reservation and automatic release mechanisms.
- Generate QR code-based tickets for added convenience and security.
- Ensure conflict-prevention mechanisms for safe concurrent bookings.
- Review system, which allows users to leave a rating (between 0-5) and a text review for movies.

With additional features such as conflict prevention and QR ticket generation, I’m striving to build a clone which resembles the actual web application itself as much as possible in terms of functionalities. This endeavour serves as a personal challenge to expand my skills beyond the course curriculum and tackle real-world challenges faced by theatre operators.

## Models

The project consists of the following 8 models:

1. **User**
    - Built-in authentication system based on the default user model.
2. **Movies**
    - Stores movie information such as title, release date, language, casts, director, genre, runtime, description, movie thumbnail.
3. **Halls**
    - Each entry within the system corresponds to a movie hall, encapsulating details such as the hall number, as well as the respective count of rows and columns of seats. For the sake of model simplicity, I approached the design under the assumption that seat arrangements adhere to a uniform row-by-column layout, with consistent seat counts per row.
4. **Movie_Hall_Allocation**
    - Junction table which handles allocation of movie to halls on a given date and time. Another way of looking at this model is that each entry represents a movie session.
5. **Transaction**
    - Contains a single image field which holds ticket QR code information. Used as foreign key in Tickets to match tickets up with a corresponding QR code.
6. **Tickets**
    - The "tickets" table serves as a repository for ticket ownership details. Each ticket is associated with a holder upon creation, utilizing the "User" model as a foreign key. Alongside holder information, the table includes essential data such as seat row, column, and movie session, with "Movie_Hall_Allocation" serving as the foreign key. These details facilitate the mapping of tickets to corresponding seats in movie sessions. Additionally, the table features attributes like "status," "timestamp," and "transaction" for validation and seat reservation purposes. Notably, a ticket doesn't always necessitate a match with a transaction, as it may be generated upon reservation without immediate payment. If payment isn't completed within the specified timeframe (referenced by the ticket's creation timestamp), the ticket is deleted, and the seat becomes available again. Conversely, upon payment, a transaction entry is generated, resulting in the creation of a QR code ticket and its association with the corresponding ticket to denote seat sale.
7. **Reviews**
    - The "reviews" table houses data related to movie reviews, with each review comprising various attributes. These include the author, represented by a foreign key referencing the "User" model, along with a rating (an integer ranging from 0 to 5), a comment, a timestamp indicating when the review was made, and finally, a foreign key linking to the respective movie being reviewed.
8. **Highlights**
    - The table "highlights" stores data necessary for generating carousel advertisements on the homepage. It comprises two fields: an image field containing the file path of the banner and a character field storing the banner's title. Utilizing a view function, all entries within the "highlights" table will be retrieved to dynamically generate a carousel featuring these banners on the homepage.

## View Functions

In this section, I’ll be going through some of the key functions running on the backend. Since there’s a lot of them, I’ll group them together based on their purpose and give an overview of what they do.

1. **Homepage Carousel Display (index view):**
   The index view renders the homepage of the website, featuring a carousel of highlights fetched from the Highlights table. These highlights could include promotional banners, upcoming movie releases, or special events, providing users with visual cues to navigate through the website's content. The carousel dynamically adjusts based on the available highlights, ensuring fresh and engaging content for visitors.

2. **User Authentication (login_view, logout_view, register views):**
   These view functions handle user authentication processes, including login, logout, and registration. Upon submitting valid credentials, users are authenticated and granted access to protected features such as purchasing tickets or leaving reviews. In case of invalid credentials or registration errors, appropriate error messages are displayed to guide users through the authentication process seamlessly.

3. **Movie Listing and Details (get_movies, movie_page views):**
   The get_movies view retrieves a list of available movies from the database and returns them as a JSON response. This information is then displayed to users, allowing them to browse through movie listings and select movies of interest. The movie_page view renders detailed information about a specific movie, including its title, description, cast, genre, and available showtimes. Users can explore movie details, view showtimes, and access user reviews to make informed decisions about movie selection.

4. **User Profile Management (profile_page view):**
   The profile_page view renders the user's profile page, displaying their transaction history and purchased tickets. Users can track their activity within the application, view past transactions, and monitor their engagement with the platform. The profile page provides a centralized hub for managing user interactions and preferences, enhancing the overall user experience.

5. **Seat Reservation and Ticketing (get_seats, checkout, reserve_seat views):**
   These views handle seat reservation and ticketing processes, allowing users to select seats for their desired movie sessions and complete the checkout process. The get_seats view retrieves seat availability information for a specific movie session and returns it as a JSON response. Users can then reserve available seats, proceed to checkout, and receive digital tickets containing essential booking details. The reserve_seat view manages seat reservations, ensuring availability and preventing conflicts during the reservation process.

   To expand on the conflict prevention mechanism, the exact logic behind this feature is as follows:
   - When a user attempts to reserve a seat for a specific movie session, their request is processed by the reserve_seat view function.
   - The view function checks if the requested seat is available for reservation by querying the database. It searches for existing ticket entries matching the specified seat, column, and movie session.
   - If a ticket entry matching the requested seat and movie session already exists in the database, it indicates a potential conflict. This implies that the seat is already reserved by another user for the same movie session.
   - To prevent conflicts, the view function checks for the existence of a matching ticket entry. If no matching ticket is found, the requested seat is considered available, and a new ticket entry is created for the user, marking the seat as reserved.
   - However, if a matching ticket entry exists, it signifies that the requested seat is already reserved by another user. In this case, the view function returns a JSON response indicating the presence of a conflict, informing the user that the seat is unavailable for reservation.
   - Depending on the outcome of the conflict detection process, the view function returns an appropriate JSON response to the user. If the seat is successfully reserved without conflicts, a success message is returned. Otherwise, a message indicating the presence of a conflict is provided to the user, guiding them to select an alternative seat.

## Scheduled Tasks

Working in conjunction with the seat reservation and ticketing functions, the “clear_reservations” function is set to run periodically to clear reservations which have exceeded the time limit (for demonstration purposes, the reservation time is set to 30 seconds). This function simply applies a filter to check if there are any entries from the “Tickets” table with timestamp + 30 seconds > current time and status of “reserved”. If the queryset is non-empty, then these entries are deleted to free up the corresponding seats to other patrons. 

This ensures that seats are utilized efficiently and remain available for other patrons, maximizing overall seat occupancy and revenue potential. By regularly removing expired reservations, the function maintains data integrity within the "Tickets" table, preventing clutter and facilitating smoother data retrieval and analysis processes. Moreover, the implementation of the "clear_reservations" function demonstrates the scalability of the ticketing system, effectively managing increasing user demand while accommodating customization of the reservation time limit to suit specific operational needs. 

Leveraging the apscheduler library for background task scheduling, the function automates the reservation clearance process, minimizing manual intervention and ensuring reliable execution of periodic tasks.

## Templates

Lastly, I’ll be introducing the templates used in this project. 

1. **Layout.html**
   - The layout template serves as the foundation for the Golden Village Cinema website, providing a consistent structure and styling across all pages. Here's an overview of its key components:

2. **Login.html**
   - The login page template allows users to authenticate themselves and access restricted features of the Golden Village Cinema website. The template extends the base layout template (ticket_purchase/layout.html), inheriting its structure and styling to maintain consistency across pages. CSRF protection is implemented using the {% csrf_token %} template tag to prevent cross-site request forgery attacks.

3. **Movie_page.html**
   - This template provides users with detailed information about a specific movie, along with options to purchase tickets and leave reviews. Here's an overview of its key features:
     - Movie Details Display: Showcases key information about the movie, including title, release date, language, genre, runtime, director, cast, and synopsis, accompanied by a visually appealing poster.
     - Ticketing Section: Enables users to browse available timeslots and select their preferred screening time. Offers an interactive seating plan for seat selection, with dynamically updated seat display.
     - Review Section: Allows authenticated users to leave reviews with ratings and comments for the movie. Utilizes star icons for rating feedback and displays existing reviews below the submission form.

4. **Profile.html**
   - This template provides users with information regarding past transactions and upcoming bookings.
     - Transaction Display: Presents a list of user transactions, detailing each purchase made, including movie title, screening date and hall number, purchased seats, transaction amount, and payment timestamp.
     - Visual Representation: Utilizes a visually appealing layout with a yellow container to highlight transaction details, accompanied by movie thumbnails for easy identification.
     - QR Code Integration: Incorporates QR code functionality for each transaction, enabling users to access their ticket QR codes with a single click. Enhances user experience and convenience.

