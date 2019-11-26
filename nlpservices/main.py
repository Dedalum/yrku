"""main file for nlp services"""
import configparser

import flask

import nlpservice.recommend

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/recommend/<string:book_title>', methods=['GET'])
def recommend_handler(book_title):
    """
    Look for a book recommendation based on the given book title.

    Args:
        book_title (string): the title

    Returns:
        string: JSON list of top books recommended
    """
    top_books = app.config['RECOMMENDER'].top_books(flask.escape(book_title))

    return nlpservice.recommend.Recommender.jsonify_recommender_result(
        top_books), 200


@app.errorhandler(404)
def resource_not_found(e):
    """Error 404 handler"""
    return flask.jsonify(error=str(e)), 404


def main():
    """main function"""
    config = configparser.ConfigParser()
    config.read_string("config.ini")

    recommender = nlpservice.recommend.Recommender(config["mysql"]["host"],
                                                   config["mysql"]["user"],
                                                   config["mysql"]["password"],
                                                   config["mysql"]["db"])
    recommender.pre_setup()
    ideal_nb_topics = recommender.ideal_nb_topics(5, 20)
    recommender.setup(nb_topics=ideal_nb_topics)

    app.config['RECOMMENDER'] = recommender
    app.run()


if __name__ == "__main__":
    main()
