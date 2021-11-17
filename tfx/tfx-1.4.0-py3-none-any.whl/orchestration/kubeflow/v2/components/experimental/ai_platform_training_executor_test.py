# Copyright 2020 Google LLC. All Rights Reserved.
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
"""Tests for AI Platform Training component executor."""

import copy

from unittest import mock

from googleapiclient import discovery
import tensorflow as tf  # pylint: disable=g-explicit-tensorflow-version-import
from tfx.dsl.component.experimental import placeholders
from tfx.orchestration.kubeflow.v2.components.experimental import ai_platform_training_executor
from tfx.types import artifact_utils
from tfx.types import standard_artifacts
from tfx.utils import json_utils
from tfx.utils import test_case_utils


_EXAMPLE_LOCATION = 'root/ExampleGen/1/examples/'
_MODEL_LOCATION = 'root/Training/2/model/'


class AiPlatformTrainingExecutorTest(test_case_utils.TfxTest):

  def setUp(self):
    super().setUp()
    self._project_id = 'my-project'
    self._job_id = 'my-job-123'
    self._labels = ['label1', 'label2']

    examples_artifact = standard_artifacts.Examples()
    examples_artifact.split_names = artifact_utils.encode_split_names(
        ['train', 'eval'])
    examples_artifact.uri = _EXAMPLE_LOCATION
    self._inputs = {'examples': [examples_artifact]}
    model_artifact = standard_artifacts.Model()
    model_artifact.uri = _MODEL_LOCATION
    self._outputs = {'model': [model_artifact]}

    training_job = {
        'training_input': {
            'scaleTier':
                'CUSTOM',
            'region':
                'us-central1',
            'masterType':
                'n1-standard-8',
            'masterConfig': {
                'imageUri': 'gcr.io/my-project/caip-training-test:latest'
            },
            'workerType':
                'n1-standard-8',
            'workerCount':
                8,
            'workerConfig': {
                'imageUri': 'gcr.io/my-project/caip-training-test:latest'
            },
            'args': [
                '--examples',
                placeholders.InputUriPlaceholder('examples'), '--n-steps',
                placeholders.InputValuePlaceholder('n_step'), '--model-dir',
                placeholders.OutputUriPlaceholder('model')
            ]
        },
        'labels': self._labels,
    }

    aip_training_config = {
        ai_platform_training_executor.PROJECT_CONFIG_KEY: self._project_id,
        ai_platform_training_executor.TRAINING_JOB_CONFIG_KEY: training_job,
        ai_platform_training_executor.JOB_ID_CONFIG_KEY: self._job_id,
        ai_platform_training_executor.LABELS_CONFIG_KEY: self._labels,
    }

    self._exec_properties = {
        ai_platform_training_executor.CONFIG_KEY:
            json_utils.dumps(aip_training_config),
        'n_step':
            100
    }

    resolved_training_input = copy.deepcopy(training_job['training_input'])
    resolved_training_input['args'] = [
        '--examples', _EXAMPLE_LOCATION, '--n-steps', '100', '--model-dir',
        _MODEL_LOCATION
    ]

    self._expected_job_spec = {
        'job_id': self._job_id,
        'training_input': resolved_training_input,
        'labels': self._labels,
    }

    self._mock_api_client = mock.Mock()
    mock_discovery = self.enter_context(
        mock.patch.object(
            discovery,
            'build',
            autospec=True))
    mock_discovery.return_value = self._mock_api_client
    self._setUpTrainingMocks()

  def _setUpTrainingMocks(self):
    self._mock_create = mock.Mock()
    self._mock_api_client.projects().jobs().create = self._mock_create
    self._mock_get = mock.Mock()
    self._mock_api_client.projects().jobs().get.return_value = self._mock_get
    self._mock_get.execute.return_value = {
        'state': 'SUCCEEDED',
    }

  def testRunAipTraining(self):
    aip_executor = ai_platform_training_executor.AiPlatformTrainingExecutor()

    aip_executor.Do(
        input_dict=self._inputs,
        output_dict=self._outputs,
        exec_properties=self._exec_properties)

    self._mock_create.assert_called_once_with(
        body=self._expected_job_spec,
        parent='projects/{}'.format(self._project_id))

  def testRunAipTrainingWithDefaultJobId(self):
    aip_executor = ai_platform_training_executor.AiPlatformTrainingExecutor()

    # Delete job_id in the exec_properties.
    training_config = json_utils.loads(
        self._exec_properties[ai_platform_training_executor.CONFIG_KEY])
    training_config[ai_platform_training_executor.JOB_ID_CONFIG_KEY] = None
    self._exec_properties[ai_platform_training_executor.CONFIG_KEY] = (
        json_utils.dumps(training_config))

    aip_executor.Do(
        input_dict=self._inputs,
        output_dict=self._outputs,
        exec_properties=self._exec_properties)

    self._mock_create.assert_called_once()
    print(self._mock_create.call_args[1])
    print(self._mock_create.call_args[1]['body'])
    self.assertEqual('tfx_',
                     self._mock_create.call_args[1]['body']['job_id'][:4])

if __name__ == '__main__':
  tf.test.main()
