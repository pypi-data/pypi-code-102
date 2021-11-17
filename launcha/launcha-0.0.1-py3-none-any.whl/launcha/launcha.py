import argparse
import subprocess
import time
from distutils.util import strtobool

import boto3
import requests
import wandb
import launcha
import os
import shutil

def parse_args():
    # fmt: off
    parser = argparse.ArgumentParser(description='Launcha CLI')
    subparsers = parser.add_subparsers(dest='subcommand')
    init = subparsers.add_parser('init', help='initialize the terraform template in the current folder')
    
    parser.add_argument('-d', '--docker-tag', type=str, default="vwxyzjn/cleanrl:latest",
        help='the name of the docker tag')
    parser.add_argument('--command', type=str, default="poetry run python cleanrl/ppo.py",
        help='the docker command')

    # Wandb args for experiment management
    parser.add_argument('--wandb-key', type=str, default="",
        help='the wandb key. If not provided, the script will try to read from `netrc`')

    # AWS Batch args for experiment submission
    parser.add_argument('--job-queue', type=str, default="m6gd-medium",
        help='the name of the job queue')
    parser.add_argument('--num-vcpu', type=int, default=1,
        help='number of vcpu per experiment')
    parser.add_argument('--num-memory', type=int, default=2000,
        help='number of memory (MB) per experiment')
    parser.add_argument('--num-gpu', type=int, default=0,
        help='number of gpu per experiment')
    parser.add_argument('--num-hours', type=float, default=16.0,
        help='number of hours allocated experiment')
    parser.add_argument('-b', '--build', type=lambda x:bool(strtobool(x)), default=False, nargs='?', const=True,
        help='if toggled, the script will build a container')
    parser.add_argument('--archs', type=str, default="linux/amd64", # linux/arm64,linux/amd64
        help='the archs to build the docker container for')
    parser.add_argument('-p', '--push', type=lambda x:bool(strtobool(x)), default=False, nargs='?', const=True,
        help='if toggled, the script will push the built container')
    parser.add_argument('--provider', type=str, default="", choices=["aws"],
        help='the cloud provider of choice (currently only `aws` is supported)')
    parser.add_argument('--aws-num-retries', type=int, default=1,
        help='the number of job retries for `provider=="aws"`')
    args = parser.parse_args()
    # fmt: on
    return args

def main():
    args = parse_args()
    if args.subcommand == "init":
        shutil.copytree(os.path.join(launcha.__path__[0], 'template'), ".", dirs_exist_ok=True)
        print("""
Terraform template files initialized. Spin up the AWS computing environments by running:
`terraform init`
`terraform apply`
The computing environments' setup is free of charge. You will only be billed when you submit jobs.
        """)
        return

    if args.build:
        output_type_str = "--output=type=registry" if args.push else "--output=type=docker"
        subprocess.run(
            f"docker buildx build {output_type_str} --platform {args.archs} -t {args.docker_tag} .",
            shell=True,
            check=True,
        )

    if not args.wandb_key:
        try:
            args.wandb_key = requests.utils.get_netrc_auth("https://api.wandb.ai")[-1]
        except:
            pass
    assert len(args.wandb_key) > 0, "you have not logged into W&B; try do `wandb login`"

    final_run_cmds = [args.command]

    for final_run_cmd in final_run_cmds:
        run_command = (
            f'docker run -d -e WANDB_API_KEY={args.wandb_key} {args.docker_tag} '
            + '/bin/bash -c "'
            + final_run_cmd
            + '"'
            + "\n"
        )
        print(run_command)

    # submit jobs
    if args.provider == "aws":
        client = boto3.client("batch")
        for final_run_cmd in final_run_cmds:
            job_name = args.docker_tag.replace(":", "").replace("/", "_").replace(" ", "").replace("-", "_") + str(
                int(time.time())
            )
            resources_requirements = []
            if args.num_gpu:
                resources_requirements = [
                    {"value": str(args.num_gpu), "type": "GPU"},
                ]
            try:
                job_def_name = args.docker_tag.replace(":", "_").replace("/", "_")
                client.register_job_definition(
                    jobDefinitionName=job_def_name,
                    type="container",
                    containerProperties={
                        "image": args.docker_tag,
                        "vcpus": args.num_vcpu,
                        "memory": args.num_memory,
                        "command": [
                            "/bin/bash",
                        ],
                    },
                )
                response = client.submit_job(
                    jobName=job_name,
                    jobQueue=args.job_queue,
                    jobDefinition=job_def_name,
                    containerOverrides={
                        "vcpus": args.num_vcpu,
                        "memory": args.num_memory,
                        "command": ["/bin/bash", "-c", final_run_cmd],
                        "environment": [
                            {"name": "WANDB_API_KEY", "value": args.wandb_key},
                            {'name': 'WANDB_RESUME', 'value': 'allow'},
                            {'name': 'WANDB_RUN_ID', 'value': wandb.util.generate_id()},
                        ],
                        "resourceRequirements": resources_requirements,
                    },
                    retryStrategy={"attempts": args.aws_num_retries},
                    timeout={"attemptDurationSeconds": int(args.num_hours * 60 * 60)},
                )
                if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    print(response)
                    raise Exception("jobs submit failure")
            except Exception as e:
                print(e)
            finally:
                response = client.deregister_job_definition(jobDefinition=job_def_name)
                if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                    print(response)
                    raise Exception("jobs submit failure")
