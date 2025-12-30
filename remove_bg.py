from PIL import Image
import sys

def remove_bg(input_path, output_path):
    img = Image.open(input_path)
    img = img.convert("RGBA")
    datas = img.getdata()
    
    newData = []
    
    # We assume the background is the "checkerboard"
    # A checkerboard is usually White (255,255,255) and Gray (something like 204,204,204 or similar)
    # But since it's a generated image, there might be compression artifacts or variations.
    
    # Let's try a different approach: Floodfill from corners is safer to avoid deleting internal whites/grays.
    # But PIL floodfill is not always available or behaves strictly.
    # Let's write a manual BFS floodfill for transparency.
    
    width, height = img.size
    pixels = img.load()
    
    # Identify "background" colors as whatever is at (0,0), (0,10), (10,0)? 
    # Or just assume the standard checkerboard colors.
    # Top left usually starts with one color.
    
    # Let's treat anything "near white" and "near gray" that touches the outside as transparent.
    
    queue = [(0, 0), (width-1, 0), (0, height-1), (width-1, height-1)]
    visited = set(queue)
    
    # Check edge pixels to seed the queue if they look like background
    for x in range(width):
        for y in [0, height-1]:
            if (x, y) not in visited:
                p = pixels[x,y]
                # Is it white-ish or gray-ish?
                # Check variance? 
                # Let's just assume if it's high brightness or specific gray.
                if sum(p[:3]) > 500: # White-ish (255+255+255 = 765)
                    queue.append((x,y))
                    visited.add((x,y))
                elif 150 < p[0] < 230 and abs(p[0]-p[1]) < 20 and abs(p[0]-p[2]) < 20: # Gray-ish
                    queue.append((x,y))
                    visited.add((x,y))

    for y in range(height):
        for x in [0, width-1]:
             if (x, y) not in visited:
                p = pixels[x,y]
                if sum(p[:3]) > 500:
                    queue.append((x,y))
                    visited.add((x,y))
                elif 150 < p[0] < 230 and abs(p[0]-p[1]) < 20 and abs(p[0]-p[2]) < 20:
                    queue.append((x,y))
                    visited.add((x,y))

    queue = list(set(queue))
    
    while queue:
        x, y = queue.pop(0)
        pixels[x, y] = (0, 0, 0, 0) # Make transparent
        
        for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
            if 0 <= nx < width and 0 <= ny < height:
                if (nx, ny) not in visited:
                    p = pixels[nx, ny]
                    # Check if neighbor is also background-like
                    is_bg = False
                    if sum(p[:3]) > 550: # White-ish
                        is_bg = True
                    elif 180 < p[0] < 225 and abs(p[0]-p[1]) < 15 and abs(p[0]-p[2]) < 15: # Gray-ish typical of checkerboard
                        is_bg = True
                    # Also catch dark gray if the user theme is dark? No, the checkerboard is usually light.
                    
                    if is_bg:
                        visited.add((nx, ny))
                        queue.append((nx, ny))

    img.save(output_path, "PNG")
    print("Done")

if __name__ == "__main__":
    if len(sys.argv) > 2:
        remove_bg(sys.argv[1], sys.argv[2])
