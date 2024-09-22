from PIL import Image, ImageDraw, ImageStat, ImageColor
import numpy as np
import time

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # file
    start_time = time.time()
    filename = "F:/marioRed.webp"
    img = Image.open(filename)
    image_matrix = np.array(img)

    #print(image_matrix)
    # params
    deg = 3  # resolution
    pixels = 36  # Num of leds
    offset: int = 0  # degree offset
    width = 5  # pixel width
    offsetWidth = 6  # offset between pixels

    # calculations
    sections = 360 / deg

    # init array

    # start file
    max_size = (pixels * 2) * (offsetWidth)
    print(max_size)
    print(img.size)
    img.show()
    img = img.resize((max_size, max_size), 0)
    print(img.size)

    # for line in image_matrix:
    #     for pixel in line:
    #         print(pixel)
    #img.save("F:/test/test.png")
    # mask arcs
    # mask = Image.new('RGBA', img.size, (0,0,0,0))
    # draw = ImageDraw.Draw(mask)
    target_color = 1
    inMask = Image.new('1', img.size, 0)
    inDraw = ImageDraw.Draw(inMask)
    halfWidth = img.width / 2
    halfHeight = img.height / 2
    # iteration for each pixel
    with open("F:/test/test.txt", "w") as file:
        for i in range(1, pixels + 1):
            curOffest = i * offsetWidth
            xyCor = (halfWidth - curOffest, halfHeight - curOffest), (halfWidth + curOffest, halfHeight + curOffest)
            for j in range(int(sections)):
                start_deg: int = j * deg
                end_deg = (j + 1) * deg - offset
                inDraw.rectangle(xyCor, 0)
                inDraw.arc(xyCor, start_deg, end_deg, 1, width)
                #inMask.save("F:/test/" + str(i) + "x" +str(j) + ".png")
                #inMask.show()
                image_matrix = np.array(inMask)
                # for line in image_matrix:
                #     print(line)
                coordinates = np.argwhere(image_matrix == True)
                file.write("(" + str(i) + "," + str(j) + ") = ")
                coord_strings = [f"[{coord[0]}, {coord[1]}]" for coord in coordinates]
                file.write(",".join(coord_strings) + "\n")
                #print(coordinates)
                #exit()


    # draw start image, result image and print 2d array
    img.show()

    # with open("C:/Users/Mari/Desktop/ESP32_POV_Display - Copy/ESP32_POV_Display - Copy/src/mario.h", "w") as file:
    #     # Write text to the file
    #     file.write("const uint32_t fontHEX[][36]={\n")
    #     for i, line in enumerate(array_2d):
    #         # formatted_columns = [f"{{{col}}}" for col in line]
    #         file.write("{")
    #         for j, col in enumerate(line):
    #             file.write(str(int(col, 16)))
    #             if j != len(line) - 1:
    #                 file.write(",")
    #
    #         if i != len(array_2d) - 1:
    #             file.write("},\n")
    #         else:
    #             file.write("}")
    #     file.write("\n};\n")
    #
    # with open("C:/Users/Mari/Desktop/ESP32_POV_Display - Copy/ESP32_POV_Display - Copy/src/mario.json", "w") as file:
    #     # Write text to the file
    #     file.write("{\"fontHEX\": [\n")
    #     for i, line in enumerate(array_2d):
    #         # formatted_columns = [f"{{{col}}}" for col in line]
    #         file.write("[")
    #         for j, col in enumerate(line):
    #             file.write(str(int(col, 16)))
    #             if j != len(line) - 1:
    #                 file.write(",")
    #
    #         if i != len(array_2d) - 1:
    #             file.write("],\n")
    #         else:
    #             file.write("]")
    #     file.write("]\n}\n")

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.6f} seconds")