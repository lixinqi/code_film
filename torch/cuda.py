# pytorch模块之pytorch.cuda。

import torch

# 使用torch.cuda.is_available检测当前机器是否有cuda支持。

torch.cuda.is_available()

# 使用torch.cuda.device_count获取当前的cuda设备数。

torch.cuda.device_count()

# 使用torch.cuda.current_device获取当前的设备ID。

torch.cuda.current_device()

# 默认的当前设备ID是0。
# 使用torch.cuda.device切换当前的cuda设备ID。

device = torch.device('cuda:1') # 创建设备描述符。
with torch.cuda.device(device):
  print(torch.cuda.current_device())


# 可以看到，with作用域里的设备被切换成了设备1。

torch.cuda.current_device() # 再次确认当前设备ID。

# 还是默认的设备0。

