# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from os.path import join, dirname


with open(join(dirname(__file__), "version.txt")) as f:
    __version__ = f.read().strip()


__title__ = 'elangai'
__package_name__ = 'elangai'
__description__ = 'elangai is an inference engine platform on edge device.'
__author__ = 'elangai Developer'
__copyright__ = 'Copyright (c) 2021, elangai Developer. All rights reserved'
