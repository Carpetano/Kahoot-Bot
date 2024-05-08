# YouCantWin

YouCantWin is a collection of tools and automation scripts to collect data from **public** kahoots.

It started as a simple script that would print answers so you know ahead of time what option to click and never lose on your kahoots, but now it includes a script that will automatically play for you. ()

In order to 'cheat' in a kahoot you need to know 2 things: 
1. The unique kahoot ID, example: ```f1493c5d-b162-4be1-ac83-35c783e34588```
2. The kahoot must be public otherwise you won't be able to retreive the questions and answers ahead of time <br><br>
3. (Optional but VERY useful) If you frequently play kahoots from the same profile (your teacher's profile) you can store the profile ID to know where to look for the IDs

## Scripts

## How to set it up
Create a file called ```Profile.txt``` where you will place the id of the profile you want to scrap all ids for later use

> ## PrintKahootData.py
> Script to Print the questions and answers of a kahoot by it's ID

> ## StoreKahootsIds.py
> From the ID set in the ```Profile.txt``` file, it wil scrap all id's then it will create/replace a file called ```IDs.txt``` with this format:
> ```
> ID -@- TITLE -@- Position of the correct answer
> ```

> ## KahootsToText.py
> From the ```IDs.txt``` file, it will create a folder called ```kahoots``` with all kahoots <br>
> The purpose of this one is in case you need to save them to need the questions and answers for a test


