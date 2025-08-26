from kfp import dsl

from component import custom_component


@custom_component
def download_dataset(dataset: dsl.Output[dsl.Dataset]):
    import pickle

    from sklearn.datasets import fetch_20newsgroups
    from sklearn.feature_extraction.text import TfidfVectorizer

    def fetch_data(subset: str):
        categories = ["alt.atheism", "talk.religion.misc", "comp.graphics", "sci.space"]
        return fetch_20newsgroups(
            subset=subset,
            categories=categories,
            shuffle=True,
            random_state=42,
        )

    data_train = fetch_data("train")
    data_test = fetch_data("test")
    y_train, y_test = data_train.target, data_test.target
    vectorizer = TfidfVectorizer(
        sublinear_tf=True, max_df=0.5, min_df=5, stop_words="english"
    )
    X_train = vectorizer.fit_transform(data_train.data)
    X_test = vectorizer.transform(data_test.data)

    out = {
        "X_train": X_train,
        "y_train": y_train,
        "X_test": X_test,
        "y_test": y_test,
        "target_names": data_train.target_names,
    }
    with open(dataset.path, mode="wb") as file:
        pickle.dump(out, file)
