# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


import importlib

from elangai._tensor import TensorData
from elangai.model.core import ModelExtension as me
from elangai.utils import (
    ELANGAI_ERROR,
    ELANGAI_WARNING,
    ELANGAI_INFO
)


TENSOR_INFO = {me.ONNX: ['name', 'shape', 'type'],
               me.TFLITE: ['name', 'shape', 'index', 'dtype', 'quantization']}


INPUT_INFO = {me.ONNX: 'get_inputs',
              me.TFLITE: 'get_input_details'}


OUTPUT_INFO = {me.ONNX: 'get_outputs',
               me.TFLITE: 'get_output_details'}


IMPORTED_MODULE = {me.ONNX: ('onnxruntime', '-- ONNXRuntime'),
                   me.TFLITE: ('tensorflow', '-- TensorFlow')}


class Dissector:
    def __init__(self, file_path: str, ext: str):
        global dissector_native

        ELANGAI_INFO("[ModelDissector] Dissector load...")

        if ext == me.ONNX: self.__dissector__ =  dissector_native.InferenceSession(file_path)
        elif ext == me.TFLITE: self.__dissector__ =  dissector_native.lite.Interpreter(file_path)
        else: ELANGAI_ERROR(TypeError, "[ModelDissector] Unsupported file extension: .{}".format(ext))

        self.__extension__ = ext

        try:
            self.__dissector__.allocate_tensors()
        except:
            ELANGAI_INFO("[ModelDissector] Dissector load complete")
            return None

        ELANGAI_INFO("[ModelDissector] Dissector load complete")

    def __disclose__(self, info_type: str):
        if info_type.lower() == "input":
            INFO = INPUT_INFO
            message_info = "Input"
        elif info_type.lower() == "output":
            INFO = OUTPUT_INFO
            message_info = "Output"
        else:
            ELANGAI_ERROR(TypeError, "[ModelDissector] Unknown type of info.")

        try:
            for tensor in getattr(self.__dissector__, INFO[self.__extension__])():
                ELANGAI_INFO("--------------------------------------------------")

                if self.__extension__ == me.TFLITE:
                    interim = TensorData()
                    for info in TENSOR_INFO[self.__extension__]:
                        setattr(interim, info, tensor[info])
                    tensor = interim

                for attribute in TENSOR_INFO[self.__extension__]:
                    message_info = "{} {}: {}".format(message_info, attribute, getattr(tensor, attribute))
                    ELANGAI_INFO(message_info)
                ELANGAI_INFO("--------------------------------------------------")
        except:
            ELANGAI_ERROR(TypeError, "[ModelDissector] Unsupported file extension: .{}".format(self.__extension__))


def module_import(ext: str):
    ELANGAI_INFO("[ModelDissector] Dissection begin") 
    try:
        global dissector_native
        dissector_native = importlib.import_module(IMPORTED_MODULE[ext][0])
    except Exception as e:
        ELANGAI_WARNING("Please make sure this library is already installed:")
        ELANGAI_WARNING(IMPORTED_MODULE[ext][1])
        ELANGAI_ERROR(e.__class__, str(e))


def module_cleanup():
    ELANGAI_INFO("[ModelDissector] Cleaning up...") 
    try:
        global dissector_native
        del dissector_native
    except:
        ELANGAI_INFO("[ModelDissector] Cleanup finished")
        return None
    ELANGAI_INFO("[ModelDissector] Cleanup finished")   


class ModelDissector:
    def __init__(self, model_path: str):
        ext = model_path.split("/")[-1].split(".")[-1]
        try:
            self.model_extension = getattr(me, ext.upper())
        except:
            ELANGAI_ERROR(TypeError, "[ModelDissector] Unsupported file extension: .{}".format(ext))
        self.file = model_path

    def dissect(self):
        module_import(self.model_extension)

        dissector = Dissector(self.file, self.model_extension)

        ELANGAI_INFO("[MODEL INPUT]")
        ELANGAI_INFO("++++++++++++++++++++++++++++++++++++++++++++++++++")
        dissector.__disclose__("input")
        ELANGAI_INFO("++++++++++++++++++++++++++++++++++++++++++++++++++")

        ELANGAI_INFO("[MODEL OUTPUT]")
        ELANGAI_INFO("++++++++++++++++++++++++++++++++++++++++++++++++++")
        dissector.__disclose__("output")
        ELANGAI_INFO("++++++++++++++++++++++++++++++++++++++++++++++++++")

        module_cleanup()
