# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from typing import Optional
from elangai.callback import ElangCallback


class ElangInference:
    """Inference engine of :py:mod:`~elangai`.

    :param model_path: path to the AI model file
    :param precision: AI model precision
    :param label: label in accordance with the AI model
    :param callback: ``ElangCallback`` reference with the respect to the AI model,
                     if ``None`` this instance is callable via ``ELANGAI_ENV``
    """
    def __init__(self, model_path: str, precision: str, label: str, callback: Optional[ElangCallback] = None):
        pass

    def predict(self, input: dict):
        """Run the inference.

        :param input: dictionary with key-value pair of its respective input tensor
        :return: dictionary with key-value pair of its respective output tensor
        """
        pass
