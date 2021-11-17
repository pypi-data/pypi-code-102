import random
import re
from typing import Text

from appyratus.files import File

from .load_data import get_species_data


class SpeciesNameGenerator:
    """
    A silly class that just generates common names for ficticious species.
    """

    def __init__(self, filepath: Text = None):
        """
        Load unique species names.
        """

        if not filepath:
            # no filepath provided, use build-in species data
            text = get_species_data()
        else:
            # attempt to read from file
            text = File.read(filepath)

        matches = re.finditer(r'\s*C=(.+)$', text, re.M)
        unique_names = set()

        for match in matches:
            name = match.groups()[0]
            is_acronym = all(c.isupper() for c in name)
            is_alphanumeric = bool(re.search(r'[0-9]', name))
            if not (is_acronym or is_alphanumeric):
                unique_names.add(name)

        self.names = list(unique_names)

    def generate(self, count=100):
        """
        A generator that yields `count` new species names.
        """
        for _ in range(count):
            yield self._generate_name()

    def _generate_name(self):
        """
        Return a new species name.
        """
        name1 = random.choice(self.names)
        name2 = random.choice(self.names)
        name1_parts = name1.split()
        name2_parts = name2.split()

        is_name1_multiword = len(name1_parts) > 1
        is_name2_multiword = len(name2_parts) > 1

        new_name = None

        if is_name1_multiword and is_name2_multiword:
            if random.randint(0, 1):
                new_name = ' '.join(name1_parts[:-1] + [name2_parts[-1]])
            else:
                new_name = ' '.join(name2_parts[:-1] + [name1_parts[-1]])
        elif (not is_name1_multiword) and is_name2_multiword:
            new_name = ' '.join(name2_parts[:-1] + [name1_parts[-1]])
        elif is_name1_multiword and (not is_name2_multiword):
            new_name = ' '.join(name1_parts[:-1] + [name2_parts[-1]])

        return new_name
