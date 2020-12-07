# Copyright 2015-2016 Yelp Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os

from behave import then
from behave import when
from itest_utils import get_service_connection_string
from itest_utils import update_context_marathon_config

from paasta_tools.util.names import decompose_job_id
from paasta_tools.utils import _run


@when('we delete a marathon app called "{job_id}" from "{cluster_name}" soa configs')
def delete_apps(context, job_id, cluster_name):
    context.job_id = job_id
    (service, instance, _, __) = decompose_job_id(job_id)
    context.service = service
    context.instance = instance
    context.zk_hosts = "%s/mesos-testcluster" % get_service_connection_string(
        "zookeeper"
    )
    update_context_marathon_config(context)
    context.app_id = context.marathon_complete_config["id"]
    os.remove(f"{context.soa_dir}/{service}/marathon-{cluster_name}.yaml")
    os.remove(f"{context.soa_dir}/{service}/deployments.json")
    os.rmdir(f"{context.soa_dir}/{service}")


@then(
    'we run cleanup_marathon_apps{flags} which exits with return code "{expected_return_code}"'
)
def run_cleanup_marathon_job(context, flags, expected_return_code):
    cmd = f"python -m paasta_tools.cleanup_marathon_jobs --soa-dir {context.soa_dir} {flags}"
    print("Running cmd %s" % (cmd))
    exit_code, output = _run(cmd)
    print(output)

    assert exit_code == int(expected_return_code)
