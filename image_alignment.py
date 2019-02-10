#!/usr/bin/env python
# Python 3
import random
import cv2 as cv


def random_rotation_matrix(max_amount_deg, center_point):
    return cv.getRotationMatrix2D(center_point, random.uniform(-1 * max_amount_deg, max_amount_deg), 1)


def random_scale(original_size, max_amount):
    scale_amount = 1.0 + random.uniform(-1 * max_amount, max_amount)

    return int(round(original_size[0] * scale_amount)), int(round(original_size[1] * scale_amount))


if __name__ == '__main__':
    source_filename = "pcb.jpeg"
    max_rotation_deg = 30
    max_scale_factor = .25

    raw_image = cv.imread(source_filename)

    resized_image = cv.resize(raw_image, random_scale((raw_image.shape[1], raw_image.shape[0]), max_scale_factor),
                              interpolation=cv.INTER_LINEAR)
    resized_center = (resized_image.shape[0] // 2, resized_image.shape[1] // 2)

    # Rotating and warping an image require plenty of padding to ensure we don't clip useful parts in the process.
    # Using BORDER_REPLICATE means there are no sudden transitions in the background. That will help with finding
    # the true PCB corners later.
    padded_image = cv.copyMakeBorder(resized_image, resized_center[0], resized_center[0], resized_center[1], resized_center[1],
                                     borderType=cv.BORDER_REPLICATE)

    rows, columns, channels = padded_image.shape
    padded_center = (columns // 2, rows // 2)

    modified_image = cv.warpAffine(padded_image, random_rotation_matrix(max_rotation_deg, padded_center), (columns, rows),
                                  borderMode=cv.BORDER_REPLICATE)

    while True:
        k = cv.waitKey(1)
        if k == 'q' or k == 27 or k == 'Q' or k == 1048603 or k == 1048689:
            break
        cv.imshow("modified", modified_image)
