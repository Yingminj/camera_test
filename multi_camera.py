import cv2
import argparse
import yaml
import numpy as np

# 解析命令行参数
def parse_args():
    parser = argparse.ArgumentParser(description='Multi Camera Viewer')
    parser.add_argument('--device', type=str, default='/dev/top_camera', help='Camera device name')
    parser.add_argument('--param', type=str, default='camera_info_640/top.yaml', help='Camera parameter YAML path')
    parser.add_argument('--show_undistort', action='store_true', help='Show undistorted image for comparison')
    parser.add_argument('--width', type=int, default=640, help='Override image width')
    parser.add_argument('--height', type=int, default=480, help='Override image height')
    parser.add_argument('--fps', type=int, default=30, help='Camera FPS')
    return parser.parse_args()

# 读取相机参数
def load_camera_params(yaml_path):
    with open(yaml_path, 'r') as f:
        params = yaml.safe_load(f)
    K = np.array(params['camera_matrix']['data']).reshape((3,3))
    D = np.array(params['distortion_coefficients']['data'])
    P = np.array(params['projection_matrix']['data']).reshape((3,4))
    width = params['image_width']
    height = params['image_height']
    return K, D, P, width, height

# 初始化相机
def init_camera(device, width, height, fps):
    cap = cv2.VideoCapture(device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FPS, fps)
    return cap

# 主程序
def main():
    args = parse_args()
    K, D, P, param_width, param_height = load_camera_params(args.param)
    width = args.width if args.width else param_width
    height = args.height if args.height else param_height
    cap = init_camera(args.device, width, height, args.fps)
    if not cap.isOpened():
        print(f'Failed to open camera: {args.device}')
        return
    print(f'Camera {args.device} opened. Resolution: {width}x{height}, FPS: {args.fps}')
    if args.show_undistort:
        new_K, _ = cv2.getOptimalNewCameraMatrix(K, D, (width, height), 1, (width, height))
    while True:
        ret, frame = cap.read()
        if not ret:
            print('Failed to grab frame')
            break
        cv2.imshow('Raw Camera', frame)
        if args.show_undistort:
            undistorted = cv2.undistort(frame, K, D, None, new_K)
            combined = np.hstack((frame, undistorted))
            cv2.imshow('Raw and Undistorted', combined)
            # cv2.imshow('Undistorted Camera', undistorted)
        key = cv2.waitKey(1)
        if key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
