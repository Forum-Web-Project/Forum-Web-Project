## FORUM SYSTEM API

## 1. Description
Design and implementation of a forum web application.
The application is designed to be used by different users to share and discuss different topics and case studies.
The functionality of the application allows to register users, create categories, create topics, send messages between users, vote for or against a particular answer.
User Authentication and Authorization. FastAPI was used for the design of the application following the principles of REST Architecture.

## 2. Application operation


### 🔐 Signup:
<span style="color: green">**This endpoint is used to register a user to our database.** </span>


<span style="color: red"> **Username** </span>

> Enter username:

<span style="color: red"> **Password** </span>

> Enter password:

<span style="color: red"> **Email** </span>

> Enter e-mail: 
****

### 🔑 Login:

<span style="color: green">**This endpoint is used to login with an existing user and get your token.**</span>


<span style="color: red"> **Username** </span>

> Enter username:

<span style="color: red"> **Password** </span>

> Enter password:
****

### 🌏 Topic Section:

<span style="color: green">**Here are a few endpoints and how to use them.** </span>


<span style="color: red"> **Get topics** </span>

> Provides you a list of all the topics with 'sort' and 'search'.

<span style="color: red"> **Get Topic By ID** </span>

> Here you enter a certain topic's ID and it gives you all the information about that topic.

<span style="color: red"> **Create Topic** </span>

> Via this endpoint you can create a topic, you must have your token!
****

### 📝 Category Section:

<span style="color: green">**Here are a few endpoints and how to use them.** </span>


<span style="color: red"> **Get Categories** </span>

> Provides you a list with all the categories with 'sort' and 'search'.

<span style="color: red"> **Get Category By Name** </span>

> Here you enter a certain category's name and it gives you all the information about that category plus the topics that are assigned to it.

<span style="color: red"> **Create Category** </span>

> Creates a category, you must be an "admin" to use this!

<span style="color: red"> **Make Category Private** </span>

> You can use this endpoint to make certain category private or non-private!
****

### 💬 Reply Section:

<span style="color: green">**Here are a few endpoints and how to use them.** </span>


<span style="color: red"> **Get Replies** </span>

> Provides you with a list of all the replies existing (for your ease).

<span style="color: red"> **Create Reply** </span>

> You can reply to a topic [must be logged in with your token].

<span style="color: red"> **Upvote Reply** </span>

> You can upvote a reply using this endpoint.

<span style="color: red"> **Downvote Reply** </span>

> You can downvote a reply using this endpoint.
****

### 📲 Messages Section:

<span style="color: green">**Here are a few endpoints and how to use them.** </span>

<span style="color: red"> **Get Conversation By Username** </span>

> Here you enter the username of the person you want to see your conversation with and your token of course!

<span style="color: red"> **Get Conversations** </span>

> Here you can see all the users with whom you have conversations.

<span style="color: red"> **Create Message** </span>

> Via this endpoint you can message an existing user.

****
Team:
M. STANOYCHEV,
G. DODEKOV,
D. TONEV
****