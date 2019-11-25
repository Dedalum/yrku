"""Test for helpers functions"""

import nlpservice.helpers


def test_prefilter_data():
    """
    Test prefilter data
    """
    titles = [
        'The Tell-Tale Heart and Other Writings',
        'The Complete Stories and Poems', 'The Cask of Amontillado',
        'The Pit and the Pendulum', 'The Fall of the House of Usher',
        'The Masque of the Red Death', 'The Black Cat',
        'The Murders in the Rue Morgue', 'The Complete Tales and Poems'
    ]

    expected_filtered_titles = [['tell', 'tale', 'heart', 'write'],
                                ['complet', 'stori', 'poem'],
                                ['cask', 'amontillado'], ['pit', 'pendulum'],
                                ['fall', 'hous', 'usher'],
                                ['masqu', 'red', 'death'], ['black', 'cat'],
                                ['murder', 'rue', 'morgu'],
                                ['complet', 'tale', 'poem']]

    filtered_titles = nlpservice.helpers.prefilter_data(titles)

    assert filtered_titles == expected_filtered_titles
