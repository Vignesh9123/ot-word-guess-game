# Word Game Django Application

This is a simple word guessing game built with Django. Users can register, log in, and play up to three games for a given calendar day.

## Features

- **User Registration & Login:** Users can create an account and log in to play.
- **Daily Game Limit:** Each user can play up to 3 games per day.
- **Word Guessing:** Guess the 5-letter word in up to 5 tries. Feedback is given for each letter (green/yellow/gray).
- **Admin Reports:** Admin users can view reports by day or by user, including number of games played and correct guesses.

## How to Play

1. **Register** for an account.
2. **Log in** to your account.
3. Click **Start Game** to begin a new word guessing game.
4. Enter your guesses. Each guess must be a 5-letter word.
5. The game will provide feedback for each letter:
    - **Green:** Correct letter in the correct position.
    - **Yellow:** Correct letter in the wrong position.
    - **Gray:** Letter not in the word.
6. You have 5 attempts to guess the word.
7. You can play up to 3 games per day.

## Admin Functionality

- **Admin Day Report:** View the number of users who played and the number of correct guesses for a specific date.
- **Admin User Report:** View a user's game history, including games played and correct guesses per day.

## Code Overview

The main logic for user authentication, game play, and admin reports is implemented in [`views.py`](wordgame/views.py). Key functions include:

- `register(request)`: Handles user registration.
- `login(request)`: Handles user login.
- `logout(request)`: Logs out the user.
- `start_game(request)`: Starts a new game for the user.
- `play(request, game_id)`: Handles the game play and guess logic.
- `admin_day(request)`: Admin report by day.
- `admin_user(request)`: Admin report by user.

## Setup

1. Clone the repository.
2. Install dependencies:  
   ```
   pip install django
   ```
3. Run migrations:  
   ```
   python manage.py migrate
   ```
4. Create a superuser (for admin access):  
   ```
   python manage.py createsuperuser
   ```
5. Init the database:
   ```
   python manage.py initdb
   ```
6. Start the development server:  
   ```
   python manage.py runserver
   ```
7. Access the app at [http://localhost:8000/](http://localhost:8000/)