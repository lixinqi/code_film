# pytorch小知识之requires_grad

import torch

# requires_grad 是pytorch张量的一个属性，表示该张量在后向计算时是否需要计算梯度数据。
# 首先定义一个张量x

x = torch.tensor([1, 2, 3, 4])

# 接下来查看x的requires_grad属性。

x.requires_grad

# 其默认值是False。
# 实际上，当你直接print(x)，requires_grad都不被展示出来。

x

# 没有requires_grad信息。

# 我们可以给torch.tensor添加keyward参数来指定其requires_grad的值

y = torch.tensor([1, 2, 3, 4], dtype=torch.float32, requires_grad=True) # 数据类型必须是浮点或复数

# 查看y的requires_grad属性

y.requires_grad

# 事实上直接print(y)，requires_grad会被打印出来，因为它为True。

y

# 如果数据类型不是浮点或者复数，同时requires_grad设置为True，此时会有异常抛出。

torch.tensor([1, 2, 3, 4], requires_grad=True) # 此时的dtype是默认的torch.int64

# 错误提示信息为：只有浮点和复数类型的张量才能要求有后向

