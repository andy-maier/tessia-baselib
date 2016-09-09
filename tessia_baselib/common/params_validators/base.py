# Copyright 2016, 2017 IBM Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Module for BaseParamsValidator class
"""

#
# IMPORTS
#
from tessia_baselib.config import CONF

import json
import os

#
# CONSTANTS AND DEFINITIONS
#

#
# CODE
#

class BaseParamsValidator(object):
    """
    This is the base class for implementation of validators that validate
    parameters using json schemas. We choose to provide a common interface
    in order to allow the implementation of different validatators.
    """

    def __init__(self, schema_file):
        """
        Initialize the instance variables, load and check the json schema.
        Args:
            sechema_file: File containing the json schema that will be used to
                          validate parameters.

        Returns:
            None

        Raises:
            ValueError: In case the schema contained in schema_file is not
                        valid.
        """

        #Open file and load json schema.
        #We expect to have a FileNotFound exception raised if the schema file
        #does not exist, or a ValueError if the json contained in the file is
        #is not valid.
        self.schema = None
        fp = open(schema_file, "r")
        self.schema = json.load(fp)

        #create the id property that is reference for all definitions in the
        #json schema.
        self.schema['id'] = "file://" + os.path.abspath(schema_file)

        #Validate the loaded schema. This method is implemented according
        #to the library that is used to handle json schema.
        self._check_schema()
    # __init__()

    def _check_schema(self):
        """
        Checks if the loaded json schema is valid. This method is dependent of
        the chosen library that implement json schema validation.
        Args:
            None

        Returns:
            None

        Raises:
            ValueError: if the json schema loaded is not valid.
        """
        raise NotImplementedError()
    # _check_schema()

    def validate(self, parameters):
        """
        Validate parameters against the loaded json schema. This method is
        dependent of the chosen library that implement json schema validation.
        Args:
            parameters: A dictionary that will be validated.

        Returns:
            None

        Raises:
            ValueError: If parameters fails to validate against the loaded json
                        schema.
        """
        raise NotImplementedError()
    # validate()
# BaseParamsValidator