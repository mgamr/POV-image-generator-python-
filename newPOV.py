from PIL import Image, ImageDraw, ImageStat, ImageColor
import numpy as np
import time
import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # file
    start_time = time.time()
    filename = "F:/marioRed.webp"
    img = Image.open(filename)


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
    array_2d = [['0' for _ in range(pixels)] for _ in range(int(sections))]
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
    resImg = Image.new('RGBA', img.size, (0, 0, 0, 0))
    drawRes = ImageDraw.Draw(resImg)

    inMask = Image.new('1', img.size, 0)
    inDraw = ImageDraw.Draw(inMask)
    halfWidth = img.width / 2
    halfHeight = img.height / 2
    image_matrix = np.array(img)
    with open("F:/test/test.txt", "r") as file:
        for line in file:
            if line:
                match_indices = re.search(r'\((\d+),(\d+)\)', line)

                # Use regex to find all coordinates in the format [x, y]
                matches_coords = re.findall(r'\[(\d+), (\d+)\]', line)

                # Extract the (i, j) indices if found
                if match_indices:
                    i, j = int(match_indices.group(1)), int(match_indices.group(2))
                    #print(f"Indices: ({i},{j})")
                    #print(matches_coords)
                    av_color = (0,0,0)
                    count =0
                    for coords in matches_coords:
                        pixel = image_matrix[int(coords[0])][int(coords[1])]
                        #print(pixel)
                        av_color += pixel
                        count = count+1
                    av_color_array = np.array(av_color)
                    if count > 0 :
                        av_color_array = av_color_array/count
                        #av_color_array = np.array(av_color)
                        av_color = tuple(int(channel) for channel in av_color_array)
                        #av_color = np.round(av_color).astype(int)
                        #print(av_color)
                        #av_color_array = np.array(av_color)
                        #print(av_color)
                        #print(av_color)
                        #print(av_color)
                        average_color = (av_color[1], av_color[0], av_color[2])
                        if j == 0:
                            print(str(i) + " " + str(j) + " " + str(average_color))
                        hex_color = '0x00{:02X}{:02X}{:02X}'.format(*average_color)
                        array_2d[j][i-1] = hex_color


                    #exit()
                    #print(average_color)
                    #exit()
                    #print(average_color)
                    #print(count)
                    #print(array_2d[i][j])
                    #print(int(array_2d[i][j],16))
                    #print("No indices found")


    with open("F:/test/testRes.h", "w") as file:
        # Write text to the file
        file.write("const uint32_t fontHEX[][36]={\n")
        for i, line in enumerate(array_2d):
            # formatted_columns = [f"{{{col}}}" for col in line]
            file.write("{")
            for j, col in enumerate(line):
                file.write(str(int(col, 16)))
                if j != len(line) - 1:
                    file.write(",")

            if i != len(array_2d) - 1:
                file.write("},\n")
            else:
                file.write("}")
        file.write("\n};\n")
    # iteration for each pixel
    # for i in range(1, pixels + 1):
    #     curOffest = i * offsetWidth
    #     xyCor = (halfWidth - curOffest, halfHeight - curOffest), (halfWidth + curOffest, halfHeight + curOffest)
    #     for j in range(int(sections)):
    #         start_deg: int = j * deg
    #         end_deg = (j + 1) * deg - offset
    #         inDraw.rectangle(xyCor, 0)
    #         inDraw.arc(xyCor, start_deg, end_deg, 1, width)
    #
    #         stat = ImageStat.Stat(img, mask=inMask)
    #         # write in array
    #         average_color = (0, 0, 0)
    #         if sum(stat.count) >= 1:
    #             average_color = tuple(int(channel) for channel in stat.mean)
    #             drawRes.arc(xyCor, start_deg, end_deg, average_color, width)
    #
    #         av_color = (average_color[1], average_color[0], average_color[2])
    #         hex_color = '0x00{:02X}{:02X}{:02X}'.format(*av_color)
    #         array_2d[j][i - 1] = hex_color

    # draw start image, result image and print 2d array
    #img.show()
    #resImg.show()

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