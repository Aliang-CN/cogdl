import importlib
import os

from .base_task import BaseTask


"""
主要是获取所有任务的类名和，导入包
"""


TASK_REGISTRY = {}                  # 类名：类


def register_task(name):                        # 导入task任务包的时候会调用这个
    """
    New task types can be added to cogdl with the :func:`register_task`
    function decorator.

    For example::

        @register_task('node_classification')
        class NodeClassification(BaseTask):
            (...)

    Args:
        name (str): the name of the task
    """

    def register_task_cls(cls):                             # cls 修饰的类
        if name in TASK_REGISTRY:
            raise ValueError("Cannot register duplicate task ({})".format(name))
        if not issubclass(cls, BaseTask):                   # 判断是不是BaseTask的子类
            raise ValueError("Task ({}: {}) must extend BaseTask".format(name, cls.__name__))
        TASK_REGISTRY[name] = cls
        return cls

    return register_task_cls


# automatically import any Python files in the tasks/ directory
for file in os.listdir(os.path.dirname(__file__)):                      # 列出__init__所有文件夹路径所有文件
    if file.endswith(".py") and not file.startswith("_"):
        task_name = file[: file.find(".py")]                            # 把代码名字取出来
        module = importlib.import_module("cogdl.tasks." + task_name)    # 自动导入tasks下面的包，这里导入的包会自动调用register_task


def build_task(args, dataset=None, model=None):
    if dataset is None and model is None:
        return TASK_REGISTRY[args.task](args)
    elif dataset is not None and model is None:
        return TASK_REGISTRY[args.task](args, dataset=dataset)
    elif dataset is None and model is not None:
        return TASK_REGISTRY[args.task](args, model=model)
    return TASK_REGISTRY[args.task](args, dataset=dataset, model=model)
