# 图卷积dgl库api之dgl.graph

import dgl

import torch

u = torch.tensor([0, 0, 0, 1]) # 每条边起点列表

v = torch.tensor([1, 2, 3, 3]) # 每条边终点列表

g = dgl.graph((u, v)) # 构建一个图，dgl.graph接受一个tuple，里边放起点列表张量和终点列表张量

g # 查看图概况

g.adjacency_matrix() # 查看图的邻接关系
# 可以看到有如下几条边：
# 0 -> 1
# 0 -> 2
# 0 -> 3
# 1 -> 3
