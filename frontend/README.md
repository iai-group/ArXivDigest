# ArXivDigest front-end

The front-end (running at http://arxivdigest.org) is implemented as a Flask application.  It provides users with a website for viewing and interacting with the recommendations created for them. It also includes an admin panel for managing experimental recommender systems.

## Overview

Routes available:

``/ @requiresLogin``

>Returns index page and dirctionary of index page settings, drop down values and articles as sub dictionary.

``/signup [GET]``

>Returns signup page if you're not logged in. Else returns index page.

``/signup [POST]``

>Goes to signup function. Returns a jwt token and index page if successful. Else returns error message and signup page.

``/logout [GET]``

>Goes to logout function. Logs out user and sets token expires=0. Returns index page.

``/profile [GET] @requiresLogin``

>Returns user profile page with user information.

``/modify [GET] @requiresLogin``

>Returns modify user page.

``/modify [POST] @requiresLogin``

>Returns user profile page if successful. Else return error and modify page.

``/passwordChange [GET] @requiresLogin``

>Returns page for change of password.

``/passwordChange [POST] @requiresLogin``

>Returns profile page if successful. Else returns error and password change page.

``/login [GET]``

>Returns login page if you're not logged in. Else returns index page.

``/login [POST]``

>Returns token in successful login. Else returns error and loginpage.

``/likedarticles [GET] @requiresLogin``

>Returns liked articles page with dictionary of liked articles.

``/like/<articleID>/<state> [GET] @requiresLogin``

>Likes or unlikes articles from web, depending on current state. Returns "Success" or "Fail".

``/mail/like/<int:userID>/<string:articleID>/<uuid:trace> [GET]``

>Likes article directly from email based on userid, articleid and a trace from the email.

``/mail/read/<int:userID>/<string:articleID>/<uuid:trace> [GET]``

>Records if article was clicked from email.

``/click/<string:articleId> [GET] @requiresLogin``

>Records if article was clicked from web. Returns redirect to arxiv info page or article pdf depending on where user clicked.

``/admin [GET] @requiresLogin``

>Return admin page and dictionary of systems in database.

``/addSystem [POST] @requiresLogin``

>Sends new systems name from web form to database function. Returns admin page or "System name already in use" error.

``@requiresLogin``

>Decorator that checks if you are logged in before accessing the route it is used on. If you are not logged in it returns login page and error message.

## Database

| Tables | Fields |
| ------------- | ------------- |
| users | user_ID, email, salted_hash, firstname, lastname, keywords, notification_interval, registered, admin, last_recommendation_date |
| user_categories | user_ID, category_ID |
| user_webpages | user_ID, url |
| articles | article_ID, title, abstract, doi, comments, licence, journal, datestamp |
| article_authors | author_ID, article_ID, firstname, lastname |
| article_categories | article_ID, category_ID |
| author_affiliations | author_ID, affiliation |
| categories | category_ID, category, subcategory, category_name |
| system_recommendations | user_ID, article_ID, system_ID, score, recommendation_date |
| systems | system_ID, api_key, system_name, active |
| user_recommendations | user_ID, article_ID, system_ID, score, recommendation_date, seen_email, seen_web, clicked_email, clicked_web, liked, trace_like_email, trace_click_email |

## Setup

How to deploy a flask application can be found [here](../README.md#Deploying%20a%20flask%20application)

## Dependencies

- [Mysql connector for python](https://dev.mysql.com/doc/connector-python/en/)
- [Json Web Tokens](https://jwt.io/)
- [Flask](http://flask.pocoo.org/)