# Copyright 2018 The TensorFlow Authors. All Rights Reserved.
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
# ==============================================================================
"""label_image for tflite."""

import argparse
import time

import numpy as np
from PIL import Image
import tflite_runtime.interpreter as tflite

#labelsFile = 'tensorflow/labels.txt'
#modelsFile = 'tensorflow/mobilenet_v1_1.0_224_quant.tflite'
labelsFile = 'tensorflow/labels.txt'
modelsFile = 'tensorflow/mobilenet_v1_1.0_224_quant.tflite'

inputMean = 127.5
inputStd = 127.5
numThreads = None
extDelegate = None

def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]


def recognize(imgName):
  ext_delegate = None
  ext_delegate_options = None

  # parse extenal delegate options
  if ext_delegate_options is not None:
    options = ext_delegate_options.split(';')
    for o in options:
      kv = o.split(':')
      if (len(kv) == 2):
        ext_delegate_options[kv[0].strip()] = kv[1].strip()
      else:
        raise RuntimeError('Error parsing delegate option: ' + o)

  # load external delegate
  if ext_delegate is not None:
    print('Loading external delegate from {} with args: {}'.format(
        ext_delegate, ext_delegate_options))
    ext_delegate = [
        tflite.load_delegate(ext_delegate, ext_delegate_options)
    ]

  interpreter = tflite.Interpreter(model_path=modelsFile,
      experimental_delegates=ext_delegate,
      num_threads=numThreads)
  interpreter.allocate_tensors()

  input_details = interpreter.get_input_details()
  output_details = interpreter.get_output_details()

  # check the type of the input tensor
  floating_model = input_details[0]['dtype'] == np.float32

  # NxHxWxC, H:1, W:2
  height = input_details[0]['shape'][1]
  width = input_details[0]['shape'][2]
  img = Image.open(imgName).resize((width, height))

  # add N dim
  input_data = np.expand_dims(img, axis=0)

  if floating_model:
    input_data = (np.float32(input_data) - inputMean) / inputStd

  interpreter.set_tensor(input_details[0]['index'], input_data)

  start_time = time.time()
  interpreter.invoke()
  stop_time = time.time()

  output_data = interpreter.get_tensor(output_details[0]['index'])
  results = np.squeeze(output_data)

  top_k = results.argsort()[-5:][::-1]
  labels = load_labels(labelsFile)
  resultLabels = []
  for i in top_k:
    if floating_model:
      print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
      newItem=labels[i].split(":")[1]
      if (newItem == 'banana' or newItem == 'water bottle' or newItem == 'apple' or newItem == 'corn' or newItem == 'burrito' or newItem == 'pineapple' or newItem == 'lemon' or newItem == 'broccoli' ):
         resultLabels.append(newItem)
      else:
        print('')
         
    else:
      print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))
      newItem=labels[i].split(":")[1]
      resultLabels.append(newItem)

  print('time: {:.3f}ms'.format((stop_time - start_time) * 1000))
  return resultLabels
