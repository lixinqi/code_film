# Paddle api 之 fluid.dygraph.grad
import paddle.fluid as fluid

# fluid.dygraph.grad 是 Paddle 动态图下获取反向传播梯度的 API

def test_dygraph_grad(create_graph):
    with fluid.dygraph.guard():
        x = fluid.layers.ones(shape=[1], dtype='float32')
        x.stop_gradient = False
        y = x * x
        """
        接受输出outputs，输入inputs
        
        create graph 属性表示是否创建计算过程中的反向图，若值为False，则计算过程中的反向图会释放
        
        retain_graph 属性表示是否保留计算梯度的前向图。如果保留则可对同一张图求两次反向
        
        grad_outputs 属性表示outputs的梯度初始值，默认为None
        
        注意这里create_graph对梯度的影响
        """
        # dx等于y对x求导数，dx = 2*x
        dx = fluid.dygraph.grad(outputs=[y], inputs=[x], create_graph=create_graph, retain_graph=True)[0] 
        # 计算 z = y + dx
        z = y + dx
        # 进行反向传播
        z.backward()
        # 返回 x 的 梯度
        return x.gradient()

# 当create_graph = False 则 dx 不创建反向图，因此它不会反向传播给 x

# z = x*x + dx，此时反向传播给x的仅仅只有第一项导数，x.gradient = 2*x = 2

test_dygraph_grad(create_graph=False)

# 当create_graph = True 则 dx 创建反向图

# z = x*x + dx，此时反向传播给x的是z第一，第二项导数，x.gradient = 2*x + 2 = 4

test_dygraph_grad(create_graph=True) 

