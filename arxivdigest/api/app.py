# -*- coding: utf-8 -*-

__author__ = 'Øyvind Jekteberg and Kristian Gingstad'
__copyright__ = 'Copyright 2020, The arXivDigest project'

from datetime import datetime

from flask import Flask
from flask import g
from flask import jsonify
from flask import make_response
from flask import request

import arxivdigest.api.database as db
import arxivdigest.api.validator as validation
from arxivdigest.api.utils import CustomJSONEncoder
from arxivdigest.api.utils import getUserlist
from arxivdigest.api.utils import validateApiKey
from arxivdigest.core.config import config_api

from arxivdigest.core.config import CONSTANTS

app = Flask(__name__)

app.config.update(**config_api)
app.json_encoder = CustomJSONEncoder


@app.route('/user_feedback/articles', methods=['GET'])
@validateApiKey
@getUserlist
def user_feedback_articles(users):
    """API-endpoint for requesting user_feedback for articles, 'user_id' must be
    one or more ids separated by comma."""
    return jsonify(db.get_user_feedback_articles(users))


@app.route('/user_feedback/topics', methods=['GET'])
@validateApiKey
@getUserlist
def user_feedback_topics(users):
    """API-endpoint for requesting user feedback for topics, 'user_id' must be
    one or more ids separated by comma."""
    return jsonify(db.get_user_feedback_topics(users))


@app.route('/users', methods=['GET'])
@validateApiKey
def users():
    """API-endpoint for fetching userIDs, ids will be returned in batches
    starting from 'fromID'.
    If 'fromID' is unspecified 0 will be used as default."""
    try:
        fromID = int(request.args.get('from', 0))
        if fromID < 0:
            return make_response(jsonify({'error': '"from" must be positive'}), 400)
    except Exception:
        err = '"from" must be an integer'
        return make_response(jsonify({'error': err}), 400)

    users = db.getUserIDs(fromID, app.config['max_userid_request'])
    return make_response(jsonify({'users': users}), 200)


@app.route('/user_info', methods=['GET'])
@validateApiKey
@getUserlist
def user_info(users):
    """API-endpoint for requesting userdata, 'user_id' must be one or more ids
    separated by comma."""
    return make_response(jsonify({'user_info': db.getUsers(users)}), 200)


@app.route('/articles', methods=['GET'])
@validateApiKey
def articles():
    """API-endpoint for requesting articleIDs of articles from the last 7
    days."""
    return make_response(jsonify({
        'articles': db.get_article_ids_past_seven_days()}), 200)


@app.route('/article_data', methods=['GET'])
@validateApiKey
def article_data():
    """API-endpoint for requesting article_data, 'article_id' must be one or
    more ids separated by comma."""
    try:
        ids = request.args.get('article_id').split(',')
    except Exception:
        return make_response(jsonify({'error': 'No IDs supplied.'}, 400))
    if (len(ids) > app.config['max_articledata_request']):
        err = 'You cannot request more than %s articles at a time.' % app.config[
            'max_articledata_request']
        return make_response(jsonify({'error': err}), 400)

    articles = db.checkArticlesExists(ids)
    if len(articles) > 0:
        err = 'Could not find articles with ids: %s.' % ', '.join(articles)
        return make_response(jsonify({'error': err}), 400)

    articles = db.get_article_data(ids)
    return make_response(jsonify({'articles': articles}), 200)

@app.route('/topics', methods=['GET'])
@validateApiKey
def topics():
    """API-endpoint for requesting a list of all topics currently
    stored in arXivDigest."""
    topics = db.get_topics()
    return make_response(jsonify({'topics': topics}), 200)

@app.route('/recommendations/articles', methods=['POST'])
@validateApiKey
@validation.validate_json(validation.article_recommendation)
def make_article_recommendations():
    """API-endpoint for inserting article recommendations"""
    data = request.get_json().get('recommendations')
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    data = [(k, v['article_id'], g.sysID, v['explanation'], v['score'], now)
            for k, v in data.items() for v in v]

    db.insert_article_recommendations(data)
    return make_response(jsonify({'success': True}), 200)


@app.route('/recommendations/topics', methods=['POST'])
@validateApiKey
@validation.validate_json(validation.topic_recommendation)
def make_topic_recommendations():
    """API-endpoint for inserting topic recommendations"""
    json = request.get_json().get('recommendations')

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    data = []
    for user, recommendations in json.items():
        for recommendation in recommendations:
            data.append({'user_id': user,
                         'topic': recommendation['topic'],
                         'system_id': g.sysID,
                         'date': now,
                         'score': recommendation['score']})

    db.insert_topic_recommendations(data)
    return make_response(jsonify({'success': True}), 200)


@app.route('/recommendations/articles', methods=['GET'])
@validateApiKey
@getUserlist
def get_article_recommendations(users):
    """API-endpoint for requesting user-recommendations of articles,
     "user_id" must be one or more ids separated by comma."""
    users = db.get_article_recommendations(users)
    return make_response(jsonify({'users': users}), 200)


@app.route('/recommendations/topics', methods=['GET'])
@validateApiKey
@getUserlist
def get_topic_recommendations(users):
    """API-endpoint for requesting user-recommendations of topics,
     "user_id" must be one or more ids separated by comma."""
    topic_recommendations = db.get_topic_recommendations(users)
    return make_response(jsonify({'users': topic_recommendations}), 200)


@app.route('/', methods=['GET'])
def info():
    """Info response."""
    settings = {
        'user_ids_per_request': config_api['max_userid_request'],
        'max_userinfo_request': config_api['max_userinfo_request'],
        'max_articledata_request': config_api['max_articledata_request'],
        'max_users_per_recommendation': config_api[
            'max_users_per_recommendation'],
        'max_recommendations_per_user': config_api[
            'max_recommendations_per_user'],
        'max_explanation_len': config_api['max_explanation_len'],
        'max_topic_len': CONSTANTS.max_topic_length
    }

    return make_response(jsonify({'info': 'This is the arXivDigest API',
                                  'settings': settings}), 200)


@app.teardown_appcontext
def teardownDb(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    app.run(port=config_api.get('dev_port'), debug=True)
