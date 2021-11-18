"""
Class that provides layers from a given SAM template
"""

import logging
import six

from .provider import LayerProvider, Layer
from .sam_base_provider import SamBaseProvider

LOG = logging.getLogger(__name__)


class SamLayerProvider(LayerProvider):
    """
    Fetches and returns CFC Layers from a SAM Template. The SAM template passed to this provider is assumed
    to be valid, normalized and a dictionary.

    It may or may not contain a layer.
    """

    _SERVERLESS_LAYER = "BCE::Serverless::Layer"
    _DEFAULT_LAYERURI = "."

    def __init__(self, template_dict):
        """
        Initialize the class with SAM template data. The SAM template passed to this provider is assumed
        to be valid, normalized and a dictionary. It should be normalized by running all pre-processing
        before passing to this class. The process of normalization will remove structures like ``Globals``, resolve
        intrinsic layers etc.
        This class does not perform any syntactic validation of the template.

        After the class is initialized, any changes to the ``template_dict`` will not be reflected in here.
        You need to explicitly update the class with new template, if necessary.

        :param dict template_dict: SAM Template as a dictionary
        """

        self.template_dict = SamBaseProvider.get_template(template_dict)
        self.resources = self.template_dict.get("Resources", {})

        LOG.debug("%d resources found in the template", len(self.resources))

        # Store a map of layer name to layer information for quick reference
        self.layers = self._extract_layers(self.resources)

    def get(self, name):
        """
        Returns the layer given name or LogicalId of the layer. Every SAM resource has a logicalId, but it may
        also have a layer name. This method searches only for LogicalID and returns the layer that matches
        it.

        :param string name: Name of the layer
        :return Layer: namedtuple containing the Layer information if layer is found.
                          None, if layer is not found
        :raises ValueError If name is not given
        """

        if not name:
            raise ValueError("Layer name is required")

        return self.layers.get(name)

    def get_all(self):
        """
        Yields all the Lambda layers available in the SAM Template.

        :yields Layer: namedtuple containing the layer information
        """

        for _, layer in self.layers.items():
            yield layer
    

    def deploy(self, client, name):
        """
        Yields all the Lambda layers available in the SAM Template.

        :yields Layer: namedtuple containing the layer information
        """

        layer =  self.layers.get(name)


    @staticmethod
    def _extract_layers(resources):
        """
        Extracts and returns layer information from the given dictionary of SAM resources. This
        method supports layers defined with BCE::Serverless::Layer and BCE::Lambda::Layer

        :param dict resources: Dictionary of SAM resources
        :return dict(string : bsamcli.commands.local.lib.provider.Layer): Dictionary of layer LogicalId to the
            Layer configuration object
        """

        result = {}

        for name, resource in resources.items():

            resource_type = resource.get("Type")
            resource_properties = resource.get("Properties", {})

            if resource_type == SamLayerProvider._SERVERLESS_LAYER:
                result[name] = SamLayerProvider._convert_sam_layer_resource(name, resource_properties)

            # We don't care about other resource types. Just ignore them

        return result

    @staticmethod
    def _convert_sam_layer_resource(name, resource_properties):
        """
        Converts a BCE::Serverless::Layer resource to a Layer configuration usable by the provider.

        :param string name: LogicalID of the resource NOTE: This is *not* the layer name because not all layers
            declare a name
        :param dict resource_properties: Properties of this resource
        :return samcli.commands.local.lib.provider.Layer: Layer configuration
        """

        layer_uri = resource_properties.get("LayerUri")

        # TODO layer_Uri can be a dictionary of BOS Bucket/Key or a BOS URI, neither of which are supported
        if isinstance(layer_uri, dict) or \
                (isinstance(layer_uri, six.string_types) and layer_uri.startswith("bos://")):

            layer_uri = SamLayerProvider._DEFAULT_LAYERURI
            LOG.warning("CFC layer '%s' has specified BOS location for LayerUri which is unsupported. "
                        "Using default value of '%s' instead", name, layer_uri)

        LOG.debug("Found CFC layer with name='%s' and LayerUri='%s'", name, layer_uri)

        return Layer(
            name=name,
            layer_uri=resource_properties.get("LayerUri"),
            compatible_runtimes=resource_properties.get("CompatibleRuntimes"),
            license_info=resource_properties.get("LicenseInfo"),
            description=resource_properties.get("Description"),
        )
