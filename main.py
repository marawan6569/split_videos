import numpy as np
import cv2
from time import sleep


def draw_rect_and_take_photo(e, x, y, flags, params):
    window = params['window']
    image = params['img']
    p_w = 100
    p_h = 100

    if e == cv2.EVENT_MOUSEMOVE:
        cv2.rectangle(image, (x-p_w, y-p_h), (x+p_w, y+p_h), (0, 255, 0), 2)
        cv2.imshow(window, image)

    elif e == cv2.EVENT_LBUTTONDOWN:
        if x - p_w <= 0:
            x_start = 0
        else:
            x_start = x - p_w

        if x + p_w >= width:
            x_end = x + (width - x)
        else:
            x_end = x + p_w

        if y - p_h <= 0:
            y_start = 0
        else:
            y_start = y - p_h

        if y + p_h >= height:
            y_end = y + (height-y)
        else:
            y_end = y + p_h

        photo = image[y_start: y_end, x_start: x_end]
        cv2.imshow('photo', photo)


cap = cv2.VideoCapture(0)
while cap.isOpened():
    _, img = cap.read()

    if _:
        height, width, channels = img.shape
        part1 = img[0:height, 0: int(width/2)]
        part2 = img[0:height, int(width/2): int(width)]

        # cv2.imshow('original', img)
        cv2.imshow('part1', part1)
        cv2.imshow('part2', part2)

        # cv2.setMouseCallback('original', draw_rect_and_take_photo, {'window': 'original', 'img': img})
        cv2.setMouseCallback('part1', draw_rect_and_take_photo, {'window': 'part1', 'img': part1})
        cv2.setMouseCallback('part2', draw_rect_and_take_photo, {'window': 'part2', 'img': part2})

    k = cv2.waitKey(1)
    if k == 27:
        break
    elif k == 32:
        while True:
            k = cv2.waitKey(1)
            if k == 27:
                break
            elif k == 32:
                break
            # cv2.imshow('original', img)
            cv2.imshow('part1', part1)
            cv2.imshow('part2', part2)

    sleep(.05)
