##首先创建游戏的画布
from tkinter import *
import random
import time

class Ball:
    def __init__(self, canvas, paddle, color): ##定义两个变量
        self.canvas = canvas ##导入类外定义的对象canvas，因为我们要在类里调用canvas对象来移动小球
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color) ##创建小球，并设置其颜色，把其ID作为变量存储起来方便后面移动它
        self.canvas.move(self.id, 245, 100) ##移动小球到画布的中心
        starts = [-3, -2, -1, 1, 2, 3] 
        random.shuffle(starts) ##用shuffle函数弄乱starts列表的顺序
        self.x = starts[0] ##小球在横放向每次移动的像素点不确定，所以才会乱窜
        self.y = -3 ##让小球在纵方向每次移动3个像素点
        self.canvas_height = self.canvas.winfo_height() ##调用winfo_height来获取当前画布的高度
        self.canvas_width = self.canvas.winfo_width() ##调用winfo_height来获取当前画布的宽度
        self.hit_bottom = False

    def hit_paddle(self, pos): #不太明白这个pos变量为什么可以直接引用
        paddle_pos = self.canvas.coords(self.paddle.id) ##[255, 29, 470, 45]
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id) ##coords函数通过小球的ID获取小球的坐标
        if pos[1] <= 0: ##pos[0] 代表小球左上角的纵坐标
            self.y = 3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if pos[3] >= self.canvas_height: ##pos[3] 代表小球右下角的纵坐标
            self.y = -3 ##-1是指反向移动，并不是跳到该像素点英东
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= self.canvas_width:
            self.x = -3
          ##你会发现这里无论x/y的值都是3/-3，这里表示小球每次移动的距离都是3个像素点，这样移动的速度会快一点，而且x=y=3是为了保持各个方向上一致  
        if self.hit_paddle(pos) == True:
            self.y = -3
        

class Paddle: ##这个类的定义没什么好解释的
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left) ##绑定键盘的方向键信号
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right) ##绑定键盘的方向键信号
        

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= self.canvas_width:
            self.x = 0

    def turn_left(self, evt): ##键盘按一次，小球就向左移动2个像素点,evt什么意思？
        self.x = -2

    def turn_right(self, evt): ##键盘按一次，小球向右移动2个像素点
        self.x = 2


        
tk = Tk()
tk.title("Game") ##命名画布的标题为“Game”
tk.resizable(0, 0) ##使用窗口的大小不可调整，参数0，0表示在水平方向和垂直方向都不可以改变
tk.wm_attributes("-topmost", 1) ##把包含我们画布的窗口放到所有其他窗口之前
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0) ##最后两个具名参数确保在画布之外没有边框，为了美观
canvas.pack() ##让画布按前一行给出的高度和宽度参数来调正其自身的大小
tk.update() ##为我们游戏中的动画初始化

paddle = Paddle(canvas, 'blue')
ball = Ball(canvas, paddle, 'red') ##类描述了它能做什么，但是实际上是对象在做这些事情。


##这个循环的意思是把小球移动一点点，在新的位置重画屏幕。
while 1:
    if ball.hit_bottom == False:
        ball.draw()
        paddle.draw()
    tk.update_idletasks() ##tk.update_idletasks和tk.update让tkinter快一点把画布上的东西画出来
    tk.update()
    time.sleep(0.01)
    
