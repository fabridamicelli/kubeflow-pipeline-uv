from kfp import dsl, local

from components import download_dataset, train, plot_confusion_matrix


@dsl.pipeline
def pipeline():
    dataset_task = download_dataset()
    train_task = train(dataset=dataset_task.outputs["dataset"])
    plot_task = plot_confusion_matrix(predictions=train_task.outputs["predictions"])


if __name__ == "__main__":
    local.init(local.DockerRunner())
    pipeline()
