# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai._constant import elangai_precision


@elangai_precision
class PRECISION:
    def __init__(self, precision: str):
        self._precision = precision

    def __repr__(self):
        return self._precision

    def __eq__(self, precision):
        return self.__validate_precision__(self, precision)


INT8 = PRECISION("uint8")
FP16 = PRECISION("float16")
FP32 = PRECISION("float32")
