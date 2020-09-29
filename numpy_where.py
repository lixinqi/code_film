# numpy api 之 where

import numpy as np

a = np.arange(10)
a
# a是0到9的序列。

# 接下来展示where的常见用法: numpy.where(condition, x, y)，且 condition，x和y的形状都一样

a.shape
(10 * a).shape
(a < 5).shape
#显然满足上述要求

np.where(a < 5, a, 10 * a) # 对每个元素，若值大于5，则乘以10，否则仍为原值。

# 首先，`a < 5`这个表达式计算每个值是否小于5

condition = a < 5
condition
# 前5个值为True, 后5个值为False。
condition[0:5] # True
condition[5:] # False

# 原表达式`np.where(a < 5, a, 10 * a)`即为`np.where(condition, a, 10 * a)`
# 对于condition里的每一个元素，如果值为真，则从a的对应位置取值；否则从(10 * a)里取值

ret = np.where(condition, a, 10 * a)
ret
# 可以看到，前5个值来自a，后5个值来自(10 * a)
ret[0:5]
np.all(ret[0:5] == a[0:5])
ret[5:]
np.all(ret[5:] == (10 * a)[5:])

# 详细资料见https://numpy.org/doc/stable/reference/generated/numpy.where.html


