# Copyright 2018 Google LLC
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

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import synthtool.languages.ruby as ruby
import logging
from subprocess import call

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

v1alpha2 = gapic.ruby_library(
    'irm', 'v1alpha2',
    artman_output_name='google-cloud-ruby/google-cloud-irm',
    private=True,
    config_path='artman_irm_v1alpha2.yaml'
)
s.copy(v1alpha2 / 'acceptance')
s.copy(v1alpha2 / 'lib')
s.copy(v1alpha2 / 'test')
s.copy(v1alpha2 / 'README.md')
s.copy(v1alpha2 / 'LICENSE')
s.copy(v1alpha2 / '.gitignore')
s.copy(v1alpha2 / '.yardopts')
s.copy(v1alpha2 / 'google-cloud-irm.gemspec', merge=ruby.merge_gemspec)

# https://github.com/googleapis/gapic-generator/issues/2243
s.replace(
    'lib/google/cloud/irm/*/*_client.rb',
    '(\n\\s+class \\w+Client\n)(\\s+)(attr_reader :\\w+_stub)',
    '\\1\\2# @private\n\\2\\3')

# https://github.com/googleapis/gapic-generator/issues/2279
s.replace(
    'lib/**/*.rb',
    '\\A(((#[^\n]*)?\n)*# (Copyright \\d+|Generated by the protocol buffer compiler)[^\n]+\n(#[^\n]*\n)*\n)([^\n])',
    '\\1\n\\6')

# https://github.com/googleapis/gapic-generator/issues/2323
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://github\\.com/GoogleCloudPlatform/google-cloud-ruby',
    'https://github.com/googleapis/google-cloud-ruby'
)
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://googlecloudplatform\\.github\\.io/google-cloud-ruby',
    'https://googleapis.github.io/google-cloud-ruby'
)

# https://github.com/googleapis/gapic-generator/issues/2393
s.replace(
    'google-cloud-irm.gemspec',
    'gem.add_development_dependency "rubocop".*$',
    'gem.add_development_dependency "rubocop", "~> 0.64.0"'
)

# Require the helpers file
s.replace(
    f'lib/google/cloud/irm/v1alpha2.rb',
    f'require "google/cloud/irm/v1alpha2/incident_service_client"',
    '\n'.join([
        f'require "google/cloud/irm/v1alpha2/incident_service_client"',
        f'require "google/cloud/irm/v1alpha2/helpers"',
    ])
)

# Generate the helper methods
call('bundle update && bundle exec rake generate_partials', shell=True)
