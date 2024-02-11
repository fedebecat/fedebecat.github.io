import os
import fitz 
import io 
from PIL import Image 
import numpy as np
import matplotlib.pyplot as plt
import cv2


folder_path = "assets/papers/"
pdf_files = [file for file in os.listdir(folder_path) if file.endswith(".pdf")]

def pix2np(pix):
    im = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
    im = np.ascontiguousarray(im[..., [2, 1, 0]])  # rgb to bgr
    return im

for file in pdf_files:
    # Process each PDF file here
    print(file)
    pdf_file = fitz.open(folder_path + file)
    page_imgs = []
    for page in pdf_file:  # iterate through the pages
        pix = page.get_pixmap()  # render page to an image
        im = pix2np(pix)
        page_imgs.append(im)
    pdf_file.close()

    if page_imgs[0].shape != page_imgs[1].shape:
        # if the first two pages are not the same size, assume the first page is the cover
        # and the second page is the first page of the paper
        # so remove the first page
        page_imgs.pop(0)

    # define a white page
    white_page = np.ones(page_imgs[0].shape, dtype=np.uint8) * 255
    for i in range(8):
        page_imgs.append(white_page)

    # preallocate the full image
    full_img = np.ones((int(page_imgs[0].shape[0] * 2), int(page_imgs[0].shape[1] * 4), 3), dtype=np.uint8)*255

    # double the size of the first page
    first_big = cv2.resize(page_imgs[0], (page_imgs[0].shape[1] * 2, page_imgs[0].shape[0] * 2))

    full_img[:, :first_big.shape[1]] = first_big

    # concatenate the first 3 pages horizontally
    first_row = np.concatenate(page_imgs[1:3], axis=1)
    full_img[:first_row.shape[0], first_big.shape[1]:first_big.shape[1]+first_row.shape[1]] = first_row

    #if len(page_imgs)>=4:
    # concatenate the next 3 pages horizontally
    second_row = np.concatenate(page_imgs[3:5], axis=1)
    full_img[first_row.shape[0]:, first_big.shape[1]:first_big.shape[1]+second_row.shape[1]] = second_row

    # resize full image to have height of 400
    new_height = 400
    scale = new_height / full_img.shape[0]
    full_img = cv2.resize(full_img, (0, 0), fx=scale, fy=scale)

    # save image
    cv2.imwrite('assets/paper_imgs/' + file.replace(".pdf", ".png"), full_img)
    #plt.imshow(full_img)
    #plt.show()

    deb = 1

    