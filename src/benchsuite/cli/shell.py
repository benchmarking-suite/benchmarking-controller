# Benchmarking Suite
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

import cmd
import sys
from io import TextIOWrapper, BytesIO

#
# In order to not re-implement all the commands and option parsers, we are re-using here the commands functions and
# parsers already defined in command.py amd argument_parser.py.
# In the reality this shell just wraps the commandline interface. In order to realize some functionalities like the
# cache of the ids of the last session and last execution created, we also do some very fragile hacks (redirect of
# sys.stdout)
#

class BenchsuiteShell(cmd.Cmd):
    """An interacive shell for the Benchmarking Suite"""

    def __init__(self, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)

        self.debug_option = ''
        self.last_session = None
        self.last_execution = None


    def precmd(self, line):
        # replace "-" in the command name with "_"
        tokens = line.split(maxsplit=1)
        tokens[0] = tokens[0].replace('-', '_')
        return ' '.join(tokens)

    def do_set_debug(self, line):
        try:
            lvl = int(line)
        except:
            print('Debug level must be an int in the range 0-3')
            lvl = 0

        if lvl == 0:
            self.debug_option = ''
        elif lvl == 1:
            self.debug_option = '-v'
        elif lvl == 2:
            self.debug_option = '-vv'
        elif lvl == 3:
            self.debug_option = '-vvv'
        else:
            print('Invalid debug level (must be in the range 0-3). Setting it to 0')
        print('Debug option set to ' + self.debug_option)

    def do_new_session(self, line):

        retcode, out = self.__call_cmdline('new-session', line)

        if retcode == 0:
            print('last_session='+out.strip())
            self.last_session = out.strip()
        else:
            print('Command failed.')

    def do_new_exec(self, line):
        if len(line.split()) < 3:
            line = self.last_session + ' ' + line

        retcode, out = self.__call_cmdline('new-exec', line)

        if retcode == 0:
            print('last_execution='+out.strip())
            self.last_execution = out.strip()
        else:
            print('Command failed.')


    def do_prepare_exec(self, line):
        if not line:
            line = self.last_execution
        self.__call_cmdline('prepare-exec', line)

    def do_run_exec(self, line):
        if not line:
            line = self.last_execution
        self.__call_cmdline('run-exec', line)

    def do_list_sessions(self, line):
        self.__call_cmdline('list-sessions', line)


    def do_EOF(self, line):
        return True


    def __call_cmdline(self, command, options):
        # redirect solution comes from https://stackoverflow.com/questions/1218933/can-i-redirect-the-stdout-in-pytho
        # n-into-some-sort-of-string-buffer/19345047#19345047

        cmd = ' '.join([self.debug_option, command, options])
        print('Executing: ' + cmd)
        old_stdout = sys.stdout
        sys.stdout = TextIOWrapper(BytesIO(), sys.stdout.encoding)

        from benchsuite.cli.command import main
        retcode = main(cmd.split())

        sys.stdout.seek(0)
        out = sys.stdout.read()
        sys.stdout.close()
        sys.stdout = old_stdout
        print(out)

        return retcode, out