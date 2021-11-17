import pkg_resources


def get_species_data():
    """
    Load species data provided by the module
    """
    return pkg_resources.resource_string(__name__, 'data/species.txt').decode()
