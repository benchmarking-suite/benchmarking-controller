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
import logging
import os
import sys

from benchsuite.core.model.provider import load_service_provider_from_config_file


OUTPUT = """
2017-10-11 09:30:00,645 - benchsuite.core.sessionmanager - DEBUG - Benchmarking Sessions loaded from /home/ggiammat/.local/share/benchmarking-suite/sessions.dat (60 sessions)
2017-10-11 09:30:00,678 - benchsuite.backend.mongodb - DEBUG - Loading benchsuite.backend.mongodb.MongoDBStorageConnector
2017-10-11 09:30:00,680 - benchsuite.backend.mongodb - INFO - MongoDBStorageConnector created for mongodb://localhost:27019/, db=benchmarking, coll=results
f2f5c6c3-0878-4162-ae14-37ce3fc35d33
2017-10-11 09:30:00,726 - benchsuite.core.sessionmanager - DEBUG - Benchmarking Sessions stored to /home/ggiammat/.local/share/benchmarking-suite/sessions.dat (61 sessions)

last_session=2017-10-11 09:30:00,462 - benchsuite.core.config - DEBUG - Using default configuration directory: /home/ggiammat/.config/benchmarking-suite
2017-10-11 09:30:00,463 - benchsuite.core.config - DEBUG - Using alternative configuration directory: /home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig
2017-10-11 09:30:00,645 - benchsuite.core.sessionmanager - DEBUG - Benchmarking Sessions loaded from /home/ggiammat/.local/share/benchmarking-suite/sessions.dat (60 sessions)
2017-10-11 09:30:00,678 - benchsuite.backend.mongodb - DEBUG - Loading benchsuite.backend.mongodb.MongoDBStorageConnector
2017-10-11 09:30:00,680 - benchsuite.backend.mongodb - INFO - MongoDBStorageConnector created for mongodb://localhost:27019/, db=benchmarking, coll=results
f2f5c6c3-0878-4162-ae14-37ce3fc35d33
2017-10-11 09:30:00,726 - benchsuite.core.sessionmanager - DEBUG - Benchmarking Sessions stored to /home/ggiammat/.local/share/benchmarking-suite/sessions.dat
"""


if __name__ == '__main__':


    import re
    uuidre = re.compile("^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.MULTILINE)
    result = uuidre.findall(OUTPUT)
    print(result)
