from PIL import ImageGrab

def is_bar_almost_full(region, threshold=80):

    screenshot = ImageGrab.grab(bbox=region)

    rgb_im = screenshot.convert('RGB')

    green_pixels = 0
    total_pixels = 0

    for y in range(rgb_im.size[1]):
        for x in range(rgb_im.size[0]):
            total_pixels += 1
            r, g, b = rgb_im.getpixel((x, y))

            if g > r and g > b and g > 100:  
                green_pixels += 1

    green_percentage = (green_pixels / total_pixels) * 100

    return green_percentage >= threshold

region = (832, 1026, 1304, 1035)
if is_bar_almost_full(region):
    print("POD is at least 80% FULL.")
else:
    print("POD is less than 80% FULL.")