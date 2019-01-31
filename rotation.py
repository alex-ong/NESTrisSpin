from PIL import Image, ImageDraw
block_size = 128
pixel_size = block_size//8

colors = {'t': (146,52,0,255),
          'o': (146,52,0,255),
          'l': (196,144,40,255),
          'j': (146,52,0,255),
          's': (146,52,0,255),
          'z': (196,144,40,255),
          'i': (146,52,0,255)}
          

def lerp(start, end, perc):    
    return perc * (end-start) + start
    
def inverse_lerp(start, end, value):
    return (value-start) / (end-start)

def generate_white_corner(im,top_left,perc,limit):
    perc %= 1.0    
    if perc <= 0.25:
        perc = inverse_lerp(0.0,0.25,perc)
        top_left_x = lerp(top_left[0],top_left[0]+pixel_size*limit,perc)
        top_left = (top_left_x,top_left[1])
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 0.5:
        perc = inverse_lerp(0.25,0.5,perc)
        top_left_x = top_left[0]+pixel_size*limit
        top_left_y = lerp(top_left[1],top_left[1]+pixel_size*limit,perc)     
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 0.75:
        perc = inverse_lerp(0.5,0.75,perc)
        top_left_x = lerp(top_left[0]+pixel_size*limit,top_left[0],perc)
        top_left_y = top_left[1]+pixel_size*limit
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))
    elif perc <= 1.0:
        perc = inverse_lerp(0.75,1.0,perc)
        top_left_x = top_left[0]
        top_left_y = lerp(top_left[1]+pixel_size*limit,top_left[1],perc)
        top_left = (top_left_x, top_left_y)        
        bottom_right = (top_left[0]+pixel_size,top_left[1]+pixel_size)
        im.rectangle((top_left,bottom_right),fill=(255,255,255,255))       
        
def generate_block(im, top_left, perc, solid=False,primary=(255,0,0,255)):
    #black border
    top_left2 = top_left[0] - pixel_size, top_left[1]-pixel_size
    bottom_right = (top_left[0]+block_size,top_left[1]+block_size)
    im.rectangle((top_left2,bottom_right),fill=(0,0,0,255))
    #red border    
    bottom_right = bottom_right[0] - pixel_size, bottom_right[1]-pixel_size
    im.rectangle((top_left,bottom_right),fill=primary)    
    if (not solid):
        #white fill
        top_left_w = top_left[0] + pixel_size, top_left[1]+pixel_size
        bottom_right = bottom_right[0] - pixel_size, bottom_right[1]-pixel_size
        im.rectangle((top_left_w,bottom_right),fill=(255,255,255,255))
        
    #white corner
    generate_white_corner(im,top_left,perc,6)
    
    #generate three point triangle...
    if (solid):
        top_left = (top_left[0] + pixel_size, top_left[1] + pixel_size)
        generate_white_corner(im,top_left,perc,4)
        generate_white_corner(im,top_left,perc+1/16,4)
        generate_white_corner(im,top_left,perc-1/16,4)
        
def rotate(image, angle, color):
    bg = Image.new("RGBA", image.size, color)
    im = image.convert("RGBA").rotate(angle)
    bg.paste(im, im)
    return bg

def gen_t(im, perc, color):
    offset = block_size + pixel_size
    generate_block(im,(offset+block_size,offset), perc,False,color)
    generate_block(im,(offset,offset+block_size), perc,False,color)
    generate_block(im,(offset+block_size,offset+block_size), perc,False,color)
    generate_block(im,(offset+block_size,offset+2* block_size), perc,False,color)

def gen_o(im, perc, color):
    offset = block_size + block_size/2 + pixel_size        
    generate_block(im,(offset,offset), perc,False,color)
    generate_block(im,(offset+block_size,offset), perc,False,color)
    generate_block(im,(offset,block_size+offset), perc,False,color)
    generate_block(im,(offset+block_size,offset+block_size), perc,False,color)

def gen_l(im, perc,color):
    offset = block_size + pixel_size
    offsety = offset + block_size
    generate_block(im,(offset,offsety), perc,True,color)
    generate_block(im,(offset+block_size,offsety), perc,True,color)
    generate_block(im,(offset+block_size*2,offsety), perc,True,color)
    generate_block(im,(offset,offsety+block_size), perc,True,color)    

def gen_j(im, perc,color):
    offset = block_size + pixel_size
    offsety = offset + block_size
    generate_block(im,(offset,offsety), perc,True,color)
    generate_block(im,(offset+block_size,offsety), perc,True,color)
    generate_block(im,(offset+block_size*2,offsety), perc,True,color)
    generate_block(im,(offset,offsety-block_size), perc,True,color)

def gen_z(im, perc,color):
    offset = block_size + pixel_size
    offsety = offset + block_size/2
    generate_block(im,(offset,offsety), perc,True,color)
    generate_block(im,(offset+block_size,offsety), perc,True,color)
    generate_block(im,(offset+block_size,offsety+block_size), perc,True,color)
    generate_block(im,(offset+block_size*2,offsety+block_size), perc,True,color)

def gen_s(im, perc,color):
    offset = block_size + pixel_size
    offsety = offset + block_size/2
    generate_block(im,(offset+block_size,offsety), perc,True,color)
    generate_block(im,(offset+block_size*2,offsety), perc,True,color)
    generate_block(im,(offset,offsety+block_size), perc,True,color)
    generate_block(im,(offset+block_size,offsety+block_size), perc,True,color)    
    
    
pieces = {'t': gen_t,
          'o': gen_o,
          'l': gen_l,
          'j': gen_j,
          'z': gen_z,
          's': gen_s}

            
def gen_image(perc, img_num, piece):
    img = Image.new('RGBA', (block_size*5+pixel_size,block_size*5+pixel_size), (0,255,0,0));
    im = ImageDraw.Draw(img)
    pieces[piece](im, perc,colors[piece])
    del im
    img = rotate(img,perc*360,(0,255,0,0))
    img.save(piece+"spin"+"{:02d}".format(img_num)+".png")
    
if __name__ == '__main__':   
    for i in range(64):
        gen_image(1/64*i,i,'o')
        gen_image(1/64*i,i,'t')
        gen_image(1/64*i,i,'l')
        gen_image(1/64*i,i,'j')
        gen_image(1/64*i,i,'s')
        gen_image(1/64*i,i,'z')
    
    

