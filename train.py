from ultralytics import YOLO

if __name__ == '__main__':
    # Load a model
    model = YOLO("yolov10n.pt")  # load a pretrained model (recommended for training)

    # Train the model
    results = model.train(data="./yolo_dataset/data.yaml", epochs=500, imgsz=640)