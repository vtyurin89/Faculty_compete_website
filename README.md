# FACULTY
#### Video Demo:  <https://www.youtube.com/watch?v=zxdhpmkxk-U>
#### Description: A web application for teachers which allows them to award points to houses or classes in a school (or to deduct points). The teacher can award students for good deeds or correct answers and take the points away for wrong answers or misbehaviour. This system resembles the points system from Hogwarts school from Harry Potter book series.

# Technologies

- Python
- Django
- SQLite3
- jQuery
- HTML
- CSS
- Bootstrap 5

# Features

## Login / Register Page

All users have to create an account and log in before using the application. The validation is Django's standart form validation. Before the user logs in he cannot access index page or any other page of the website.

## Index Page
The content of the index page will change depending on the status of the user.

If the user is not assigned to any school profile on the website, the application will offer him to either JOIN an already existing school or to CREATE a new school.

If the user chooses to create a school, the application will send him to **School creation page** and redirect back after the school has been created. This will add a new school to the database and link the user to this school. After that the user will be able to create several Houses/Faculties in the new school: upon clicking the button the application will send him to Faculty creation page and the redirect back after the faculties have been created. This will "activate" the school, and now it's set up and ready to go.

If the user chooses to join a school, the application will send him to **Join school page**, where he is supposed to input the unique secret code of the school. Random secret code is automatically generated upon creation of the school. You can find your schools' code in the profile menu, however there is no way to get somebody else's code unless the other user gives it to you. This is done to prevent random people from joining (*this is probably not the most sophisticated implementation, however it works for now*). The user cannot join a school if it has not been activated (if the faculties have not been created yet).

If the user created and activated a school OR joined a school, he will see a little menu with the list of Houses/Faculties with their current amount of points and two buttons: "Award" and "Deduct" under an input field.

The user can choose any house/faculty, type the amount of points in the input field and press any of the two buttons to either award or deduct points. The corresponding house/faculty will either get or lose this amount of points.

There are several simple rules for points usage (yes, the code will not allow you to break them):

- The user cannot award or deduct zero points or a negative amount of points or a fractional number of points.
- The user cannot award or deduct more than 1000 points.
- The number of points of each house/faculty cannot drop below 0. If it goes below 0, it will just remain 0.

The application shows some more useful information about the school on the index page:

 - 10 recent actions done by the users who belong to this school.
 - The name of the currently winning faculty (if there is a draw, the application will show that there is a draw).
 - The graph of the competition. The graph is generated with the help of jquery.

## School creation page

The user who doesn't belong to any school will be able to create a new school, choosing name, country and city. The form also contains text field for additional information about the school. Country selection is implemented using django-countries module (version 7.5.1). Upon submitting the form the user will be linked to this school, so this page will become inaccessible. *The application doesn't have any functionality to switch schools yet.*

## Faculty creation page

The user who created a new school will be able to create several faculties/houses, choosing their names. Javascript code on this page allows to dynamically create or delete new input fields, so the user can create as many faculties as he wants. Any blank fields or the ones having duplicate names will not be processed.

Upon submitting the form this page will become inaccessible.

## Join school page

The user who doesn't belong to any school will be able to input some school's secret key in order to join it. Upon submitting the code the user will be linked to this school, so this page will become inaccessible.  

## User settings

User settings include an additional menu (profile menu) and 4 pages:  **User profile page, School information, Recent actions, Safety**.

###  User profile

This page allows users to configure their user profile (to change first name, last name, email and profile picture).

Profile picture functionality was implemented with the help of two Django modules: easy-thumbnails (version 2.8.5) and django-cleanup (version 7.0.0).

By default the application uses two avatar placeholders. The smaller one is 35x35 pixels, it is used in the navigation bar, the bigger one is 96x96 pixels and it's used in the profile menu.

If the user uploads a new picture, the application automatically creates a user folder in /media/images and then creates two corresponding thumbnails using easy-thumbnails.

Since Django does not automatically delete unused picture files, django-cleanup comes to the resque and does exactly that when the user updates the profile picture.

*But django-cleanup does not delete thumbnails generated by easy-thumbnails, which became a problem during the development. So I had to create a post-delete signal which solved this issue.*

### School information

This page shows information about the current school of the user (if it exists). If the school exists, here we can find the secret key of the school which we can give to other teachers who would want to join.

### Recent actions

In fact, this page contains not the recent actions, but ALL the actions of the current user with timestamps.

Standard Django Paginator class was used to do pagination.

### Safety

This page allows users to change password.

