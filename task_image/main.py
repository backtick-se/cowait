import os
import sys
import json
import pipeline.worker
from pipeline.engine import get_cluster_provider

# cluster provider
provider_type = os.environ.get('TASK_CLUSTER_PROVIDER', 'docker')
provider_args = json.loads(os.environ.get('TASK_CLUSTER_ARGUMENTS', '{}'))
print('cluster provider:', provider_type)
print('provider arguments:', provider_args)

ClusterProvider = get_cluster_provider(provider_type)
provider = ClusterProvider(**provider_args)

# inputs
task = json.loads(os.environ.get('TASK_DEFINITION', '{}'))
print('task:', task)

task_name = sys.argv[1]
pipeline.worker.execute(task_name, provider, task)
