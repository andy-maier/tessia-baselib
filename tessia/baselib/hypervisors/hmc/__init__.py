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
Expose the class which implements the hypervisor interface for HMC
"""

#
# IMPORTS
#
from tessia.baselib.hypervisors.hmc.hmc import HypervisorHmc

#
# CONSTANTS AND DEFINITIONS
#

#
# CODE
#

# the hypervisor class to expose to the factory
Hypervisor = HypervisorHmc