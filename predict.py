import torch
import torch.nn as nn
import numpy as np

# 定义反归一化函数
def denormalize_value(normalized_value, min_value, max_value):
    return normalized_value * (max_value - min_value) + min_value


class CNNRegressor(nn.Module):
    def __init__(self):
        super(CNNRegressor, self).__init__()
        
        self.conv1 = nn.Conv2d(in_channels=14, out_channels=16, kernel_size=3, stride=1, padding=1)   # 32*3*16
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=64, kernel_size=3, stride=1, padding=1)   # 32*3*64
        self.conv3 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=1, padding=1)   # 32*3*128  

        self.fc1 = nn.Linear(128 * 32 * 3, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 1)
        
     
    def forward(self, x):

        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(-1, 128 * 32 * 3)
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# 创建模型实例
model = CNNRegressor()

# 加载训练好的模型权重
model.load_state_dict(torch.load('trained_model.pth'))
model.eval()

# 读取训练集的最小值和最大值（用于反归一化）
min_original = -1032.1597  # 替换为实际的最小值
max_original = -766.93186  # 替换为实际的最大值

# 创建需要预测的输入数据（这里仅示范，根据您的实际数据格式进行处理）
# input_data = torch.tensor(np.random.random((1, 14, 32, 3)), dtype=torch.float32)  # 替换为您的输入数据

matrix = np.loadtxt("trainx/POSCAR0.51.csv", delimiter=',')

matrix =  matrix.reshape((14, 32, 3))
           
# 将读取的数据转换为张量
input_data = torch.tensor(matrix, dtype=torch.float32)



# 进行预测
with torch.no_grad():
    normalized_prediction = model(input_data)
    
# 反归一化预测结果
original_prediction = denormalize_value(normalized_prediction.item(), min_original, max_original)

# 打印预测结果
print('Normalized Prediction:', normalized_prediction.item())
print('Original Prediction:', original_prediction)
