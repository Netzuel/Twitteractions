# En este caso consideramos que el hardware es una NPU, por lo que hemos de usar únicamente Tensorflow Lite.
# Para ello ha de existir únicamente el intérprete de TFLite que incluye el código mínimo necesario para realizar inferencia usando modelos .tflite.
# Más info en: https://www.tensorflow.org/lite/guide/python
import tflite_runtime.interpreter as tflite

class Model_npu(object):
    def __init__(self, path, shape_input):
        self.path = path
        self.input_w = shape_input[0]
        self.input_h = shape_input[1]
    def model(self):
        interpreter = tflite.Interpreter(model_path = self.path)
        interpreter.resize_tensor_input(interpreter.get_input_details()[0]["index"], [1,self.input_w,self.input_h,3], strict = True)
        interpreter.allocate_tensors()
        return interpreter
    def predict(self, object_to_predict):
        tflitemodel = self.model()
        input_details = tflitemodel.get_input_details()
        output_details = tflitemodel.get_output_details()
        tflitemodel.set_tensor(input_details[0]["index"], object_to_predict)
        tflitemodel.invoke()
        predictions = [tflitemodel.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        return predictions