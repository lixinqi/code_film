# pytorch api 之 tensor.grad

import torch

# 首先我们创建一个带后向的张量x

x = torch.tensor([1, 2, 3.], requires_grad=True)

# 使用grad属性获取后向张量

x.grad
type(x.grad)

# 默认是None。其实，如果x不带后向，x.grad也是None
# 接下来使用backward方法执行后向计算，首先我们定义一个全1的张量

ones = torch.ones((3,), dtype=torch.float32)

# 接着直接执行x.backward。

x.backward(ones) # ones.shape 必须等于x.shape

# 此时的x.grad已更新

x.grad

# 这个结果等于ones，这相当于执行了一个identity op的后向

# 接下来我们试着多次执行backward

x.backward(ones)

# 再观察x.grad值的变化

x.grad

# 其结果像是两次梯度叠加到了一起，我们再次执行backward验证一下。

x.backward(ones)
x.grad

# 果然，梯度是累加到一起的。
# 最后可以使用tensor.grad.data.zero_()清空梯度数据

x.grad.data.zero_()
x.grad

# 已清理，最后再玩一次backward

x.backward(ones)
x.grad

