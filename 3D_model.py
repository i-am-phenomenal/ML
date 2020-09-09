# from skimage import transform
# from skimage.transform import warp, ProjectiveTransform
# import matplotlib.pyplot as plt
# import cv2
# import numpy as np

# img = cv2.imread('.top-down-image.jpeg')

# theta = np.deg2rad(20)
# tx = 0
# ty = 0

# S, C = np.sin(theta), np.cos(theta)

# # Rotation matrix, angle theta, translation tx, ty
# H = np.array([[C, -S, tx],
#               [S,  C, ty],
#               [0,  0, 1]])

# # Translation matrix to shift the image center to the origin
# r, c = img.shape
# T = np.array([[1, 0, -c / 2.],
#                [0, 1, -r / 2.],
#               [0, 0, 1]])

# # Skew, for perspective
# S = np.array([[1, 0, 0],
#               [0, 1.3, 0],
#               [0, 1e-3, 1]])

# trans = ProjectiveTransform(T)
# img_rot = warp(img, H)
# img_rot_center_skew = warp(img, S.dot(np.linalg.inv(T).dot(H).dot(T)))

# for i in [img, img_rot, img_rot_center_skew]:
#     f, ax = plt.subplots(figsize=(20,20))
#     ax.imshow(i, cmap=plt.cm.gray, interpolation='nearest')
#     plt.show()

