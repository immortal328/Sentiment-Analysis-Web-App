from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
import pandas as pd
import pickle


def load_model():
    model = tf.keras.models.load_model(
        'model_data/imdb_sentiment_analysis.hdf5')
    return model


def load_tokenizer():
    with open('model_data/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    return tokenizer


def get_review_prediction(model, tokenizer):
    df = pd.read_csv('dataframe.csv', sep='|')
    reviews = list(df['Review'])

    max_length = 120
    trunc_type = 'post'

    reviews_sequences = tokenizer.texts_to_sequences(reviews)
    reviews_padded = pad_sequences(reviews_sequences, maxlen=max_length)
    prediction = model.predict(reviews_padded)

    prediction_values = [x[0] for x in prediction]
    positive = [x for x in prediction_values if x > 0.5]
    negative = [x for x in prediction_values if x <= 0.5]

    return len(prediction_values), len(positive), len(negative)


'''
model = load_model()
tokenizer = load_tokenizer()

total, positive, negative = get_review_prediction(model, tokenizer)

print(total, positive, negative)
'''
