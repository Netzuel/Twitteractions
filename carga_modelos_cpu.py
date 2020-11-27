# En est caso trabajamos con CPU por lo que podemos cargar el módulo entero de Tensorflow.
import tensorflow as tf
from cv2 import imread, cvtColor, resize, INTER_LINEAR_EXACT, COLOR_BGR2RGB
from tensorflow.keras.models import load_model
from numpy import expand_dims

# Vamos a definir una clase para preprocesar una imagen.

class Imagen(object):
    def __init__(self, path):
        self.path = path
    def processed(self, shape_input):
        try:
            frame = imread(self.path)
            frame = cvtColor(frame, COLOR_BGR2RGB)
            frame = resize(frame, (shape_input[0], shape_input[1]), interpolation = INTER_LINEAR_EXACT)
            frame = frame.astype('float32')
            frame /= 255.0
            frame = expand_dims(frame, 0)
            return frame
        except:
            print("La imagen no ha podido ser procesada. Las dimensiones deseadas deben ser especificadas como una tupla (width, height)")
        

# Primero vamos a crear una clase para definir el objeto Model.

class Model(object):
    def __init__(self, path, shape_input):
        # 'path' va a ser la dirección del modelo que se cargará de tipo h5, pb, o tflite.
        self.path = path
        self.input_w = shape_input[0]
        self.input_h = shape_input[1]
    def model(self):
        # Se admitirán los 3 formatos.
        if self.path.endswith(".h5"):
            model = load_model(self.path, compile = False)
            return model
        elif self.path.endswith(".pb"):
            model = tf.saved_model.load(self.path)
            return model
        elif self.path.endswith(".tflite"):
            interpreter = tf.lite.Interpreter(model_path = self.path)
            interpreter.resize_tensor_input(interpreter.get_input_details()[0]["index"], [1,self.input_w,self.input_h,3], strict = True)
            interpreter.allocate_tensors()
            return interpreter
    def predict(self, object_to_predict):
        if self.path.endswith(".h5"):
            self.object_input = object_to_predict
            predictions = self.model().predict(object_to_predict)
            return predictions
        elif self.path.endswith(".pb"):
            self.object_input = object_to_predict
            predictions = self.model().predict(object_to_predict)
            return predictions
        elif self.path.endswith(".tflite"):
            tflitemodel = self.model()
            input_details = tflitemodel.get_input_details()
            output_details = tflitemodel.get_output_details()
            tflitemodel.set_tensor(input_details[0]["index"], object_to_predict)
            tflitemodel.invoke()
            predictions = [tflitemodel.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            return predictions
    def convert_to_tflite(self, output_path):
        if self.path.endswith(".h5") or self.path.endswith(".pb"):
            tf.saved_model.save(self.model(), "saved_model")
            converter = tf.lite.TFLiteConverter.from_saved_model("saved_model")
            tflite_model = converter.convert()
            try:
                with open(output_path, "wb") as f:
                    f.write(tflite_model)
                    print("El modelo se ha convertido satisfactoriamente.")
            except:
                print("Ha ocurrido un error, asegúrese de haber especificado correctamente la ruta a su modelo .tflite, por ejemplo: 'modelo.tflite'.")
        else:
            print("El modelo de entrada ha de ser .h5 o bien .pb.")