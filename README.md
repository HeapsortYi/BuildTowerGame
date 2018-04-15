# BuildTowerGame
游戏AI中的算法-DQN实例

有一天，我们想盖很高很高层的塔，然而北大里的建筑都不能高过博雅塔……于是我们随手写了一个界面简陋的游戏

# 需要的环境
- Python 3.5+/Python 2.7（Python 2.7我没有测试）
- Keras 2.0+
- [Pygame](https://www.pygame.org/wiki/GettingStarted)
- tensorflow
- scikit-image
- numpy
- 其他提醒你需要安装的库

# 如何运行？
## 运行游戏
```
python build_tower.py
```
按下空格放下积木

## 运行训练好的模型自动玩游戏
```
python DQN.py -m 'Run'
```

## 训练模型
删除已有的model.json和model.h5
```
python DQN.py -m 'Train'
```

# 部分效果展示
## 完成DQN训练
![play](/gif/play.gif)

## 训练中
**还未正式开始进行训练，通过𝜖-greedy策略进行observe，初始化记忆池D：**
![observe](/gif/training_observe_resize.gif)

**一边采样加入记忆池D，一边选取mini-batch的样本进行训练的explore过程：**
![explore](/gif/training_explore_resize.gif)

# Reference
1. [Using Keras and Deep Q-Network to Play FlappyBird](https://yanpanlau.github.io/2016/07/10/FlappyBird-Keras.html)
