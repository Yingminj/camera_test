import yaml
import numpy as np

def load_camera_intrinsics(camera_type):
    """
    加载指定相机的内参。
    
    Args:
        camera_type (str): 'head' 或 'top'
    
    Returns:
        tuple: (camera_matrix, dist_coeffs)
    """
    if camera_type == 'head':
        path = 'camera_test/camera_info_640/head.yaml'
    elif camera_type == 'top':
        path = 'camera_test/camera_info_640/top.yaml'
    else:
        raise ValueError("Invalid camera type. Choose 'head' or 'top'.")
    
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    camera_matrix = np.array(data['camera_matrix']['data']).reshape(3, 3)
    dist_coeffs = np.array(data['distortion_coefficients']['data'])
    projection_matrix = np.array(data['projection_matrix']['data']).reshape(3, 4)[:3, :3]
    
    return camera_matrix, dist_coeffs, projection_matrix

def load_camera_extrinsics():
    """
    加载top到head的外参。
    
    Returns:
        tuple: (translation, quaternion)
    """
    path = 'camera_test/camera_info_640/top_to_head_camera.yaml'
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    translation = np.array(data['translation'])
    quaternion = np.array(data['quaternion'])
    
    return translation, quaternion

def get_all_camera_params():
    """
    加载所有相机的内参和外参。
    
    Returns:
        dict: {
            'head': (camera_matrix, dist_coeffs),
            'top': (camera_matrix, dist_coeffs),
            'extrinsics': (translation, quaternion)
        }
    """
    params = {}
    params['head'] = load_camera_intrinsics('head')
    params['top'] = load_camera_intrinsics('top')
    params['extrinsics'] = load_camera_extrinsics()
    return params

# 示例用法
if __name__ == "__main__":
    # 加载head内参
    head_matrix, head_dist = load_camera_intrinsics('head')
    print("Head Camera Matrix:")
    print(head_matrix)
    print("Head Distortion Coefficients:")
    print(head_dist)
    
    # 加载外参
    trans, quat = load_camera_extrinsics()
    print("\nTranslation:")
    print(trans)
    print("Quaternion:")
    print(quat)
    
    # 加载所有参数
    all_params = get_all_camera_params()
    print("\nAll Parameters Loaded:")
    for key, value in all_params.items():
        print(f"{key}: {value}")