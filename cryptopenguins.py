from ctypes import resize
from turtle import pen
import cv2
import numpy as np

def fetchParts (base, back, beak, eyes, shad, sign, text) -> list:
    penguin = []

    p_base = cv2.imread(f'./penguin/back/{base}.png', cv2.IMREAD_UNCHANGED)
    p_base = cv2.cvtColor(p_base, cv2.COLOR_BGR2RGB)
    penguin.append(p_base)

    p_back = cv2.imread(f'./penguin/back/{back}.png', cv2.IMREAD_UNCHANGED)
    p_back = cv2.cvtColor(p_back, cv2.COLOR_BGR2RGB)
    penguin.append(p_back)

    p_beak = cv2.imread(f'./penguin/beak/{beak}.png', cv2.IMREAD_UNCHANGED)
    p_beak = cv2.cvtColor(p_back, cv2.COLOR_BGR2RGB)
    penguin.append(p_beak)

    p_eyes = cv2.imread(f'./penguin/eyes/{eyes}.png', cv2.IMREAD_UNCHANGED)
    p_eyes = cv2.cvtColor(p_eyes, cv2.COLOR_BGR2RGB)
    penguin.append(p_eyes)

    p_shad = cv2.imread(f'./penguin/shad/{shad}.png', cv2.IMREAD_UNCHANGED)
    p_shad = cv2.cvtColor(p_shad, cv2.COLOR_BGR2RGB)
    penguin.append(p_shad)

    p_sign = cv2.imread(f'./penguin/sign/{sign}.png', cv2.IMREAD_UNCHANGED)
    p_sign = cv2.cvtColor(p_sign, cv2.COLOR_BGR2RGB)
    penguin.append(p_sign)

    p_text = cv2.imread(f'./penguin/sign/{text}.png', cv2.IMREAD_UNCHANGED)
    p_text = cv2.cvtColor(p_text, cv2.COLOR_BGR2RGB)
    penguin.append(p_text)

    return penguin

# def recolorPart (part, color):
#     for i in part:
#         for j in i:
#             if j[0] == 255 and j[1] == 255 and j[2] == 255:
#                 continue
#             else: j = color

pen_parts = fetchParts(0, 0, 0, 0, 0, 0, 0)
# recolorPart (pen_parts[0], [220, 0, 0])

penguin = np.zeros(shape=[100, 80, 4], dtype=np.uint8)
for parts in pen_parts:
    penguin += parts

height, width = penguin.shape[0], penguin.shape[1]
new_height = int(height*4)
new_width = int(width*4)

resized = cv2.resize(penguin, (new_width, new_height), interpolation = cv2.INTER_AREA)

cv2.imshow('pengu', resized)
cv2.cv2.waitKey(0)