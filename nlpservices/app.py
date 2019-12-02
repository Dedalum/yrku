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
        book_title (str): the title

    Returns:
        str: JSON list of top books recommended
    """
    try:
        author = flask.request.args.get("author") if not None else None
        top_books = app.config["RECOMMENDER"].top_books(
            flask.escape(book_title), author=author)
    except Exception as err:
        return resource_not_found(err)

    top_books = app.config["RECOMMENDER"].append_author(top_books)
    return nlpservice.recommend.Recommender.jsonify_recommender_result(
        top_books), 200


@app.errorhandler(404)
def resource_not_found(err):
    """Error 404 handler"""
    return flask.jsonify(error=str(err)), 404


def main():
    """
    main function: 
    - starts an instance of the Recommend class and sets up the
    LSI model to be used. It requires a MySQL DB to be running, filled with 
    training data for preparing the model.
    - once the recommender is set, start the server  
    """
    config = configparser.ConfigParser()
    config.read("config.ini")

    recommender = nlpservice.recommend.Recommender(config["mysql"]["host"],
                                                   config["mysql"]["user"],
                                                   config["mysql"]["password"],
                                                   config["mysql"]["db"])
    recommender.pre_setup()
    ideal_nb_topics = recommender.ideal_nb_topics(5, 15)
    recommender.setup(nb_topics=ideal_nb_topics)

    app.config['RECOMMENDER'] = recommender
    app.run(host=config["app"]["host"])


if __name__ == "__main__":
    main()
