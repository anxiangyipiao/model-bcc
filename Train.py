
import torch
import torch.nn as nn
import torch.optim as optim
import os
import numpy as np
from torch.utils.data import Dataset, DataLoader


#[16, 14, 32, 3]

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



model = CNNRegressor()
# Define loss function and optimizer
criterion = nn.MSELoss()  # Mean Squared Error loss
optimizer = optim.Adam(model.parameters(), lr=0.001)  # Adam optimizer


class CustomDataset(Dataset):
    def __init__(self, x_data, y_data):
        self.x_data = x_data
        self.y_data = y_data

    def __len__(self):
        return len(self.y_data)

    def __getitem__(self, idx):
        x_sample = self.x_data[idx]
        y_sample = self.y_data[idx]
        return x_sample, y_sample


class Readdata(object):

    def __init__(self,
                 filenamex = None,
                 filenamey = None):

        self.filenamex = filenamex
        self.filenamey = filenamey
        self.datax = self._readx()
        self.dataset = self._mready()

    def _readx(self):

        datax = []
        file_names = os.listdir(self.filenamex)
        for file_name in file_names:
            
            file_path = os.path.join(self.filenamex, file_name)
            #读取矩阵
            matrix = np.loadtxt(file_path, delimiter=',')
            #转换
            matrix =  matrix.reshape((14, 32, 3))
           
            # 将读取的数据转换为张量
            x_train = torch.tensor(matrix, dtype=torch.float32)
           # print(x_train.shape)
            datax.append(x_train)
        
        return datax

    def _ready(self):
        
        with open(self.filenamey, "r") as f:
                lines = f.readlines()
        
        energy_values = [float(line.strip()) for line in lines if line.strip()]

        return  energy_values

    def _mready(self):
        
        energy_values = self._ready()
        normalized_values = self.normalize_value(energy_values)

        y_train = [torch.tensor(value, dtype=torch.float32) for value in normalized_values]

        # 创建自定义数据集实例并返回
        dataset = CustomDataset(self.datax, y_train)
        return dataset 
    
    def normalize_value(self,energy_values):
         # 进行归一化处理
        min_value = min(energy_values)
        max_value = max(energy_values)

        normalized_values = [(value - min_value) / (max_value - min_value) for value in energy_values]

        return normalized_values

    def denormalize_value(self,normalized_value):
        
        energy_values = self._ready()
        min_value = min(energy_values)
        max_value = max(energy_values)
       
        return normalized_value * (max_value - min_value) + min_value


dataset = Readdata(
    filenamex="trainx",
    filenamey="out.log"
).dataset


batch_size = 16  # 设置批大小
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)


for batch_x, batch_y in dataloader:
    print("Batch x shape:", batch_x.shape)
    print("Batch y shape:", batch_y.shape)
    break


num_epochs = 300

for epoch in range(num_epochs):
    for batch_x, batch_y in dataloader:
        optimizer.zero_grad()  # Clear gradients

        # Forward pass
        outputs = model(batch_x)
        
        # Calculate loss
        loss = criterion(outputs.squeeze(), batch_y)

        # Backpropagation
        loss.backward()
        optimizer.step()

    # Print progress
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

print('Training finished.')

# Save the trained model
torch.save(model.state_dict(), 'trained_model.pth')



# 加载验证数据集
validation_dataset = Readdata(
    filenamex="trainx",
    filenamey="out.log"
).dataset

validation_dataloader = DataLoader(validation_dataset, batch_size=batch_size, shuffle=False)

# 用于累积验证损失
validation_loss_sum = 0.0

# 将模型设置为评估模式
model.eval()

# 在验证集上进行验证
with torch.no_grad():
    for batch_x, batch_y in validation_dataloader:
        outputs = model(batch_x)
        loss = criterion(outputs.squeeze(), batch_y)
        validation_loss_sum += loss.item()

    # 计算平均验证损失
    average_validation_loss = validation_loss_sum / len(validation_dataloader)

# 将模型设置回训练模式
model.train()

# 打印验证损失
print(f'Validation Loss: {average_validation_loss:.4f}')