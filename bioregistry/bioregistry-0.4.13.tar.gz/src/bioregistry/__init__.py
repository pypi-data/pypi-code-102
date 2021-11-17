# -*- coding: utf-8 -*-

"""Extract registry information."""

from .collection_api import get_collection  # noqa:F401
from .metaresource_api import (  # noqa:F401
    get_registry,
    get_registry_description,
    get_registry_example,
    get_registry_homepage,
    get_registry_name,
    get_registry_provider_uri_format,
    get_registry_uri,
)
from .parse_iri import curie_from_iri, parse_iri  # noqa:F401
from .resolve import (  # noqa:F401
    get_banana,
    get_bioportal_prefix,
    get_contact,
    get_curie_pattern,
    get_default_format,
    get_description,
    get_example,
    get_fairsharing_prefix,
    get_homepage,
    get_identifiers_org_prefix,
    get_json_download,
    get_license,
    get_license_conflicts,
    get_mappings,
    get_miriam_uri_format,
    get_miriam_uri_prefix,
    get_n2t_prefix,
    get_name,
    get_namespace_in_lui,
    get_obo_download,
    get_obofoundry_prefix,
    get_obofoundry_uri_format,
    get_obofoundry_uri_prefix,
    get_ols_prefix,
    get_ols_uri_format,
    get_ols_uri_prefix,
    get_owl_download,
    get_pattern,
    get_preferred_prefix,
    get_prefixcommons_uri_format,
    get_provides_for,
    get_registry_map,
    get_resource,
    get_synonyms,
    get_version,
    get_versions,
    get_wikidata_prefix,
    has_no_terms,
    is_deprecated,
    is_proprietary,
    normalize_curie,
    normalize_parsed_curie,
    normalize_prefix,
    parse_curie,
)
from .resolve_identifier import (  # noqa:F401
    get_bioportal_iri,
    get_bioregistry_iri,
    get_default_iri,
    get_identifiers_org_curie,
    get_identifiers_org_iri,
    get_iri,
    get_link,
    get_n2t_iri,
    get_obofoundry_iri,
    get_ols_iri,
    get_providers,
    get_providers_list,
    is_known_identifier,
)
from .resource_manager import Manager, manager  # noqa:F401
from .schema.struct import Author, Collection, Provider, Registry, Resource  # noqa:F401
from .uri_format import (  # noqa:F401
    get_format_urls,
    get_prefix_map,
    get_uri_format,
    get_uri_prefix,
)
from .utils import (  # noqa:F401
    read_collections,
    read_contributors,
    read_metaregistry,
    read_mismatches,
    read_registry,
    write_registry,
)
