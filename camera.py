import cv2
import datetime

def start_camera(device, width=640, height=480, fps=30):
    cap = cv2.VideoCapture(device)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FPS, fps)
    
    if not cap.isOpened():
        print("无法打开相机")
        return
    
    recording = False
    out = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Camera', frame)
        if recording:
            out.write(frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('e'):
            # 拍照
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cap/photo_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"照片已保存: {filename}")
        elif key == ord('r'):
            # 切换录制状态
            if not recording:
                # 开始录制
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"cap/video_{timestamp}.mp4"
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(filename, fourcc, fps, (width, height))
                recording = True
                print(f"开始录制: {filename}")
            else:
                # 停止录制
                out.release()
                recording = False
                print("录制停止")
    
    if recording and out is not None:
        out.release()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera(device="/dev/video0", fps=60)