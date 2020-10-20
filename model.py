import os
from operator import itemgetter
from statistics import mean, stdev

import tensorflow as tf

def load_model(model_dir):
    """Load a Tensorflow saved model"""
    return tf.saved_model.load(model_dir)

def _predict(saved_model, text):
    """Infer a Tensorflow saved model"""

    content_tensor = tf.constant([text])
    predicted = saved_model.signatures['serving_default'](content_tensor)

    numpy_floats = predicted['scores'][0].numpy()
    languages = predicted['classes'][0].numpy()

    probability_values = (float(value) for value in numpy_floats)

    unsorted_scores = zip(languages, probability_values)
    scores = sorted(unsorted_scores, key=itemgetter(1), reverse=True)
    return scores

def _is_reliable(probabilities):
    """Arbitrary rule to determine if the prediction is reliable:

    The predicted language probability must be higher than
    2 standard deviations from the mean.
    """
    threshold = mean(probabilities) + 2*stdev(probabilities)
    predicted_language_probability = max(probabilities)
    return predicted_language_probability > threshold   

def guess_programming_language(classiffer, code_text):
    """Guess language name and score for new code text from Tensorflow saved model"""

    language_probabilities = _predict(classiffer, code_text)
    probabilities = [value for _, value in language_probabilities]
    if not _is_reliable(probabilities):
        LOGGER.warning('No programming language detected')
        return "Unknown", 0

    language_name, score = language_probabilities[0]
    score = round(score*100, 2)
    return language_name, score             

