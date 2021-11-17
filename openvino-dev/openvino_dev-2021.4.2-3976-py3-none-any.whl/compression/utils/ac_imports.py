# Copyright (C) 2020-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0

try:
    from libs.open_model_zoo.tools.accuracy_checker.\
        accuracy_checker.evaluators.quantization_model_evaluator import create_model_evaluator
    from libs.open_model_zoo.tools.accuracy_checker.accuracy_checker.config import ConfigReader
    from libs.open_model_zoo.tools.accuracy_checker.accuracy_checker.dataset import\
        Dataset, DataProvider as DatasetWrapper
    from libs.open_model_zoo.tools.accuracy_checker.accuracy_checker.logging\
        import _DEFAULT_LOGGER_NAME

except ImportError:
    from accuracy_checker.evaluators.quantization_model_evaluator import create_model_evaluator
    from accuracy_checker.config import ConfigReader
    from accuracy_checker.dataset import Dataset
    from accuracy_checker.logging import _DEFAULT_LOGGER_NAME
    try:
        from accuracy_checker.dataset import DataProvider as DatasetWrapper
    except ImportError:
        from accuracy_checker.dataset import DatasetWrapper
