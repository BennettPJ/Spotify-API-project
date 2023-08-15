# Spotify-API-project

This project is to save all of the songs every week from the discover weekly playlist to a playlist the user created.

08-15-2023: This project is not yet automated. In the future the weekly adder playlist will be automated. The "auth.py" script will only need to be ran once on the initial creation of a new app by the user.

Setup instructions:

(Step 1) The user needs to create an app on the spotify developer dashboard.
            - spotify developer dashboard: https://developer.spotify.com

(Step 2) The user needs to run the "auth.py" script. 
            -All of the arguments required come from the app the user created on the developer dashboard

(step 3) The user can then run the "weekly_adder.py" script.
            -This uses the token generated in the "auth.py" script and a few other arguments
