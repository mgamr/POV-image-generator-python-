from PIL import Image, ImageDraw, ImageStat, ImageColor
import numpy as np
import time

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
    array_2d = [["" for _ in range(pixels)] for _ in range(int(sections))]
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
    resImg = Image.new('RGB', img.size, (0, 0, 0, 0))
    drawRes = ImageDraw.Draw(resImg)

    inMask = Image.new('1', img.size, 0)
    inDraw = ImageDraw.Draw(inMask)
    halfWidth = img.width / 2
    halfHeight = img.height / 2

    image_matrix = np.array(img)
    # iteration for each pixel
    for i in range(1, pixels + 1):
        curOffest = i * offsetWidth
        xyCor = (halfWidth - curOffest, halfHeight - curOffest), (halfWidth + curOffest, halfHeight + curOffest)
        for j in range(int(sections)):
            start_deg: int = j * deg
            end_deg = (j + 1) * deg - offset
            inDraw.rectangle(xyCor, 0)
            inDraw.arc(xyCor, start_deg, end_deg, 1, width)
            #inMask.show()
            image_mat = np.array(inMask)
            # for line in image_matrix:
            #     print(line)
            coordinates = np.argwhere(image_mat == 1)
            # print(coordinates)
            # for coord in coordinates:
            #     print(image_matrix[coord[0], coord[1]])
            #     print(image_mat[coord[0], coord[1]])
            stat = ImageStat.Stat(img, mask=inMask)
            # write in array
            average_color = (0, 0, 0)
            if sum(stat.count) >= 1:
                average_color = tuple(int(channel) for channel in stat.mean)
                #print(average_color)
                drawRes.arc(xyCor, start_deg, end_deg, average_color, width)
            #print(average_color)
            #print(average_color)
            av_color = (average_color[1], average_color[0], average_color[2])
            hex_color = '0x00{:02X}{:02X}{:02X}'.format(*av_color)
            array_2d[j][i - 1] = hex_color
            #print(str(i) + " " + str(j) + " " + str(av_color))
           # break
            #print(hex_color)

            #print(stat.count)
            #exit()

    # draw start image, result image and print 2d array
    img.show()
    resImg.show()

    with open("F:/test/test.h", "w") as file:
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

    with open("F:/test/test.json", "w") as file:
        # Write text to the file
        file.write("{\"fontHEX\": [\n")
        for i, line in enumerate(array_2d):
            # formatted_columns = [f"{{{col}}}" for col in line]
            file.write("[")
            for j, col in enumerate(line):
                file.write(str(int(col, 16)))
                if j != len(line) - 1:
                    file.write(",")

            if i != len(array_2d) - 1:
                file.write("],\n")
            else:
                file.write("]")
        file.write("]\n}\n")

    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Time taken: {elapsed_time:.6f} seconds")