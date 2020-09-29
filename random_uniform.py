# 张量API综合对比之均匀分布

# numpy

import numpy
numpy.random.rand(3, 3)

# tensorflow

import tensorflow
tensorflow.ones((1)) # 这行代码只是为了初始化tensorflow，请忽略。

tensorflow.random.uniform((3, 3))

# pytorch

import torch
torch.rand(3, 3)

# 上述API均产生[0, 1)均匀分布的数据，注意参数形式的细微差别:

#  1. `numpy.random.rand`的第0个参数表示形状的第0维；

numpy.random.rand(3, 3) # 第0个参数表示第0维的大小为3

#  2. `tensorflow.random.uniform`的第0个参数表示整个形状；

tensorflow.random.uniform((3, 3)) # 第0个参数是(3, 3), 表示整个形状

#  3. torch.rand同时支持两种形式；

torch.rand(3, 3) # 这是OK的
torch.rand((3, 3)) # 这也是OK的
