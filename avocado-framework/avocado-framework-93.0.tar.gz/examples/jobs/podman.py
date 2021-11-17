#!/usr/bin/env python3
import sys

from avocado.core.job import Job

job_config = {'resolver.references': ['/bin/true'],
              'nrunner.spawner': 'podman'}

with Job.from_config(job_config=job_config) as job:
    sys.exit(job.run())
