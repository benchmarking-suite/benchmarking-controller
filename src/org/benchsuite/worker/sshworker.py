#!/usr/bin/env python
# BenchmarkingSuite - Benchmarking Controller
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)

import os

from org.benchsuite.model.common import TestExecutor
from eu.artist.benchmarking.benchmark import BenchmarkFactory
from org.benchsuite.model.exception import BashCommandExecutionFailedException
from org.benchsuite.util import run_ssh_cmd, ssh_transfer_output


def get_output(vm, cmd):
    exit_status, stdout, stderr = run_ssh_cmd(vm, cmd)
    return stdout

def run_ssh_script(vm, cmd, phase, id, async=False, needs_pty=False):
    name = phase + '-' + id
    script = '/tmp/'+name + '.sh'
    script_wrapper = '/tmp/'+name + '.wrapper.sh'
    lock = '/tmp/'+name +'.lock'
    ret = '/tmp/'+name +'.ret'
    out = '/tmp/'+name + '.out'
    err = '/tmp/'+name + '.err'
    runtime = '/tmp/'+name + '.time'

    working_dir = vm.working_dir + os.path.sep + id

    invocation_cmd = '{0} 2> {2} > {1}'.format(script, out, err)
    if async:
        invocation_cmd = '' + invocation_cmd + ' &'


    decorated_cmd = '''cat << EOF > {0}
touch {1}
mkdir -p {2}
cd {2}
cat << END2 > {3}
{4}
END2
SECONDS=0
bash -e  {3} 1> {5} 2> {6}
echo \$? > {7}
echo \$SECONDS > {8}
rm {1}
exit \`cat {7}\`
EOF
bash {0}'''.format(script, lock, working_dir, script_wrapper, cmd, out, err, ret, runtime)

    # decorated_cmd = 'cat << EOF > {0}\n' \
    #     'touch {1}\n' \
    #     'mkdir -p {5}\n' \
    #     'cd {5}\n' \
    #     'SECONDS=0\n' \
    #     '{2}\n' \
    #     'echo \$SECONDS > {6}\n' \
    #     'rm {1}\n' \
    #     'EOF\n' \
    #     'chmod +x {0}\n' \
    #     '{4}\n' \
    #     'echo $? > {7}'.format(script, lock, cmd, out, invocation_cmd, working_dir, runtime, ret)


    decorated_cmd += '\n'

    exit_status, stdout, stderr = run_ssh_cmd(vm, decorated_cmd, needs_pty=needs_pty)

    if not exit_status == 0:
        # retrieve the standard

        cmd_out = get_output(vm, 'cat ' + out)
        cmd_err = get_output(vm, 'cat ' + err)

        e = BashCommandExecutionFailedException(
            'command {0} exit with status {1}. The output is: "{2}"'.format(cmd, exit_status, stdout))
        e.set_output(cmd_out, cmd_err)
        raise e

    return exit_status, stdout, stderr


class PureRemoteBashExecutor(TestExecutor):

    def __init__(self, execution):
        self.id = execution.id
        self.test = execution.test
        self.env = execution.exec_env
        self.test_scripts = execution.test.scripts

    def install(self):
        vm0 = self.env.vms[0]
        cmd = self.test_scripts.get_install_script(vm0.platform)
        if cmd:
            run_ssh_script(vm0, cmd, 'install', self.id)

        cmd = self.test_scripts.get_postinstall_script(vm0.platform)
        if cmd:
            run_ssh_script(vm0, cmd, 'post-install', self.id)

    def run(self, async=False):
        vm0 = self.env.vms[0]
        cmd = self.test_scripts.get_execute_script(vm0.platform)
        if cmd:
            run_ssh_script(vm0, cmd, 'run', self.id, async=async)

    def collect(self):
        vm0 = self.env.vms[0]
        ssh_transfer_output(vm0, 'run-'+self.id, '/tmp/run-'+self.id+".out")

    def get_runtime(self, phase):
        vm0 = self.env.vms[0]
        cmd = 'cat /tmp/' + phase + '-' + self.id + '.time'
        get_output(vm0, cmd)

    def cleanup(self):
        vm0 = self.env.vms[0]
        cmd = self.test_scripts.get_remove_script(vm0.platform)
        run_ssh_script(vm0, cmd)


