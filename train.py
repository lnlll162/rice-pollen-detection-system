import yaml
from ultralytics import YOLO
import os

# 设置环境变量
os.environ['KMP_DUPLICATE_LIB_OK']='TRUE'
os.environ['YOLO_SKIP_FONT_CHECK'] = 'TRUE'  # 跳过字体检查

# 获取当前目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 加载自定义超参数
def load_hyperparameters(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            hyp = yaml.safe_load(f)
        return hyp
    except FileNotFoundError:
        print(f"警告：超参数文件 {path} 不存在，使用默认参数")
        return {}

# 应用超参数到模型
def apply_hyperparameters(model, hyp):
    for k, v in hyp.items():
        setattr(model, k, v)

if __name__ == '__main__':
    # 设置超参数文件路径
    hyp_path = os.path.join(current_dir, "hyps", "hyp.scratch.yaml")
    
    # 加载超参数
    hyp = load_hyperparameters(hyp_path)
    
    # 加载预训练模型
    model = YOLO("yolov8x.pt")
    
    # 应用超参数
    if hyp:
        apply_hyperparameters(model, hyp)
    
    # 设置数据配置文件路径
    data_yaml = os.path.join(current_dir, "flower.yaml")
    
    # 开始训练
    results = model.train(
        data=data_yaml,
        epochs=100,
        imgsz=640,
        batch=1,
        project=current_dir,
        name="train8"  # 新的训练记录名称
    )



    # Load a model
    # model = YOLO('yolov8n.pt')  # load a pretrained model (recommended for training)

    # # Train the model
    # results = model.train(data='flower.yaml', epochs=100, imgsz=1024, batch = 8)
