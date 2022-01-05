# 2048_master

**Designer：Jiazhen-Lei & ZhaoGY**

### 1.设计内容

​	《2048》小游戏作为近年非常火爆的移动端小游戏，在大家碎片化的时间里，调剂着大家忙碌的生活；当前疫情封闭，也可以作为一个宿舍消遣的娱乐手段，《2048》简单的游戏规则和操作方式在放松之余也活跃了思维。传统的《2048》只具有了基本的单一模式，上、下、左、右四种移动手段。而本项目，团队成员希望设计一款在原有基础《2048》，增加提示和AI模式。结合本学期张老师上课所授和同学们分享的丰富Python库，理论与项目实践结合，提高团队成员面向对象项目开发能力和分工合作能力。
​	本项目程序提供了三种模式，即基础、基础+提醒、AI。项目团队成员借助Github进行跨时空合作。项目主要借助Python中的Pygame模块实现游戏效果，利用四层深度的MinMax搜索实现AI功能，提示功能通过计算一次AI预测下一步实现。采用Python面向对象编程思路，主体项目框架采用模块化编程，具体分为：animate动画模块、board界面模块、button按钮模块、game游戏模块、show显示模块、sound音效模块。

### 2.平台

Window10、Linux

### 3.开发工具

VScode

### 4.总体方案

​		整体上我们使用Pygame库来实现界面以及用户交互，并采用面向对象的设计方法，将各个游戏模块封装成类，在各个类中实现自己的功能，包括实现棋盘的Board类，实现数字块的Block类，实现动画的Animate类，实现按键的Button类等。并通过play.py和action.py进行控制，通过show进行显示，从而实现整个游戏过程。
​		我们的主脚本为play.py，在这个脚本中我们调用上述的各个类以及逻辑控制脚本base2048.py以及AI2048.py，在逻辑控制脚本中我们处理用户输入并将对board进行对应的操作，例如向上向下，增加数字等等。
​		而在Board类中我们定义了各种对棋盘的各种操作，比如移动和添加数字。同时为了更方便的实现动画，我们没有将每个数字块直接作为数字存入二维列表，而是使用了一个Block类，并在其中存储当前块的数字和上一时刻的位置，以及对应的动画类型以及动画数据，而动画数据又是通过Animate类进行处理和保存的。这样我们只需要每次调用show，将其中当前帧的数据显示出来，并调用animate类中的处理函数计算下一帧的数据，就能实现动画的效果了.
​		同时因为Pygame没有提供现成的按钮等控件，我们只能自己实现自己的按钮逻辑，为了更方便的使用，我们将button也封装成了一个类，并在button类中集成一些逻辑处理，方便使用。程序的流程大致如下图所示。
![image-20220105154309760](C:\Users\DEcade\AppData\Roaming\Typora\typora-user-images\image-20220105154309760.png)     

**各个函数功能关系：**
由于函数众多，我们仅对比较重要的函数进行说明,在play.py中，我们仅有一个play函数，没有参数输入，在其中我们显示画面并处理Button的点击，其余的逻辑均在button的响应中处理。
		在逻辑处理部分，start_base_2048是基础模式的逻辑处理函数def start_base_2048(board: Board, button, extip)，其中board包含当前的棋盘信息，button包含当前的按钮信息，extip为当前的tip值，返回值为处理后游戏是否结束，以及用于显示的tip，同理AI_2048()与start_base_2048的参数传递相同。
		AI的核心是search(thisBoard: Board, depth, alpha, beta, positions, cutoffs, plyaerTurn: bool) -> searchResult函数，其中thisBoard为当前棋盘局面；depth为当前搜索深度，在递归调用中不断减小，直到为0结束递归；alpha，beta，positions与cutoffs则是用于剪枝的部分，从而减少搜索次数，提高效率；plyaerTurn是在minmax搜索中用于区分最大值轮和最小值轮所需的。其返回值中包含了bestMove以及下次递归所需要的参数。
		Board类则包含了各种对棋盘的操作函数，包括四个move以及添加和删除函数。 Button包含了按钮的逻辑。Animate包含了几种不同的平滑动画和对应的处理方式。具体的在功能实现中进一步阐明。
		文件结构如下图。

![image-20220105154052635](C:\Users\DEcade\AppData\Roaming\Typora\typora-user-images\image-20220105154052635.png)

### 5.使用

 		在play.py路径下

```python
python play.py
```

