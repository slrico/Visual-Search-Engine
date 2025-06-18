from datasets import load_dataset
from PIL import Image
import numpy as np

# Load dataset
ds = load_dataset("nsarker/plantspecies-demo")

def process_pil_image(image):
    """
    Preprocess the image if it is already in PIL.Image format.
    Resize and normalize the image.
    """
    try:
        if not isinstance(image, Image.Image):
            raise TypeError(f"Expected PIL.Image.Image, got {type(image)}.")
        
        # Resize image to (224, 224)
        image = image.resize((224, 224))
        
        # Normalize pixel values to the range [0, 1]
        image_array = np.array(image) / 255.0
        
        return image_array
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

# Test processing with the first sample
sample = ds['train'][0]
if 'image' in sample:
    # Process the image directly as a PIL object
    processed_image = process_pil_image(sample['image'])
    print("Processed image:", processed_image)

from pymongo import MongoClient

def connect_to_mongodb():
    """
    Connect to the MongoDB server and return the database and collection objects.
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["visual_search_db"]
    images_collection = db["images"]
    print("Connected to MongoDB!")
    return images_collection

from PIL import Image
import numpy as np

def process_pil_image(image):
    """
    Preprocess the image: resize and normalize pixel values.
    """
    try:
        if not isinstance(image, Image.Image):
            raise TypeError(f"Expected PIL.Image.Image, got {type(image)}.")
        
        # Resize image to (224, 224)
        image = image.resize((224, 224))
        
        # Normalize pixel values to range [0, 1]
        image_array = np.array(image) / 255.0
        
        return image_array
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def insert_data(images_collection, image_path, processed_image, features, label):
    """
    Insert a single document (image data and metadata) into MongoDB.
    """
    try:
        if processed_image is None:
            raise ValueError("Processed image is invalid.")

        document = {
            "image_path": image_path,
            "processed_image": processed_image.tolist(),
            "features": features.tolist(),
            "label": label.tolist()
        }
        result = images_collection.insert_one(document)
        print(f"Inserted document with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error inserting document: {e}")

def batch_insert(images_collection, dataset):
    """
    Insert multiple documents from the dataset into MongoDB in batch.
    """
    batch = []
    for example in dataset:
        processed_image = process_pil_image(example['image'])
        if processed_image is None:
            continue  # Skip invalid images
        document = {
            "image_path": example.get('image_path', "unknown.jpg"),
            "processed_image": processed_image.tolist(),
            "features": np.random.rand(1000).tolist(),  # Simulated feature vector
            "label": np.array([1, 0]).tolist()  # Simulated one-hot encoded label
        }
        batch.append(document)
    result = images_collection.insert_many(batch)
    print(f"Inserted {len(result.inserted_ids)} documents into the collection!")

def query_data(images_collection, query_filter=None):
    """
    Query data from MongoDB based on the provided filter.
    """
    if query_filter is None:
        query_filter = {}
    cursor = images_collection.find(query_filter)
    results = [doc for doc in cursor]
    print(f"Retrieved {len(results)} documents.")
    return results

def fetch_features(images_collection):
    """
    Fetch feature vectors from all documents in MongoDB.
    """
    cursor = images_collection.find({}, {"features": 1, "_id": 0})
    features = [doc["features"] for doc in cursor]
    print(f"Fetched {len(features)} feature vectors.")
    return features

def fetch_labels(images_collection):
    """
    Fetch labels from all documents in MongoDB.
    """
    cursor = images_collection.find({}, {"label": 1, "_id": 0})
    labels = [doc["label"] for doc in cursor]
    print(f"Fetched {len(labels)} labels.")
    return labels

if __name__ == "__main__":
    # Connect to MongoDB
    images_collection = connect_to_mongodb()

    # Example data
    sample = ds['train'][0]
    processed_image = process_pil_image(sample['image'])
    image_path = "unknown.jpg"
    features = np.random.rand(1000)  # Simulated feature vector
    label = np.array([1, 0])  # Example one-hot encoded label

    # Insert single data
    insert_data(images_collection, image_path, processed_image, features, label)

    # Batch insert data
    batch_insert(images_collection, ds['train'])

    # Query data
    query_results = query_data(images_collection)
    print(f"Sample query result: {query_results[0]}")

    # Fetch features and labels
    features = fetch_features(images_collection)
    labels = fetch_labels(images_collection)
