from kfp import dsl

from component import custom_component


# @dsl.component(
#     base_image="python:3.12",
#     packages_to_install=["scikit-learn", "matplotlib", "seaborn"],
# )


@custom_component
def plot_confusion_matrix(
    predictions: dsl.Input[dsl.Artifact],
    confusion_plot: dsl.OutputPath(str),
):
    import pickle

    import matplotlib.pyplot as plt
    from sklearn.metrics import ConfusionMatrixDisplay
    import seaborn as sns

    sns.set_theme(style="white", font_scale=1.2)

    with open(predictions.path, mode="rb") as file:
        preds = pickle.load(file)

    fig, ax = plt.subplots(figsize=(10, 5))
    ConfusionMatrixDisplay.from_predictions(preds["y_test"], preds["y_pred"], ax=ax)
    ax.xaxis.set_ticklabels(preds["target_names"])
    ax.yaxis.set_ticklabels(preds["target_names"])
    ax.set_title("Confusion Matrix")
    fig.savefig(confusion_plot)
    plt.close()
