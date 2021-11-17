TEMPLATE_PROJECT_DIRS = [
    "src/",
    "assets/",
    "tests/",
]

TEMPLATE_PROJECT_FILES = [
    "template/src/endpoints.py",
    "template/assets/model.joblib",
    "template/assets/loans_test.pqt",
    "template/tests/test_accuracy.py",
    "template/tests/test_plausibility.py",
    "template/tests/test_schema.py",
    "template/.gitignore",
    "template/.gitattributes",
    "template/.buildfile",
    "template/.dockerignore",
    "template/README.md",
    "template/requirements.txt",
]


CONFIG_FILE_TEMPLATE = """
# See the full documentation at https://docs.taktile.com/configuring-taktile/deployment-configuration

# If this option is set only commits with a commit message starting
# with the deployment_prefix will be deployed
# deployment_prefix: "#deploy"

# If this option is set commits with a commit message starting
# with the undeployment_prefix will cause an existing Taktile
# deployment to no longer be deployed
# undeployment_prefix: "#undeploy"

service:

  # Rest deployment scaling parameters
  rest:
    # requests determine the size of each replica. CPU should be specified as 'XXXm', where XXX is
    # thousandths of a core, up to 1000. Memory can be specified in base 2 units (Mi or Gi)
    requests:
      cpu: 500m
      memory: 512Mi
    # Maximum and minimum number of replicas to which the REST service is allowed to reach
    # by the auto-scaler
    max_replicas: 1
    # Minimum, or starting number of replicas
    replicas: 1

  # Arrow deployment scaling parameters
  arrow:
    requests:
      cpu: 500m
      memory: 512Mi
    # Arrow replicas are fixed and don't autoscale
    replicas: 1

version: {version}
"""
