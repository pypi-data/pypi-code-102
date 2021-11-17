# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from typing import Optional
from elangai.callback import ElangCallback
from elangai.inference import ElangInference
from elangai.utils import FP32


class ElangChainer:
    """Entwining AI model into sequenced pipeline.
    """
    def __init__(self):
        pass

    def add(self, model: str, label: str, callback: Optional[ElangCallback] = None, precision = FP32):
        """Add AI model reference to ``ElangChainer``.

        :param model: the AI model filename
        :param label: the AI model label file
        :param callback: reference to ``ElangCallback`` in accordance with the AI model.
                         If callback is ``None`` the model can only be accessed through ``ELANGAI_ENV``
                         and will not be run as pipeline
        :param precision: the weight precision of AI model
        """
        pass

    def add_inference(self, inference: ElangInference):
        """Add AI model reference to ``ElangChainer`` directly from ``ElangInference``.

        :param inference: the AI model inference instance
        """
        pass

    def remove(self, idx: int):
        """Remove AI model reference from ``ElangChainer`` based on its index.

        :param idx: index to the certain AI model
        """
        pass
