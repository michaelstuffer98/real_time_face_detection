import os

def image_dir_generator(path):
    for f in os.listdir(path):
        image_path = os.path.join(path, f)
        if os.path.isfile(image_path):
            yield image_path

def pad(box, padding, width, height):
    # apply padding
    (x, y, w, h) = box
    x = max(0, x-padding)
    y = max(0, y-padding)
    w = min(width, x+w+padding)-x
    h = min(height, y+h+padding)-y
    return (x, y, w, h)

# Fancy output for progress, integer in range 0 to 1 
def print_progress(progress: float):
    progress = int(progress * 10)
    print(" > ", progress*"##", (10-progress)*"  ", "||", progress * 10.0, " %", end='\r')
