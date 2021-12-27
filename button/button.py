import pygame as pg

class Button(object):
    def __init__(self,rect,color,function,**kwargs):
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
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text,True,color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text,True,color)
            self.text = self.font.render(self.text,True,self.font_color)

    def check_event(self,event,tip = 0):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            return self.on_click(event,tip)
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            return self.on_release(event,tip)
        else:
            return tip

    def on_click(self,event,tip = 0):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                return self.function()
            else:
                return tip
        else:
            return  tip

    def on_release(self,event,tip = 0):
        if self.clicked and self.call_on_release:
            self.clicked = False
            if self.click_sound:
                    self.click_sound.play()
            return self.function()
        else:
            return tip
        
    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def update(self,surface):
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