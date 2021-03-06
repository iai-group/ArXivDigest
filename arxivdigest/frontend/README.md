# arXivDigest front-end

The front-end (running at http://arxivdigest.org) is implemented as a Flask application.  It provides users with a website for viewing and interacting with the recommendations created for them. The recommendated science papers can be sorted on time intervals such as today, this week, this month and all time. They can also be sorted by title or score. It also includes an admin panel for managing experimental recommender systems.

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

``/savedarticles [GET] @requiresLogin``

>Returns saved articles page with dictionary of saved articles.

``/save/<articleID>/<state> [GET] @requiresLogin``

>Saves or removes articles from web, depending on current state. Returns "Success" or "Fail".

``/mail/save/<int:userID>/<string:articleID>/<uuid:trace> [GET]``

>Saves article directly from email based on userid, articleid and a trace from the email.

``/mail/read/<int:userID>/<string:articleID>/<uuid:trace> [GET]``

>Records if article was clicked from email.

``/click/<string:articleId> [GET] @requiresLogin``

>Records if article was clicked from web. Returns redirect to arXiv info page or article pdf depending on where user clicked.

``/admin [GET] @requiresLogin``

>Return admin page and dictionary of systems in database.

``/systems/get [GET] @requiresLogin``

>Returns list of systems from db.

``/admins/get [GET] @requiresLogin``

>Returns list of admins from db.

``/systems/toggleActive/<int:systemID>/<state> [GET] @requiresLogin``

>Activate/deactivate system with systemID depending on state.

``/general [GET] @requiresLogin``

>Returns number of users and articles.

``/system/register [POST]``

>Sends new systems data from web form to database function. Returns register system page or error.

``/system/register [GET]``

>Returns page for system registration.

``/update_topic/<topic_id>/<state> [PUT]``

>Updates the state of a topic recommended to a user.

``/refresh_topics [GET]``

>Refreshes the list of topics recommended to a user by running the topic interleaving process.

``@requiresLogin``

>Decorator that checks if you are logged in before accessing the route it is used on. If you are not logged in it returns login page and error message.

## Configurations

These are the values that can be configured in the frontend-section of config.json.

- `data_path`: Path where the application will store caches and compiled static files. There will be created folders named 'static' and 'cache' in this location, or if these folders already exist the content will be deleted. Files will be created inside of package install location if left empty.
- `dev_port`: Port the server while be launched on while running in development mode.
- `max_content_length`: Maximum request size.
- `jwt_key`: Secret key for signing JWTs.
- `secret_key`: Secret key used by flask.

## Database

| Tables | Fields |
| ------------- | ------------- |
| users | user_id, email, salted_hash, firstname, lastname, notification_interval, last_recommendation_date, last_email_date, registered, admin, organization, dblp_profile, google_scholar_profile, semantic_scholar_profile, personal_website|
| user_categories | user_id, category_id |
| user_topics | user_id, topic_id, state |
| topics | topic_id, topic, filtered |
| articles | article_id, title, abstract, doi, comments, licence, journal, datestamp |
| article_authors | author_id, article_id, firstname, lastname |
| article_categories | article_id, category_id |
| author_affiliations | author_id, affiliation |
| categories | category_id, category, subcategory, category_name |
| article_recommendations | user_id, article_id, system_id, score, recommendation_date, explanation |
| systems | system_id, api_key, system_name, active, admin_user_id |
| article_feedback | user_id, article_id, system_id, score, recommendation_date, seen_email, seen_web, clicked_email, clicked_web, saved, trace_save_email, trace_click_email, explanation |
| feedback | feedback_id, user_id, article_id, type, feedback_text |
| topic_recommendations | recommendation_id, user_id, topic_id, system_id, datestamp, system_score, interleaving_order, seen, clicked |

## Setup

Read the [Setup guide](../../Setup.md).

## Dependencies

### Python
- [Mysql connector for python](https://dev.mysql.com/doc/connector-python/en/)
- [Json Web Tokens](https://github.com/jpadilla/pyjwt) 
- [Flask](http://flask.pocoo.org/)
- [Passlib](https://passlib.readthedocs.io/en/stable/index.html)

### Javascript
- [Bootstrap 3](https://getbootstrap.com/docs/3.3/)
- [Chart.js](https://www.chartjs.org/)
- [jQuery](https://jquery.com/)
- [jQuery UI](https://jqueryui.com/)
- [MathJax](https://github.com/mathjax/MathJax)
