# Spotify-API-project

This project is to save all of the songs every week from the discover weekly playlist to a playlist the user created.

Setup instructions:

(Step 1) The user needs to create an app on the spotify developer dashboard. Spotify developer dashboard: https://developer.spotify.com

(Step 2) The user needs to run the "auth.py" script. All of the arguments required come from the app the user created on the developer dashboard.

(step 3: Optional) The user can then run the "weekly_adder.py" script. This uses the token generated in the "auth.py" script and a few other arguments.

(step 4) The user can go to their settings and add in their GitHub Actions secrets in the user settings section of GitHub. Once the required secrets are entered then the GitHub Action's will be able to run this script weekly to save the users discover weekly playlist. 
