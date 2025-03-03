import numpy as np
import matplotlib.pyplot as plt

draw_config = {
    "figsize": (5, 5),
    "xlim": (-1, 1),
    "ylim": (-1, 1),
    "txt_color": "red",
    "fontsize": 8,
    "floor_color": "black",
    "line_style": "--"
}

# def draw_from_config(x_list,y_list):
#     plt.figure(figsize=(5,5))
#     plt.xlim(-1, 1)
#     plt.ylim(-1, 1)
#     plt.plot(x_list, y_list)
#
#     for i, label in enumerate(labels):
#         if i < len(labels):
#             plt.text(x_list[i], y_list[i], label, fontsize=8, ha='right', va='bottom', color='red')
#     plt.show()