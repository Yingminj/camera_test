import cv2
import datetime
import yaml
import numpy as np
from camera_test.load_cam_params import load_camera_intrinsics 

class Camera:
    def __init__(self, device, width=640, height=480, fps=30, undistortion=False):
        self.device = device
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None
        self.recording = False
        self.out = None
        self.undistortion = undistortion
        self.camera_matrix = None
        self.dist_coeffs = None
        if self.undistortion:
            self.camera_matrix, self.dist_coeffs, self.proj_matrix = load_camera_intrinsics('head')

    def initialize(self):
        self.cap = cv2.VideoCapture(self.device)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        if not self.cap.isOpened():
            print("无法打开相机")
            return False
        return True

    def get_frame(self):
        if not self.initialize():
            return 
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.undistortion:
                frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)
 
            yield frame
        self.cleanup()

    def run(self):
        if not self.initialize():
            return
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if self.undistortion:
                frame = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs)    
            cv2.imshow('Camera', frame)
            if self.recording:
                self.out.write(frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('e'):
                self.take_photo(frame)
            elif key == ord('r'):
                self.toggle_recording()
        self.cleanup()

    def take_photo(self, frame):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cap/photo_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"照片已保存: {filename}")

    def toggle_recording(self):
        if not self.recording:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cap/video_{timestamp}.mp4"
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))
            self.recording = True
            print(f"开始录制: {filename}")
        else:
            self.out.release()
            self.recording = False
            print("录制停止")

    def cleanup(self):
        if self.recording and self.out is not None:
            self.out.release()
        if self.cap is not None:
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    camera = Camera(device="/dev/video6", fps=60)
    camera.run()