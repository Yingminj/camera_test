import cv2

# 打开视频文件
cap = cv2.VideoCapture('cap/video_20251013_114234.mp4')

# 检查视频是否成功打开
if not cap.isOpened():
    print("无法打开视频文件")
    exit()

# 循环读取和显示帧
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow('Video', frame)
    
    # 按 'q' 键退出
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()