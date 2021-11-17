# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai.utils._logging import ELANGAI_ERROR


class NotFoundError(Exception):
    """Exception raised for errors in the case of file not found.

    :param message: message of the exception
    """
    def __init__(self, *message):
        super().__init__(*message)
        self.message = message if len(message) else "File not Found!"

    def __repr__(self):
        return self.message
