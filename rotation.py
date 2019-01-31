from PIL import Image, ImageDraw
block_size = 128
pixel_size = block_size//8

def lerp(start, end, perc):    
    return perc * (end-start) + start
    
def inverse_lerp(start, end, value):
    return (value-start) / (end-start)
    
def generate_block(im, top_left, perc):
    #black border
    top_left2 = top_left[0] - pixel_size, top_left[1]-pixel_size
    bottom_right = (top_left[0]+block_size,top_left[1]+block_size)
    im.rectangle((top_left2,bottom_right),fill=(0,0,0,255))
    #red border    
    bottom_right = bottom_right[0] - pixel_size, bottom_right[1]-pixel_size
    im.rectangle((top_left,bottom_right),fill=(255,0,0,255))    
    #white fill
    top_left_w = top_left[0] + pixel_size, top_left[1]+pixel_size
    bottom_right = bottom_right[0] - pixel_size, bottom_right[1]-pixel_size
    im.rectangle((top_left_w,bottom_right),fill=(255,255,255,255))
    #white corner
    perc %= 1.0    
    if perc <= 0.25:
        perc = inverse_lerp(0.0,0.25,perc)
        top_left_x = lerp(top_left[0],top_left[0]+pixel_size*6,perc)
        top_left = (top_left_x,top_left[1])
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 0.5:
        perc = inverse_lerp(0.25,0.5,perc)
        top_left_x = top_left[0]+pixel_size*6
        top_left_y = lerp(top_left[1],top_left[1]+pixel_size*6,perc)     
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 0.75:
        perc = inverse_lerp(0.5,0.75,perc)
        top_left_x = lerp(top_left[0]+pixel_size*6,top_left[0],perc)
        top_left_y = top_left[1]+pixel_size*6
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 1.0:
        perc = inverse_lerp(0.75,1.0,perc)
        top_left_x = top_left[0]
        top_left_y = lerp(top_left[1]+pixel_size*6,top_left[1],perc)
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))        
        
def rotate(image, angle, color):
    bg = Image.new("RGBA", image.size, color)
    im = image.convert("RGBA").rotate(angle)
    bg.paste(im, im)
    return bg
    
if __name__ == '__main__':   
    img = Image.new('RGBA', (block_size*4+pixel_size,block_size*4+pixel_size), (0,255,0,0));
    im = ImageDraw.Draw(img)
    offset = block_size/2
    perc = 1.0
    generate_block(im,(offset+block_size+pixel_size,offset+pixel_size), perc)
    generate_block(im,(offset+pixel_size           ,offset+block_size+pixel_size), perc)
    generate_block(im,(offset+block_size+pixel_size,offset+block_size+pixel_size), perc)
    generate_block(im,(offset+block_size+pixel_size,offset+2* block_size+pixel_size), perc)
    
    del im
    img = rotate(img,perc*360,(0,255,0,0))
    img.save("tspin001.png")

