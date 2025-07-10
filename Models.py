import tensorflow as tf
from tensorflow.keras.applications import (
    EfficientNetB0, DenseNet121
)
from transformers import AutoFeatureExtractor, SwinForImageClassification, ViTForImageClassification, AutoModel

class VisionModels:
    def __init__(self, model_name, input_shape=(224, 224, 3)):
        """
        Initialize the class with the model name and input shape.
        Args:
        - model_name (str): Name of the model ('efficientnet', 'densenet', 'swin_transformer', 'dino', 'clip').
        - input_shape (tuple): Shape of input data, default is (224, 224, 3).
        """
        self.model_name = model_name
        self.input_shape = input_shape
        self.model = self._load_model()

        # For CLIP, load the feature extractor separately
        if self.model_name.lower() == "clip":
            self.feature_extractor = AutoFeatureExtractor.from_pretrained("openai/clip-vit-base-patch32")
            self.clip_model = AutoModel.from_pretrained("openai/clip-vit-base-patch32")

    def _load_model(self):
        """
        Load the chosen model based on the name.
        Returns:
        - Model object.
        """
        if self.model_name.lower() == "efficientnet":
            return EfficientNetB0(weights='imagenet', input_shape=self.input_shape, include_top=False)
        elif self.model_name.lower() == "densenet":
            return DenseNet121(weights='imagenet', input_shape=self.input_shape, include_top=False)
        elif self.model_name.lower() == "swin_transformer":
            return AutoModel.from_pretrained("microsoft/swin-base-patch4-window7-224")
        elif self.model_name.lower() == "dino":
            return AutoModel.from_pretrained("facebook/dino-vit-base")
        elif self.model_name.lower() == "clip":
            # CLIP handled separately
            return None
        else:
            raise ValueError(f"Model name '{self.model_name}' is not supported.")

    def preprocess(self, image):
        """
        Preprocess the input image for the model.
        Args:
        - image (np.array or PIL.Image): Image to preprocess.
        Returns:
        - Preprocessed image or features.
        """
        if self.model_name.lower() == "efficientnet":
            image = tf.image.resize(image, (224, 224))
            image = tf.keras.applications.efficientnet.preprocess_input(image)
            return image
        elif self.model_name.lower() == "densenet":
            image = tf.image.resize(image, (224, 224))
            image = tf.keras.applications.densenet.preprocess_input(image)
            return image
        elif self.model_name.lower() == "swin_transformer" or self.model_name.lower() == "dino":
            return self.feature_extractor(images=image, return_tensors="pt")
        elif self.model_name.lower() == "clip":
            return self.feature_extractor(images=image, return_tensors="pt")
        else:
            raise ValueError("Unsupported model during preprocessing.")

    def extract_features(self, image):
        """
        Extract features using the chosen model.
        Args:
        - image (np.array or PIL.Image): Image to extract features from.
        Returns:
        - Extracted features.
        """
        preprocessed = self.preprocess(image)

        if self.model_name.lower() == "efficientnet":
            return self.model(tf.expand_dims(preprocessed, axis=0))
        elif self.model_name.lower() == "densenet":
            return self.model(tf.expand_dims(preprocessed, axis=0))
        elif self.model_name.lower() == "swin_transformer":
            outputs = self.model(**preprocessed)
            return outputs.last_hidden_state
        elif self.model_name.lower() == "dino":
            outputs = self.model(**preprocessed)
            return outputs.last_hidden_state
        elif self.model_name.lower() == "clip":
            # For CLIP, get image features
            with torch.no_grad():
                outputs = self.clip_model(**preprocessed)
            return outputs
        else:
            raise ValueError("Unknown model during feature extraction.")

if __name__ == "__main__":
    # Existing models
    efficientnet_model = VisionModels(model_name="efficientnet")
    print("EfficientNet initialized!")

    swin_transformer_model = VisionModels(model_name="swin_transformer")
    print("Swin Transformer initialized!")

    dino_model = VisionModels(model_name="dino")
    print("DINO initialized!")

    # New models
    densenet_model = VisionModels(model_name="densenet")
    print("DenseNet initialized!")

    clip_model = VisionModels(model_name="clip")
    print("CLIP initialized!")