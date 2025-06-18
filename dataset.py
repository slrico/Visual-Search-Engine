from datasets import load_dataset
from PIL import Image, UnidentifiedImageError
import numpy as np
from torchvision import transforms, models
import torch
from torch.nn.functional import one_hot
from sklearn.model_selection import train_test_split

# Login using e.g. `huggingface-cli login` to access this dataset
print("Loading dataset...")
ds = load_dataset("nsarker/plantspecies-demo")

# Inspect the dataset structure
print("Dataset structure:", ds)
print("Inspecting the first training sample...")
print(ds['train'][0])  # Look at the first sample


# Step 1: Basic Preprocessing
def preprocess_basic(example):
    """
    Preprocess a single example by resizing the image and normalizing pixel values.
    Includes error handling for missing or invalid data.
    """
    try:
        if 'image' not in example or example['image'] is None:
            raise ValueError("Missing or invalid 'image' field in the example.")

        if not isinstance(example['image'], Image.Image):
            raise TypeError(f"Expected PIL.Image, got {type(example['image'])}.")

        image = example['image'].resize((224, 224))
        image_array = np.array(image) / 255.0
        return {'image': image_array, 'label': example['label']}
    except (UnidentifiedImageError, ValueError, TypeError) as e:
        print(f"Error in preprocess_basic: {e}")
        return None


# Step 2: Data Augmentation
def preprocess_with_augmentation(example):
    """
    Apply augmentation techniques like random flipping and rotation to the image.
    """
    try:
        if not isinstance(example['image'], Image.Image):
            raise TypeError(f"Expected PIL.Image, got {type(example['image'])}.")

        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ToTensor()
        ])

        augmented_image = transform(example['image'])
        augmented_image = augmented_image.numpy()
        return {'image': augmented_image, 'label': example['label']}
    except Exception as e:
        print(f"Error in preprocess_with_augmentation: {e}")
        return None


# Step 3: One-Hot Encoding for Labels
def one_hot_encode_labels(example):
    """
    One-hot encode labels for binary classification.
    """
    try:
        num_classes = 2  # Assuming binary classification
        label = one_hot(torch.tensor(example['label']), num_classes).numpy()
        return {'image': example['image'], 'label': label}
    except Exception as e:
        print(f"Error in one_hot_encode_labels: {e}")
        return None


# Step 4: Feature Extraction Using ResNet
resnet = models.resnet50(pretrained=True)  # Load pre-trained ResNet50
resnet.eval()  # Set model to evaluation mode

def extract_resnet_features(example):
    """
    Extract feature vectors using a pre-trained ResNet model.
    """
    try:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ])

        image = transform(example['image']).unsqueeze(0)  # Add batch dimension
        features = resnet(image).detach().numpy()
        return {'features': features, 'label': example['label']}
    except Exception as e:
        print(f"Error in extract_resnet_features: {e}")
        return None


# Apply all steps sequentially
print("Applying basic preprocessing...")
try:
    ds = ds.map(preprocess_basic, batched=False)
    print("Basic preprocessing completed successfully.")
except Exception as e:
    print(f"An error occurred during basic preprocessing: {e}")

print("Applying data augmentation...")
try:
    ds = ds.map(preprocess_with_augmentation, batched=False)
    print("Data augmentation completed successfully.")
except Exception as e:
    print(f"An error occurred during data augmentation: {e}")

print("One-hot encoding labels...")
try:
    ds = ds.map(one_hot_encode_labels, batched=False)
    print("One-hot encoding completed successfully.")
except Exception as e:
    print(f"An error occurred during one-hot encoding: {e}")

print("Extracting features using ResNet...")
try:
    ds = ds.map(extract_resnet_features, batched=False)
    print("Feature extraction completed successfully.")
except Exception as e:
    print(f"An error occurred during feature extraction: {e}")

# Step 5: Train-Test Split
print("Splitting dataset into training and testing sets...")
try:
    images = np.array([example['features'] for example in ds['train']])
    labels = np.array([example['label'] for example in ds['train']])
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)
    print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")
except Exception as e:
    print(f"An error occurred during train-test split: {e}")

# Step 6: Save the Processed Dataset
print("Saving processed data...")
try:
    import pickle
    with open("processed_dataset.pkl", "wb") as f:
        pickle.dump({'X_train': X_train, 'X_test': X_test, 'y_train': y_train, 'y_test': y_test}, f)
    print("Data saved to 'processed_dataset.pkl'.")
except Exception as e:
    print(f"An error occurred while saving the dataset: {e}")
