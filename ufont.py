"""Custom 7x4
"""

def draw_one(x,y,d):
    """
      X 
     XX 
    X X 
      X 
      X 
      X 
     XXX
    """
    d.pixel(x,y+2,1)
    d.pixel(x+1,y+1,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.vline(x+2,y,7,1)
    d.pixel(x+3,y+6,1)

def draw_tow(x,y,d):
    """
     XX 
    X  X
       X
      X
     X
    X 
    XXXX
    """
    d.pixel(x,y+1,1)
    d.pixel(x,y+5,1)
    d.pixel(x,y+6,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+4,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+6,1)
    d.pixel(x+3,y+1,1)
    d.pixel(x+3,y+2,1)
    d.pixel(x+3,y+6,1)

def draw_three(x,y,d):
    """
     XX 
    x  X
       X
      X 
       X
    x  X
     XX 
    """
    d.pixel(x,y+1,1)
    d.pixel(x,y+5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+6,1)
    d.pixel(x+3,y+1,1)
    d.pixel(x+3,y+2,1)
    d.pixel(x+3,y+4,1)
    d.pixel(x+3,y+5,1)

def draw_four(x,y,d):
    """
    X  X
    X  X
    X  X
    XXXX
       X
       X
       X
    """
    d.pixel(x,y,1)
    d.pixel(x,y+1,1)
    d.pixel(x,y+2,1)
    d.pixel(x,y+3,1)
    d.pixel(x+1,y+3,1)
    d.pixel(x+2,y+3,1)
    d.vline(x+3,y,7,1)

def draw_five(x,y,d):
    """
    XXXX
    X
    X X
    XX X
       X
    X  X
     XX 
    """
    d.pixel(x,y,1)
    d.pixel(x,y+1,1)
    d.pixel(x,y+2,1)
    d.pixel(x,y+3,1)
    d.pixel(x,y+5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+3,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+2,1)
    d.pixel(x+2,y+6,1)
    d.pixel(x+3,y,1)
    d.pixel(x+3,y+3,1)
    d.pixel(x+3,y+4,1)
    d.pixel(x+3,y+5,1)

def draw_six(x,y,d):
    """
     XX
    X  X
    X
    XXX 
    X  X
    X  X
     XX 
    """
    d.vline(x,y+1,5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+3,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+6,1)
    d.pixel(x+3,y+1,1)
    d.pixel(x+3,y+4,1)
    d.pixel(x+3,y+5,1)

def draw_seven(x,y,d):
    """
    XXXX
       X
       X
      X
      X
     X
     X
    """
    d.pixel(x,y,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+5,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+4,1)
    d.pixel(x+3,y,1)
    d.pixel(x+3,y+1,1)
    d.pixel(x+3,y+2,1)

def draw_eight(x,y,d):
    """
     XX 
    X  X
    X  X
     XX
    X  X
    X  X
     XX 
    """
    d.pixel(x,y+1,1)
    d.pixel(x,y+2,1)
    d.pixel(x,y+4,1)
    d.pixel(x,y+5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+3,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+6,1)
    d.pixel(x+3,y+1,1)
    d.pixel(x+3,y+2,1)
    d.pixel(x+3,y+4,1)
    d.pixel(x+3,y+5,1)

def draw_nine(x,y,d):
    """
     XX 
    X  X
    X  X
     XXX
       X
    X  X
     XX 
    """
    d.pixel(x,y+1,1)
    d.pixel(x,y+2,1)
    d.pixel(x,y+5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+3,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+3,1)
    d.pixel(x+2,y+6,1)
    d.vline(x+3,y+1,5,1)

def draw_zero(x,y,d):
    """
     XX
    X  X
    X  X
    X  X
    X  X
    X  X
     XX
    """
    d.vline(x,y+1,5,1)
    d.pixel(x+1,y,1)
    d.pixel(x+1,y+6,1)
    d.pixel(x+2,y,1)
    d.pixel(x+2,y+6,1)
    d.vline(x+3,y+1,5,1)
    

font_numbers = {
    '1': draw_one,
    '2': draw_tow,
    '3': draw_three,
    '4': draw_four,
    '5': draw_five,
    '6': draw_six,
    '7': draw_seven,
    '8': draw_eight,
    '9': draw_nine,
    '0': draw_zero,
}

def draw_number(display, x, y, text):
    for idx, t in enumerate(text):
        if t in font_numbers:
            font_numbers[t](x+(5*idx), y, display)