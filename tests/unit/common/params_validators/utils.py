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
Module for unit tests of the utility functions of the util module.
"""

#
# IMPORTS
from tessia_baselib.common.params_validators.utils import create_params_validator
from tessia_baselib.common.params_validators.utils import validate_params
from unittest import mock

import unittest

#
# CONSTANTS AND DEFINITIONS
#
VALIDATOR_NOT_IN_LIBS = "any validator"

#
# CODE
#

class TestUtils(unittest.TestCase):
    """
    Unit tests for the utility functions of parameters validation.
    """
    @mock.patch('tessia_baselib.common.params_validators.utils.CONF',
                autospect=True)
    def test_invalid_params_validator(self, mock_conf):
        """
        Test the case that the default validator is not defined and not
        provided in the factory function arguments

        Args:
            mock_conf: Mock of the configuration dictionary that is created
                       from the configuration file.

        Returns:
            None

        Raises:
            None
        """
        mock_conf.get_config.return_value = {
            "default_schema_validator": None
        }

        self.assertRaisesRegex(ValueError, "not defined in",
                               create_params_validator, "any_schema")
    # test_invalid_params_validator()

    def test_invalid_params_validator_in_arguments(self):
        """
        Test the case that the choosen validator is not valid.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.assertRaisesRegex(ValueError, "is not a valid",
                               create_params_validator, "any_schema",
                               VALIDATOR_NOT_IN_LIBS)
    # test_invalid_params_validator_in_arguments()

    @mock.patch("tessia_baselib.common.params_validators.utils.VALIDATOR_LIBS",
                autospect=True)
    @mock.patch("tessia_baselib.common.params_validators.utils.CONF",
                autospect=True)
    def test_create_params_validator_default(self, mock_conf,
                                             mock_validator_libs):
        """
        Test that the default validator is sucessfuly created

        Args:
            mock_conf: Mock of the dictionary containing the
                       tessia_baselib configuration.
            mock_validator_libs: Mock of the constant dictionary that
                                 contains all the supported json schema
                                 validation libraries.

        Returns:
            None

        Raises:
            None
        """
        mock_conf.get_config.return_value = {
            "default_schema_validator": "my_lib"
        }

        mock_validator_libs.keys.return_value = ["my_lib"]
        mock_my_lib = mock.Mock()

        mock_validator_libs["my_lib"].return_value = mock_my_lib

        lib = create_params_validator("any_file")

        #assert that the default library is properly instantiated
        mock_validator_libs["my_lib"].assert_called_with("any_file")
        #assert that the return value of the function is correct
        self.assertEqual(lib, mock_my_lib)
    # test_create_params_validator_default()

    @mock.patch("tessia_baselib.common.params_validators.utils.VALIDATOR_LIBS",
                autospect=True)
    @mock.patch("tessia_baselib.common.params_validators.utils.CONF",
                autospect=True)
    def test_create_params_validator_argument(self,mock_conf,
                                             mock_validator_libs):
        """
        Test that the validator passed as argument to
        create_params_validator is sucessfuly created.

        Args:
            mock_conf: Mock of the dictionary containing the
                       tessia_baselib configuration.
            mock_validator_libs: Mock of the constant dictionary that
                                 contains all the supported json schema
                                 validation libraries.

        Returns:
            None

        Raises:
            None
        """
        mock_conf.get_config.return_value = {
            "default_schema_validator": "my_lib"
        }

        mock_validator_libs.keys.return_value = ["my_lib", "other_lib"]
        mock_other_lib = mock.Mock()

        mock_validator_libs["other_lib"].return_value = mock_other_lib

        lib = create_params_validator("any_file", "other_lib")

        #assert that the constructor of the library passed as argument is
        #properly instantiated.

        mock_validator_libs["other_lib"].assert_called_with("any_file")

        #assert that the return value of the function is correct

        self.assertEqual(lib, mock_other_lib)

    # test_create_params_validator_argument()

    def test_func_name_is_not_valid(self):
        """
        Test the case that the name of the function being decorated by
        validate_params is not valid.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        mock_func = mock.Mock()

        mock_func.__name__ = "not_valid_function_name"

        self.assertRaisesRegex(NameError, "should only decorate",
                               validate_params, mock_func)
    # test_func_name_is_not_valid()

    @mock.patch("tessia_baselib.common.params_validators.utils.inspect",
                autospect=True)
    def test_func_argument_not_valid(self, mock_inspect):
        """
        Test the case that the argument to be validated is not present
        in the arguments of the function being decorated by
        validate_params.

        Args:
            mock_inspect: Mock of the inspect module

        Returns:
            None

        Raises:
            None
        """
        mock_func = mock.Mock()
        #We use a valid function name here
        mock_func.__name__ = "start"
        func_specs_mock = mock.Mock()
        mock_inspect.getfullargspec.return_value = func_specs_mock
        func_specs_mock.args.index.side_effect = ValueError("foo")

        self.assertRaisesRegex(NameError, "Decorated function does",
                               validate_params, mock_func)
    # test_func_argument_not_valid()

    @mock.patch("tessia_baselib.common.params_validators.utils.inspect",
                autospect=True)
    @mock.patch("tessia_baselib.common.params_validators.utils.os", autospect=True)
    @mock.patch("tessia_baselib.common.params_validators"
                ".utils.create_params_validator", autospect=True)
    @mock.patch("tessia_baselib.common.params_validators"
                ".utils.SCHEMAS_BASE_DIR", new="BASE_DIR")
    def test_validate_params(self, mock_create_params_validator, mock_os,
                             mock_inspect):
        """
        Test that the decorator was properly used.

        Args:
            mock_create_params_validator: Mock of the validator factory
            mock_os: Mock of the os module
            mock_inspect: Mock of the inspect module

        Returns:
            None

        Raises:
            None
        """
        #Mock function that will be decorated
        func_name = "start"
        func = mock.Mock()
        func.__name__ = func_name

        mock_func_specs = mock.Mock()
        mock_inspect.getfullargspec.return_value = mock_func_specs

        #Chooses the index of the argument to be validated
        mock_func_specs.args.index.return_value = 0

        #Create a fake dir name for the function beeing decorated
        mock_os.path.dirname.return_value = "/dir1/dir2"

        #Create a mock parameters_validator using the factory
        mock_validator = mock.Mock()
        mock_create_params_validator.return_value = mock_validator

        #This is the fake full path for the schema
        schema_file = "BASE_DIR/dir2/actions/start.json"

        #call the software under test
        decorated_func = validate_params(func)
        decorated_func(1, 2, 3)

        #Assert that the schema file full path was created correctly
        mock_create_params_validator.assert_called_with(schema_file)

        #Assert that the validator chose the correct parameter based on the
        #index returned by mock_func_specs.args.index
        mock_validator.validate.assert_called_with(1)

        #Assert that the function was called with correct arguments
        func.assert_called_with(1, 2, 3)
    # test_validate_params()
# TestUtils