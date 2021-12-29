import pygame as pg

class Button(object):
    """实现按键最基本的操作"""
    def __init__(self,rect,color,function,**kwargs):
        """
        初始化
        参数:
            rect:按键大小位置
            color:颜色
            function:回调函数
            clicked:按下状态
            hovered:悬停状态
            hover_text:悬停显示文本
            clicked_text:按下显示文本
            process_kwargs(kwargs):其他用户个性化配置，kwargs字典数据

        说明:
            无特殊要求hover和click的颜色和文字与released相同
        """
        self.rect = pg.Rect(rect)
        self.color = color
        self.function = function
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self,kwargs):
        """其他用户自定义设置"""
        settings = {"text" : None,
                    "font" : pg.font.Font(None,24),
                    "call_on_release" : True,
                    "hover_color" : None,
                    "clicked_color" : None,
                    "font_color" : (106, 90, 205),
                    "hover_font_color" : None,
                    "clicked_font_color" : None,
                    "click_sound" : None,
                    "hover_sound" : None}
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("Button has no keyword: {}".format(kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        """按键文本显示方法"""
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)

    def check_event(self,event,tip = 0):
        """
        按键检测方法
        参数:
            event:事件类型
            tip:提示索引，默认为0，显示空
        """
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # 有按键按下动作
            return self.on_click(event,tip)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1: # 有按键释放动作
            return self.on_release(event,tip)
        else: # 无事件
            return tip

    def on_click(self,event,tip = 0):
        """
        按键按下使能方法
        参数:
            event:事件类型
            tip:提示索引，默认为0，显示空
        """
        if self.rect.collidepoint(event.pos): # 按键冲突检查 判断是否为本实例按键区域
            self.clicked = True
            if not self.call_on_release:
                return self.function() # 执行回调函数
            else:
                return tip
        else:
            return  tip

    def on_release(self,event,tip = 0):
        """
        按键释放方法
        参数:
            event:事件类型
            tip:提示索引，默认为0，显示空
        """
        if self.clicked and self.call_on_release:
            self.clicked = False
            if self.click_sound:
                    self.click_sound.play() # 按键按下音效
            return self.function() # 执行回调函数
        else:
            return tip
        
    def check_hover(self):
        """
        按键悬停方法
        返回值:
            悬停状态
        """
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self,surface):
        """
        按键刷新方法
        参数:
            surface:作用界面实例
        """
        color = self.color
        text = self.text
        self.check_hover()
        if self.clicked and self.clicked_color:
            color = self.clicked_color
            if self.clicked_font_color:
                text = self.clicked_text
        elif self.hovered and self.hover_color:
            color = self.hover_color
            if self.hover_font_color:
                text = self.hover_text
        surface.fill(color,self.rect.inflate(0,0))
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text,text_rect)