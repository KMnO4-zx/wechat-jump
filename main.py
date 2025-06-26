from ultralytics import YOLO
import subprocess
import random
import time
import os
import numpy as np
import datetime


class Jump:
    def __init__(self, model_path: str) -> None:
        self.model = YOLO(model_path)
        self.save_floder = f"./dataset/predict_{int(time.time())}"

    def predict(self, image: str):
        results = self.model.predict(image, conf=0.2, iou=0.1, verbose=False)
        # 保存预测结果
        os.makedirs(self.save_floder, exist_ok=True)
        save_name = f"{self.save_floder}/results_{time.time()}.png"
        results[0].save(filename=save_name)

        # 获取检测框和类别
        boxes = results[0].boxes.xywh.cpu().numpy()  # 转换为numpy数组
        cls = results[0].boxes.cls.cpu().numpy()  # 获取类别

        # 筛选出类别为0的检测框 cube
        cube_boxes = boxes[cls == 0]
        cube_boxes = sorted(cube_boxes, key=lambda x: x[1])
        # 筛选出类别为1的检测框
        humen_boxes = boxes[cls == 1]
        
        # 计算距离
        if len(cube_boxes) > 0 and len(humen_boxes) > 0:
            cube_box = cube_boxes[0]
            humen_box = humen_boxes[0]
            # 计算距离
            distance = np.sqrt((cube_box[0] - humen_box[0]) ** 2 + (cube_box[1] - (humen_box[1] + humen_box[3] * 0.5)) ** 2)
            return round(distance, 3)
        else:
            return 0

    # 使用adb控制手机屏幕截图，并将截图传输到本机，同时删除手机目录的截图
    def adb_screenshot(self):
        # 截图并传输
        subprocess.run(["adb", "shell", "screencap", "-p", "/sdcard/temp_screenshot.png"], check=True)
        subprocess.run(["adb", "pull", "/sdcard/temp_screenshot.png", "./iphone.png"], check=True)
        subprocess.run(["adb", "shell", "rm", "/sdcard/temp_screenshot.png"], check=True)

    # 使用 adb 模拟按压
    def adb_tap(self, x: int, y: int, duration_ms: int = 100):
        """
        使用adb模拟手机屏幕按压
        :param x: 按压位置的x坐标
        :param y: 按压位置的y坐标  
        :param duration_ms: 按压持续时间，单位毫秒
        """
        subprocess.run(["adb", "shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)], check=True)
        print(f"模拟按压位置: ({x}, {y}), 持续时间: {duration_ms}ms")

    def jump(self, k: float = 7.0):
        self.adb_screenshot()
        distance = self.predict("./iphone.png")
        print(f"距离: {distance}")

        # 计算按压时间 根据手机分辨率不同按压时间不同（系数 k 不同）
        press_time = int(distance * k)

        # 模拟按压 位置随机按压
        x = random.randint(300, 700)
        y = random.randint(1000, 1200)
        self.adb_tap(x, y, duration_ms = press_time)
        # 等待1秒
        time.sleep(2)

    

if __name__ == "__main__":
    jump = Jump("./best.pt")
    # jump.adb_screenshot()
    # print(jump.predict("./iphone.png"))
    while True:
        jump.jump(k=1.18)
