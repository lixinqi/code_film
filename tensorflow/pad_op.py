# tensorflow v2 api 之 tf.pad

import tensorflow as tf
import numpy as np

# 首先我们创建一个常量 Tensor 表示 pad op 的输入

t = tf.constant([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
t

# 接着再创建另一个常量 Tensor 表示 padding 的大小

paddings = tf.constant([[1, 1], [2, 2]]) # 表示上下各 pad 1 左右各 pad 2
paddings

# tensorflow pad op 提供 3 种 padding 模式, "CONSTANT", "REFLECT" 和 "SYMMETRIC"

# "CONSTANT" 模式表示在边缘处补0
tf.pad(t, paddings, "CONSTANT")

# "REFLECT" 模式表示以原图像边缘一圈像素为对称中心, pad 的内容与除去边缘的图像内容呈镜像关系
tf_reflect = tf.pad(t, paddings, "REFLECT")
tf_reflect

# 下面用 numpy 代码解释 "REFLECT" 模式是如何计算的
# 先计算左右的 pad 再计算上下的 pad

# 把 tensorflow 的张量转换为 numpy array
input_nd = t.numpy()

# 新建易读变量保存 paddings 张量内的值
pad_top = paddings[0][0]
pad_bottom = paddings[0][1]
pad_left = paddings[1][0]
pad_right = paddings[1][1]

# 新建一个保存 "REFLECT" pad 的计算结果
numpy_reflect = np.zeros((t.shape[0] + pad_top + pad_bottom, t.shape[1] + pad_left + pad_right), np.int32)

# 填充结果中间的部分
numpy_reflect[pad_top : numpy_reflect.shape[0] - pad_bottom, pad_left : numpy_reflect.shape[1] - pad_right] = input_nd

# 先计算左右 pad 的结果
for h in range(pad_top, numpy_reflect.shape[0] - pad_bottom):
    # 计算左边 pad
    for w in range(pad_left):
        numpy_reflect[h, w] = numpy_reflect[h, pad_left * 2 - w]
    # 计算右边 pad
    for w in range(numpy_reflect.shape[1] - pad_right, numpy_reflect.shape[1]):
        numpy_reflect[h, w] = numpy_reflect[h, 2 * (numpy_reflect.shape[1] - pad_right - 1) - w]

# 计算顶部 pad 的结果
for h in range(pad_top):
    numpy_reflect[h, :] = numpy_reflect[pad_top * 2 - h, :]

# 计算底部 pad 的结果
for h in range(numpy_reflect.shape[0] - pad_bottom, numpy_reflect.shape[0]):
    numpy_reflect[h, :] = numpy_reflect[2 * (numpy_reflect.shape[0] - pad_bottom - 1) - h, :]

# 最后可以看到 numpy 的计算结果和 tensorflow 的计算结果一致
numpy_reflect
tf_reflect.numpy()

# "SYMMETRIC" 模式与 "REFLECT" 类似, 区别在于是直接复制边界处的像素然后做镜像填充
tf_symmetric = tf.pad(t, paddings, "SYMMETRIC")
tf_symmetric

# 下面用 numpy 代码解释 "SYMMETRIC" 模式是如何计算的
# 同样是先计算左右的 pad, 然后再计算上下的 pad

# 新建一个保存 "SYMMETRIC" pad 的计算结果
numpy_symmetric = np.zeros((t.shape[0] + pad_top + pad_bottom, t.shape[1] + pad_left + pad_right), np.int32)

# 填充结果中间的部分
numpy_symmetric[pad_top : numpy_symmetric.shape[0] - pad_bottom, pad_left : numpy_symmetric.shape[1] - pad_right] = input_nd

# 先计算左右 pad 的结果
for h in range(pad_top, numpy_symmetric.shape[0] - pad_bottom):
    # 计算左边 pad
    for w in range(pad_left):
        numpy_symmetric[h, w] = numpy_symmetric[h, pad_left * 2 - w - 1]
    # 计算右边 pad
    for w in range(numpy_symmetric.shape[1] - pad_right, numpy_symmetric.shape[1]):
        numpy_symmetric[h, w] = numpy_symmetric[h, 2 * (numpy_symmetric.shape[1] - pad_right) - w - 1]

# 计算顶部 pad 的结果
for h in range(pad_top):
    numpy_symmetric[h, :] = numpy_symmetric[pad_top * 2 - h - 1, :]

# 计算底部 pad 的结果
for h in range(numpy_symmetric.shape[0] - pad_bottom, numpy_symmetric.shape[0]):
    numpy_symmetric[h, :] = numpy_symmetric[2 * (numpy_symmetric.shape[0] - pad_bottom) - h - 1, :]

# 最后可以看到 numpy 的计算结果和tensorflow的计算结果一致
numpy_symmetric
tf_symmetric.numpy()
