import pickle

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from .normalize import normalize_text

# загружаем сохраненные модель и векторизатор

model = pickle.load(open("model/logref_model.sav", 'rb'))
vectorizer: TfidfVectorizer = pickle.load(open("model/vectorizer.pk", "rb"))


def get_intent(text):
    # векторизируем текст
    vector = vectorizer.transform([normalize_text(text)]).toarray()

    probability_distribution = model.predict_proba(vector)
    print(probability_distribution)

    if np.max(probability_distribution) > 0.5:
        return model.predict(vector)[0]

    return "UNKNOWN"


if __name__ == '__main__':
    print(model.classes_)
    print(get_intent("у вас парковка закрывается на обед"))
