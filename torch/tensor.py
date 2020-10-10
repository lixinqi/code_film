# torch api 之 torch.tensor
import torch

# torch.tensor类似于numpy.array

x = torch.tensor([1, 2, 3, 4]) # 由list创建一个torch.Tensor对象

x.shape # 形状

# 注意这个返回结果类型是torch.Size，不是tuple，但差别不大。

x.dtype # 数据类型

x.device # 所在设备，这是torch.Tensor相比numpy.ndarray多出来的概念

# 默认就是在cpu上
# 如果想创建gpu上的张量，需要指定device
# 首先用torch.device创建设备描述符

device = torch.device('cuda:0') # 注意不是字符串gpu:0，而是cuda:0

device

# 设备描述符有类型type和编号index属性

# 给toch.tensor准备device参数，可以创建指定设备上的张量

x = torch.tensor([1, 2, 3, 4], device=device) # 如果首次创建该设备上的张量，则可能需要等待cuda初始化

x # 数值没变化，多了一个device属性

x.device # 注意观察其device属性
