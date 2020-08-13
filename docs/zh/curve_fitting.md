
## 使用遗传算法进行曲线拟合

随机生成训练数据
```python
import numpy as np
import matplotlib.pyplot as plt
from sko.GA import GA

x_true = np.linspace(-1.2, 1.2, 30)
y_true = x_true ** 3 - x_true + 0.4 * np.random.rand(30)
plt.plot(x_true, y_true, 'o')
```
![ga_curve_fitting0](https://github.com/guofei9987/pictures_for_blog/blob/master/heuristic_algorithm/ga_curve_fitting0.png?raw=true)


构造残差
```python
def f_fun(x, a, b, c, d):
    return a * x ** 3 + b * x ** 2 + c * x + d


def obj_fun(p):
    a, b, c, d = p
    residuals = np.square(f_fun(x_true, a, b, c, d) - y_true).sum()
    return residuals
```

使用 scikit-opt 做最优化
```python
ga = GA(func=obj_fun, n_dim=4, size_pop=100, max_iter=500,
        lb=[-2] * 4, ub=[2] * 4)

best_params, residuals = ga.run()
print('best_x:', best_params, '\n', 'best_y:', residuals)
```

画出拟合效果图
```python
y_predict = f_fun(x_true, *best_params)

fig, ax = plt.subplots()

ax.plot(x_true, y_true, 'o')
ax.plot(x_true, y_predict, '-')

plt.show()
```

![ga_curve_fitting1](https://github.com/guofei9987/pictures_for_blog/blob/master/heuristic_algorithm/ga_curve_fitting1.png?raw=true)
