# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from elangai.template._utils import UTILS


class AppGenerator:
    def _generate_base_dir_(self, app_name: str):
        UTILS.MKDIR(app_name)
        for directory in UTILS.IMPORTANT_DIR:
            UTILS.MKDIR(UTILS.JOIN(app_name, directory))

    def __getitem__(self, app_name: str):
        self._generate_base_dir_(app_name)
        for root, dirs, files in UTILS.CRAWL(UTILS.TEMPLATE_DIR):
            for filename in files:
                if filename.endswith(('.pyo', '.pyc', '.py.class')):
                    continue

                old_path = UTILS.JOIN(root, filename)
                relative_dir = UTILS.RELATIVE_DIR(app_name, root)

                filename = UTILS.NEW_NAME(filename)
                new_data = UTILS.NEW_DATA(app_name, old_path)
                new_path = UTILS.JOIN(relative_dir, filename)

                UTILS.COPY(new_data, new_path)
