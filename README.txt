To run the app:
step 1: open anaconda prompt>>navigate to the manage.py directory>>run 'python manage.py runserver'
step 2: open another anaconda prompt>>navigate to the manage.py directory>> run 'python scheduled_tasks.py'

Details:
In this project, I tried to replicate the functionalities of a local cinema's webpage. The key functionalities replicated are as follows:

1) Carousel banner - administrator can login to the admin panel and add or remove banners and each time the page is loaded, banners are dynamically retrieved from the 'Highlights' model.

2) Ticket booking - users can click on a seat to reserve a seat. Once a seat is reserved, it'll turn light blue to the reservation holder or grey to other users, indicating that the seat is unavailable. If the user does not complete his purchase within 30seconds, then the seats are freed up (this is set to 30 seconds for demonstration purposes, actual time window should be longer). 

This serves to prevent conflicts when users try to purchase the same tickets simultaneously and is accomplished via the apscheduler package so the server has to be ran simultaneously with the scheduled_tasks.py script.

3) QR Code tickets - once purchased, tickets are generated in the form of a qr code which encodes the column and row number of the selected seats as well as the transaction time. This QR code will be displayed immediately once the transaction is completed and the user can show it to the usher immediately. 

Alternatively, he can also visit the profile page by clicking on his username in the navigation bar. Here, he can view the entire list of historical transactions and view/hide the corresponding qr code tickets by clicking a button.

4) Movie review - users can click on a rating scale comprising of 5 stars to award a rating to a movie, as well as give an accompanying text review. The reviews are displayed in chronological order, with newer reviews at the top and vice-versa.

5) administration - everything on the webpage is generated dynamically from the various models. To alter elements on the page, the administrators can simply do so via the admin page.