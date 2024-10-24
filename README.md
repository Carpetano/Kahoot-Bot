# YouCantWin

YouCantWin is my first serious Python program to automatically play Kahoot in class.

It started as a simple script that would print answers so you know ahead of time what option to click and never lose on your kahoots, but now it includes a script that will automatically play for you.

In order to 'cheat' in a kahoot game you need to meet 2 requirements: 
1. The unique kahoot ID, example: ```e79f98a5-a674-4603-941b-8c99cd876194```

[UUID example](https://github.com/user-attachments/assets/f6633106-e01d-448b-b91a-120050d4f35c)
  
3. **The kahoot must be public** otherwise you won't be able to retreive the questions and answers ahead of time <br><br>
4. (Optional but VERY useful) If you frequently play kahoots from the same profile (your teacher's profile) you can store the profile ID to know where to look for the IDs

# WIP scripts, will upload eventually

## How to set it up
Create a file called ```Profile.txt``` where you will place the id of the profile you want to scrap all ids for later use

> ## PrintKahootData.py
> Script to Print the questions and answers of a kahoot by it's ID!


> ## StoreKahootsIds.py
> From the ID set in the ```Profile.txt``` file, it wil scrap all id's then it will create/replace a file called ```IDs.txt``` with this format:
> ```
> ID -@- TITLE -@- Position of the correct answer
> ```

> ## KahootsToText.py
> From the ```IDs.txt``` file, it will create a folder called ```kahoots``` with all kahoots <br>
> The purpose of this one is in case you need to save them to need the questions and answers for a test
