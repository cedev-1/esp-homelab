# ui_pack.py
from micropython import const

class ModernUI:
    def __init__(self, display):
        self.tft = display
        
    BLACK   = const(0x0000)
    WHITE  = const(0xFFFF)
    GREY_F = const(0x3186)
    GREY_C = const(0x8410)
    RED  = const(0xF800)
    GREEN   = const(0x07E0)
        
    def fill_round_rect(self, x, y, w, h, r, color):
        
        self.tft.fill_rectangle(x + r, y, w - 2 * r, h, color)
        self.tft.fill_rectangle(x, y + r, w, h - 2 * r, color)

        self.tft.fill_circle(x + r, y + r, r, color)
        self.tft.fill_circle(x + w - r - 1, y + r, r, color)
        self.tft.fill_circle(x + r, y + h - r - 1, r, color)
        self.tft.fill_circle(x + w - r - 1, y + h - r - 1, r, color)

    def draw_border_rect(self, x, y, w, h, r, color_border, color_fill):
        
        self.fill_round_rect(x, y, w, h, r, color_border)
        self.fill_round_rect(x + 1, y + 1, w - 2, h - 2, r, color_fill)

    def draw_card(self, x, y, w, h, title, value, subtext, accent_color):
        r = 8
        
        self.draw_border_rect(x, y, w, h, r, self.WHITE, self.BLACK)
        self.tft.draw_text8x8(x + 10, y + 10, title, self.WHITE, self.BLACK)
        
        self.tft.draw_text8x8(x + 10, y + 35, str(value), accent_color, self.BLACK)
            
        self.tft.draw_text8x8(x + 10, y + h - 20, subtext, self.WHITE, self.BLACK)

    def draw_progress_bar(self, x, y, w, h, percent, color_active):
        r = h // 2
        
        self.draw_border_rect(x, y, w, h, r, self.WHITE, self.GREY_C)
        
        fill_w = int((percent / 100) * (w - 2))
        
        if fill_w > r * 2:
            self.fill_round_rect(x + 1, y + 1, fill_w, h - 2, r, color_active)
  
    def draw_card_static(self, x, y, w, h, title, subtext):
        r = 8
        self.draw_border_rect(x, y, w, h, r, self.WHITE, self.BLACK)
        
        self.tft.draw_text8x8(x + 10, y + 10, title, self.WHITE, self.BLACK)
        self.tft.draw_text8x8(x + 10, y + h - 20, subtext, self.WHITE, self.BLACK)

    def draw_bar_static(self, x, y, w, h):
        self.tft.draw_rectangle(x, y, w, h, self.WHITE)

    def update_card_value(self, x, y, w, value, color):
        
        self.tft.fill_rectangle(x + 10, y + 35, w - 20, 30, self.BLACK)
        self.tft.draw_text8x8(x + 10, y + 45, str(value), color, self.BLACK)

    def update_progress_bar(self, x, y, w, h, percent, color):
        self.tft.fill_rectangle(x + 1, y + 1, w - 2, h - 2, self.BLACK)
        
        fill_w = int((percent / 100) * (w - 2))
        
        if fill_w > 0:
            self.tft.fill_rectangle(x + 1, y + 1, fill_w, h - 2, color)
    
