"""
Execution of package and deploy command
"""

import logging
import base64
import os
import zipfile
import click

from bsamcli.lib.baidubce.services.cfc.cfc_client import CfcClient
from bsamcli.lib.baidubce.bce_client_configuration import BceClientConfiguration
from bsamcli.lib.baidubce.exception import BceServerError
from bsamcli.lib.baidubce.exception import BceHttpClientError

from bsamcli.commands.exceptions import UserException
from bsamcli.local.lambdafn.exceptions import FunctionNotFound, LayerNotFound
from bsamcli.lib.samlib.cfc_credential_helper import get_credentials
from bsamcli.lib.samlib.cfc_deploy_conf import get_region_endpoint

from bsamcli.lib.samlib.deploy_context import DeployContext
from bsamcli.lib.samlib.user_exceptions import DeployContextException
from bsamcli.local.docker.cfc_container import Runtime

LOG = logging.getLogger(__name__)


def execute_pkg_command(resource=None, template=None):
    function_found, layer_found = True, True
    with DeployContext(template_file=template, resource_identifier=resource) as context:
        try:
            for f in context.all_functions:
                codeuri = warp_codeuri(f)
                zip_up(codeuri, f.name, os.path.dirname(template), True)
        except FunctionNotFound as ex:
            function_found = False
        
        try:
            for l in context.all_layers:
                zip_up(l.layer_uri, l.name, os.path.dirname(template))
        except LayerNotFound as ex:
            layer_found = False

    if (not function_found) and (not layer_found):
        resource = "Resource" if resource is None else "Resource " + resource
        raise UserException("%s not found in template yaml" % resource)


def execute_deploy_command(resource=None, region=None, endpoint=None, 
    only_config=None, template=None):
    client_endpoint = endpoint if endpoint is not None else get_region_endpoint(region)
    cfc_client = CfcClient(BceClientConfiguration(credentials=get_credentials(), endpoint=client_endpoint))

    with DeployContext(template_file=template,resource_identifier=resource) as context:
        try:
            try:
                for function in context.all_functions:
                    do_deploy(context, cfc_client, function, only_config, template)
            except FunctionNotFound as ex:
                LOG.debug('FunctionNotFound: %s' % str(ex))
        
            try:
                for layer in context.all_layers:
                    do_deploy_layer(context, cfc_client, layer, template)
            except LayerNotFound as ex:
                LOG.debug('LayerNotFound: %s' % str(ex))        

        except (BceServerError, BceHttpClientError) as ex:
            LOG.debug('BceHttpClientError: %s' % ex)
            raise UserException(parse_bce_error(ex.last_error))
        except Exception as ex:
            raise ex

def do_deploy(context, cfc_client, function, only_config, template):
    validate_runtime(function.runtime)
    existed = check_if_exist(cfc_client, function.name)
    zip_dir = os.path.dirname(template)
    base64_file = get_function_base64_file(zip_dir, function.name)

    if existed:
        update_function(cfc_client, function, base64_file, only_config)
        # TODO update triggers when update
    else:
        create_function(cfc_client, function, base64_file)
        create_triggers(cfc_client, function, context)


def do_deploy_layer(context, cfc_client, layer, template):
    zip_dir = os.path.dirname(template)
    base64_file = get_function_base64_file(zip_dir, layer.name)

    ret = context.deploy_layer(cfc_client, layer, base64_file)    
    LOG.info("Layer %s deployed, layerBrn is %s" % (layer.name, ret.LayerVersionBrn))

def check_if_exist(cfc_client, resource):
    try:
        get_function_response = cfc_client.get_function(resource)
        LOG.debug("Get function response:%s", get_function_response)
    except (BceServerError, BceHttpClientError):
        LOG.debug("Get function exceptioned")
        return False

    return True


def create_function(cfc_client, function, base64_file):
    cfc_client.create_function(function.name, base64_file, function.properties)    
    LOG.info("Function %s created", function.name)

def update_function(cfc_client, function, base64_file, only_config):    
    if only_config:
        LOG.info("Skip update function %s code" % function.name)
    else:
        cfc_client.update_function_code(function.name, zip_file=base64_file)
        LOG.info("Function %s code updated" % function.name)

    cfc_client.update_function_configuration(function.name, function.properties)
    LOG.info("Function %s configuration updated", function.name)

def get_function_base64_file(zip_dir, resource):
    zipfile_name = resource + '.zip'

    zipfile = os.path.join(zip_dir, zipfile_name)

    # 从 template.yaml 所在路径找
    if not os.path.exists(zipfile):
        raise DeployContextException("Zip file not found : {}".format(zipfile))

    with open(zipfile, 'rb') as fp:
        try:
            return base64.b64encode(fp.read()).decode("utf-8")
        except ValueError as ex:
            raise DeployContextException("Failed to convert zipfile to base64: {}".format(str(ex)))

def zip_up(code_uri, zipfile_name, target_dir, is_zip_function = False):
    if code_uri is None:
        raise DeployContextException("Missing the file or the directory to zip up : {} is not valid".format(code_uri))

    target = os.path.join(target_dir, zipfile_name + '.zip')
    z = zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED)

    if os.path.isfile(code_uri):
        z.write(code_uri, os.path.basename(code_uri))
    else:
        for dirpath, dirnames, filenames in os.walk(code_uri):
            fpath = dirpath.replace(code_uri, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                if 'site-packages' in fpath and is_zip_function:
                    fpath = fpath.replace('site-packages/','')
                z.write(os.path.join(dirpath, filename), fpath + filename)

    LOG.info('%s zip suceeded!', zipfile_name)
    z.close()

def validate_runtime(func_runtime):
    if not Runtime.has_value(func_runtime):
        raise ValueError("Unsupported CFC runtime {}".format(func_runtime))
    return func_runtime


def create_triggers(cfc_client, function, context):
    func_config = cfc_client.get_function_configuration(function.name)
    LOG.debug("get function ret is: %s", func_config)
    context.deploy(cfc_client, func_config)


def warp_codeuri(f):
    LOG.debug("f.runtime is: %s", f.runtime)
    if f.runtime == "dotnetcore2.2":
        new_uri = os.path.join(f.codeuri, "bin", "Release", "netcoreapp2.2", "publish/")
        return new_uri
    return f.codeuri

def parse_bce_error(ex):
    last = None
    ex = str(ex)

    for line in ex.split('>>>>'):
        last = line

    for msg in last.split('BceServerError:'):
        last = msg

    return last
