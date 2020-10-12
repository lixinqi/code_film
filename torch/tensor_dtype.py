# pytorch.tensor关于dtype的小知识

import torch

# 可以使用dtype指定张量的数据类型。

x = torch.tensor([1, 2, 3, 4], dtype=torch.float32)
x.dtype

# 顺带说一句，torch.float就是torch.float32。

torch.float is torch.float32

# 对于默认整型的python数组，由它构建的张量的dtype默认是torch.int64。

x = torch.tensor([1, 2, 3, 4])
x.dtype
# 默认是torch.int64。
# 但只要其中一个数值写成浮点的形式，其dtype就是浮点。

x = torch.tensor([1, 2, 3, 4.])
x.dtype
# 数值也都以torch.float32存储

x

