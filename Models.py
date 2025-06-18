import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from transformers import AutoFeatureExtractor, SwinForImageClassification, ViTForImageClassification, AutoModel

class VisionModels:
    def __init__(self, model_name, input_shape=(224, 224, 3)):
        """
        Initialize the class with the model name and input shape.
        Args:
        - model_name (str): Name of the model ('efficientnet', 'swin_transformer', or 'dino').
        - input_shape (tuple): Shape of input data, default is (224, 224, 3).
        """
        self.model_name = model_name
        self.input_shape = input_shape
        self.model = self._load_model()

    def _load_model(self):
        """
        Load the chosen model based on the name.
        Returns:
        - Model object.
        """
        if self.model_name.lower() == "efficientnet":
            return EfficientNetB0(weights='imagenet', input_shape=self.input_shape, include_top=False)
        elif self.model_name.lower() == "swin_transformer":
            feature_extractor = AutoFeatureExtractor.from_pretrained("microsoft/swin-base-patch4-window7-224")
            model = SwinForImageClassification.from_pretrained("microsoft/swin-base-patch4-window7-224")
            return model
        elif self.model_name.lower() == "dino":
            feature_extractor = AutoFeatureExtractor.from_pretrained("facebook/dino-vit-base")
            model = AutoModel.from_pretrained("facebook/dino-vit-base")
            return model
        else:
            raise ValueError(f"Model name '{self.model_name}' is not supported. Choose 'efficientnet', 'swin_transformer', or 'dino'.")

    def preprocess(self, image):
        """
        Preprocess the input image for the model.
        Args:
        - image (np.array or PIL.Image): Image to preprocess.
        Returns:
        - Preprocessed image.
        """
        if self.model_name.lower() == "efficientnet":
            image = tf.image.resize(image, (224, 224))
            image = tf.keras.applications.efficientnet.preprocess_input(image)
            return image
        elif self.model_name.lower() == "swin_transformer":
            return AutoFeatureExtractor.from_pretrained("microsoft/swin-base-patch4-window7-224")(image)
        elif self.model_name.lower() == "dino":
            return AutoFeatureExtractor.from_pretrained("facebook/dino-vit-base")(image)

    def extract_features(self, image):
        """
        Extract features using the chosen model.
        Args:
        - image (np.array or PIL.Image): Image to extract features from.
        Returns:
        - Extracted features.
        """
        preprocessed_image = self.preprocess(image)
        if self.model_name.lower() == "efficientnet":
            return self.model(tf.expand_dims(preprocessed_image, axis=0))
        elif self.model_name.lower() == "swin_transformer":
            outputs = self.model(preprocessed_image)
            return outputs.last_hidden_state
        elif self.model_name.lower() == "dino":
            outputs = self.model(preprocessed_image)
            return outputs.last_hidden_state


if __name__ == "__main__":

    efficientnet_model = VisionModels(model_name="efficientnet")
    print("EfficientNet initialized!")
    
    swin_transformer_model = VisionModels(model_name="swin_transformer")
    print("Swin Transformer initialized!")
    
    dino_model = VisionModels(model_name="dino")
    print("DINO initialized!")
