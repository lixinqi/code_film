# 调研pytorch是否有类似op placement的机制

import torch

# pytorch有个torch.cuda.device可以切换当前的cuda设备ID。但和oneflow的placement并没有相似之处，它能影响的只是torch.cuda.current_device。

device = torch.device('cuda:1') # 创建设备描述符。
with torch.cuda.device(device):
    print(torch.cuda.current_device())
    x = torch.tensor([1, 2, 3, 4])
    y = torch.tensor([5, 6, 7, 8])
    z = x + y


# 可以看到，with作用域里的设备被切换成了设备1。
# 我们再来看一下张量x和y所在的设备:

x.device
y.device

# 它们还是torch.tensor默认的cpu，说明张量的创建不受torch.cuda.device的影响，再看张量z的设备类型

z.device
# 这里起码说明加法op所产出的张量也不受torch.cuda.device影响。

# 实际上pytorch一样会有op placement类似的问题。只是它的规则简单得多：op所在的设备就是输入张量所在的设备。若多个输入张量所属设备不一致，直接报错。

a = torch.tensor([1, 2, 3, 4], device=device) # device即cuda:1
b = torch.tensor([1, 2, 3, 4], device=device) # a和b都在cuda:1上
c = torch.tensor([1, 2, 3, 4]) # c单独在cpu上

a + b # 注意看结果的设备属性

# 还是在cuda:1上，我们也可以差不多理解为此时的加法op也在cuda:1上

# 接下来看看输入设备不一致的情形

a + c

# 可以看到，输入设备不一致会直接引发异常。

