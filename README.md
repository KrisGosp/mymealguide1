# MyMealGuide

#### Video Demo:

#### Description:

This project is intended to help and simplify the management and choosing of recipes at home. I am a student and often find it really challenging to come up with what should I cook at home, despite being able to cook many different recipes, all of which I would proudly say that I really enjoy eating. There is so much going on in the life of a student that we rarely have the time to think about stuff in advance and most often I focus on what am I going to cook once I already feel hungry. In this moment I would much rather have something quick to satisfy my hunger instead of a patiently cooked meal, for which I also need to go grocery shopping for ingredients first.

After encountering this issue way too many times I decided that I need to do something about it. There has to be a way for me to remember all the recipes I know how to cook and also those that I just try out or come up with myself and actually end up enjoying them. Because of this reason I decided to make my own app where I can store and organize all these recipes in a way that I can easily access and use them once I feel hungry. What is most important for me is the relative cost of the meal, the difficulty and the time that I will spend cooking it. I also realised that I probably do not want to eat the same thing over and over again within a short period of time so I decided that I will also store the last time I cooked a recipe. It was a particularly difficult feature to implement but it allows me to also sort the recipes based on when I cooked them last, so that I can avoid recipes that I recently used and pay more attention to those that I have not used in a while.

#### Files Explained:

##### App.py

** This files handles the entire logic of the application. **

- First I had to set up the session storage so that I can store the user in it and later use that stored user in order to save and update to the database only files that are related to the user that is logged in.

- Second most important thing for the entire project is the manipulation of the database. In order to be able to do this I had to initiate connection at the start of the file and at end to commit all changes and close the connection. It was not working properly so I also had to setp up the @app.before_request and @app.teardown_request events and the issues went away.

- Next thing I did was create the entire authentication process which goes about the same for every website. I had to create a register, login and logout routes. For hashing the password and later comparing inputted password to its supposed hash I used the werkzeug.security package. A key part was populating the session storage and also clearing it on logout.

- After this it was time to implement all the routes within the website for the user after they have successfully logged in. These routes include: home page, add recipe page, recipe details page and a history page. Given that I only want to show a user the recipes that they personally added I made all these routes to be @login_reqiured.

- I also have a few additional helper routes that I needed to create for the functionality of the website. I added a sorting route which after selection of a sorting method returns the recipes in a sorted way. Other routes a added are the update and delete recipe routes to make it more useable for users in case of a mistake.

##### Templates:

- layout.html
  The layout page contains the navbar for the most part, along with some Jinja syntax for later populating with page-specific information.

- index.html
  This is the homepage of the application and is also where a user would spend the vast majority of time spent in the website. This is where they see a list of all the recipes they added and also have the ability to sort them alphabetically, and also based on the recipes' price, difficulty, rating and most importantly - last time it was used. There is also a filter on top where users can select which category of recipes they want to look at, making it singificantly easier if, for example, they are looking to make breakfast.

- add.html and update.html
  Here users go in order to add a new recipe. It was particularly challenging to create this page, given all the fields that it requires because a recipes has a lot of components to it. I wanted to make it more interesting so I used a few dropdown menus and then a radio button for the rating. At the end I used a toggle button used to select if the recipe is going to be cooked now or in the future. Update page is almost the same but all fields are already populated with the original information.

- recipe.html
  Details of a chosen recipe are displayed here. It was not easy to put all the information about a recipe in a way that looks good but after many tries I decided to put most of the info in a div with gray background and leave out the name, short description and instructions. This page also features a form toggle button in case a user uses it and wants to save that they used it at this time. One can also update and delete a recipe through this page.

- history.html
  There is not too much going on in this page, it just shows a history of recipes cooked and which is useful if a user wants to look back at what they have been cooking. Clicking on a recipe also brings to recipe details page.

- profile.html
  Currently containts the username of the user logged in.

- apology.html
  This page is rendered in case of an error. It expects an error message and error code and returns a meme with information about the error.

- register.html, login.html
  Here every user starts and needs to login or register in order to access the website.
