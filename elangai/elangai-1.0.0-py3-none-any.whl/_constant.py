# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


def __validate_precision__(ctx, reference, candidate):
    """Validate if the candidate has the same reference.

    :param reference: precision reference
    :param candidate: precision to be validated
    :return: conditional value of the equality between the candidate and the reference
    """
    candidate = str(candidate)
    return True if str(reference) == candidate else False


def elangai_precision(cls):
    """Register class to the valid elangai precision constant.

    :param cls: class to be registered
    :return: valid elangai precision class
    """
    setattr(cls, __validate_precision__.__name__, __validate_precision__)
    return cls
