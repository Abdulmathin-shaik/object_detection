from ultralytics import YOLO

def download_models():
    models = ['yolov8n.pt', 'yolov8m.pt', 'yolov8s.pt']
    for model in models:
        print(f"Downloading {model}...")
        YOLO(model)
        print(f"Downloaded {model}")

if __name__ == "__main__":
    download_models()
