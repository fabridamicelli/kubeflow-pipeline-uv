from kfp import dsl

from component import custom_component

# @dsl.component(
#     base_image="python:3.12",
#     packages_to_install=["scikit-learn"],
# )


@custom_component
def train(
    dataset: dsl.Input[dsl.Dataset],
    predictions: dsl.Output[dsl.Artifact],
):

    import pickle
    from sklearn.linear_model import RidgeClassifier

    with open(dataset.path, mode="rb") as file:
        data = pickle.load(file)

    clf = RidgeClassifier(tol=1e-2, solver="sparse_cg")
    clf.fit(data["X_train"], data["y_train"])
    pred = clf.predict(data["X_test"])

    out = {
        "y_test": data["y_test"],
        "y_pred": pred,
        "target_names": data["target_names"],
    }
    with open(predictions.path, mode="wb") as file:
        pickle.dump(out, file)
