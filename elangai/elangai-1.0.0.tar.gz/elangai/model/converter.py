# Copyright 2021 elangai Developer. All Rights Reserved.
#
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by Resha Al-Fahsi <resha.alfahsi@techbros.io>, 2021.
# =========================================================================


from os.path import exists
from elangai.model.core import ModelExtension as me
from elangai.utils.exception import NotFoundError
from elangai.utils._timer import elang_timer
from elangai.utils import (
    ELANGAI_ERROR,
    ELANGAI_INFO,
    ELANGAI_WARNING
)


class ModelConverter:
    def __init__(self, src: str, dst: str, precision: str):
        ext = src.split("/")[-1].split(".")[-1]
        try:
            self.model_extension = getattr(me, ext.upper())
        except:
            ELANGAI_ERROR(TypeError, "[ModelConverter] Unsupported file extension: .{}".format(ext))

        ext = dst.split("/")[-1].split(".")[-1]
        assert ext in ".trt", "[ModelConverter] Output file extension must be: '.trt'"

        try:
            import tensorrt as trt
        except Exception as e:
            ELANGAI_WARNING("Please make sure this library is already installed:")
            ELANGAI_WARNING("-- TensorRT")
            ELANGAI_ERROR(e.__class__, str(e))

        self.input_path = src
        self.output_path = dst
        self.precision = precision.lower()
        self.trt_logger = trt.Logger()
        self.explicit_batch = 1 << (int)(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)

    @elang_timer
    def convert(self):
        try:
            import tensorrt as trt
        except Exception as e:
            ELANGAI_WARNING("Please make sure this library is already installed:")
            ELANGAI_WARNING("-- TensorRT")
            ELANGAI_ERROR(e.__class__, str(e))

        trt.init_libnvinfer_plugins(self.trt_logger, "")
        builder = trt.Builder(self.trt_logger)
        network = builder.create_network(self.explicit_batch)
        config = builder.create_builder_config()

        config.max_workspace_size = (256 << 20)
        builder.max_batch_size = 1
        if self.precision == 'fp32':
            ELANGAI_INFO("[ModelConverter] Using default precision: fp32")
        elif self.precision == 'fp16':
            ELANGAI_INFO("[ModelConverter] Using precision: fp16")
            config.set_flag(trt.BuilderFlag.GPU_FALLBACK)
            config.set_flag(trt.BuilderFlag.FP16)
        elif self.precision == 'int8':
            ELANGAI_INFO("[ModelConverter] Using precision: int8")
            config.set_flag(trt.BuilderFlag.GPU_FALLBACK)
            config.set_flag(trt.BuilderFlag.INT8)
        else:
            ELANGAI_ERROR(TypeError, "[ModelConverter] Expected precision: fp16, fp32 or int8")

        if self.model_extension == me.ONNX:
            parser = trt.OnnxParser(network, self.trt_logger)
            ELANGAI_INFO("[ModelConverter] Loading ONNX file from path {}...".format(self.input_path))
            if not exists(self.input_path):
                ELANGAI_ERROR(NotFoundError, "[ModelConverter] ONNX file, {}, not found.".format(self.input_path))

            with open(self.input_path, "rb") as model:
                ELANGAI_INFO("[ModelConverter] Beginning ONNX file parsing")
                if not parser.parse(model.read()):
                    ELANGAI_ERROR(Exception, "[ModelConverter] Failed to parse the ONNX file")

            ELANGAI_INFO("[ModelConverter] Completed parsing of ONNX file")
            ELANGAI_INFO("[ModelConverter] Building an engine from file {}; this may take a while...".format(self.input_path))
            engine = builder.build_engine(network, config)
            ELANGAI_INFO("[ModelConverter] Completed creating Engine: {}".format(self.output_path))
            with open(self.output_path, "wb") as f:
                f.write(engine.serialize())
        else:
            ELANGAI_ERROR(TypeError, "[ModelConverter] Model Conversion Failed: File not Supported")
