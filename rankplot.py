import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
from matplotlib.colors import is_color_like


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),
                         ['', 'K', 'M', 'B', 'T'][magnitude])

def rankplot(    
    data, labels=None,
    y_labels=None, color=None, color_map=None, grey_color='grey',
    trim=True, show_vals=True, hspace=0, vspace=0, labelpad=0, 
    label_fontsize=5, tick_fontsize=6, 
    ax=None):
    """
    Args:
        data (`list` or `dict`): The ranking data. Can be a list of dicts with the label as key (`[{"John": 2, "Ali": 5}]`),
         a nested dictionary with the column label as key (`{'2010': {'John': 2, 'Ali': 2}}`) or a 2D array (`[[2, 5]]`).   
        labels (`list`, *optional*): 2D array in the same shape of the data, containing the labels. Mainly useful when the 
         input is a 2D array, otherwise labels are already extracted from the data. Defaults to None.
        y_labels (`list`, *optional*): Labels for the columns. Already extracted when the input is a nested 
         dictionary. Defaults to None.
        color (`list` or `str`, *optional*): The color(s) of the boxes. If one color is provided, all boxes 
         will get the same colors. If multiple colors are provided, the most frequent labels
          will be assigned a color. Defaults to None.
        color_map (`dict`, *optional*): Dictionary that allows for a custom mapping of labels to 
         specific colors. Overwrites the input of the color parameter. Defaults to None.
        grey_color (`str`, *optional*): Color for the labels that aren't included in color_map. Defaults to 'grey'.
        trim (`bool`, *optional*): Puts the last word of the label on a new line if the string if 
         wider than the box. Defaults to True.
        show_vals (`bool`, *optional*): Display the values in the box. Defaults to True.
        hspace (`int`, *optional*): Spacing between rows. Defaults to 0.
        vspace (`int`, *optional*): Spacing between columns. Defaults to 0.
        labelpad (`int`, *optional*): Spacing from the boxes to tick labels. Defaults to 0.
        label_fontsize (`int`, *optional*): Fontsize of the box labels. Defaults to 5.
        tick_fontsize (`int`, *optional*): Fontsize of the column labels. Defaults to 6.
        ax (*matplotlib axes object*, *optional*): An axes of the current figure. Defaults to None.

    Returns:
        _type_: Axes 
    """

    if ax is None:
        ax = plt.gca()
    fig = ax.figure 
    if isinstance(data, dict):
        if y_labels is None:
            y_labels = list(data.keys())
        data = list(data.values())
        labels = np.array([[item for item in row] for row in data])
        data = np.array([[row[item] for item in row] for row in data])
    elif isinstance(data[0], dict):
        labels = np.array([[item for item in row] for row in data])
        data = np.array([[row[item] for item in row] for row in data])
    else:
        data = np.array(data)
        if labels is not None:
            labels = np.array(labels)
        else:
            labels = np.zeros(data.shape, str)
    data_sorted = np.argsort(data)
    sorted_data = [row[data_sorted[i]][::-1] for i, row in enumerate(data)]
    sorted_labels = [row[data_sorted[i]][::-1] for i, row in enumerate(labels)]
    
    max_row_length = max(np.sum(sorted_data, axis=1))
    unique_labels = np.unique(np.concatenate(labels))

    
    if color is None:
        color = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
    if isinstance(color, (list, tuple, np.ndarray)):
        if len(color) == 1:
            if color_map is None:
                color_map = dict(zip(unique_labels, [color[0]] * len(unique_labels)))
        else:
            most_common_labels = [label for label, count in 
                              Counter(np.concatenate(labels)).most_common(len(color))]
            if color_map is None:
                color_map = dict(zip(most_common_labels, color))
    elif is_color_like(color):
        color_map = dict(zip(unique_labels, [color] * len(unique_labels)))

    width = int(max_row_length / len(sorted_data))
    labelpad = width / (20 - labelpad)
    
    fig_width, fig_height = ax.figure.get_figwidth(), ax.figure.get_figheight()
    aspect_ratio = fig_width / fig_height
    labelpad_horizontal = labelpad 
    labelpad_vertical = labelpad * aspect_ratio
    
    horizontal_spacing = width / (12 - hspace)

    if vspace >= 8:
        vspace = 7.9
    vertical_spacing = width / (8 - vspace)

    text_height = max_row_length
    n_plots = len(sorted_data)

    r = fig.canvas.get_renderer()
    rec_pos_x = 0 
    text_height = 0
    text_width = 0

    ax.set_ylim(0, max_row_length + vertical_spacing * len(sorted_data[0]))
    ax.set_xlim(0, (len(sorted_data) * width) + len(sorted_data) * horizontal_spacing)
    ax.invert_yaxis()

    for i, row in enumerate(sorted_data):
        rec_pos_y = 0 - vertical_spacing
        for item_idx, height in enumerate(row):
            corresponding_label = sorted_labels[i][item_idx]
            rectangle_color = color_map[corresponding_label] if corresponding_label in color_map else grey_color
            item_rec = plt.Rectangle((rec_pos_x, rec_pos_y + vertical_spacing), 
                                     width, height, color=rectangle_color)
            ax.add_patch(item_rec)

            if height > text_height + labelpad_vertical:
                text = ax.text(rec_pos_x + labelpad_horizontal, 
                               rec_pos_y + vertical_spacing + labelpad_vertical, 
                               corresponding_label, fontsize=label_fontsize, va='top',
                               color='white', weight='bold')
                bb = text.get_window_extent(renderer = fig.canvas.renderer)
                bb_datacoords = bb.transformed(ax.transData.inverted())
                text_height = bb_datacoords.height * -1
                text_width = bb_datacoords.width
                if height < text_height + labelpad_vertical:
                    text.set_visible(False)
                if trim:
                    if text_width + labelpad_horizontal * 2 > width:
                        label = corresponding_label.split()
                        if len(label) > 1:
                            label = ' '.join(label[:-1]) + '\n' + label[-1]
                            text.set_visible(False) 
                            text = ax.text(rec_pos_x + labelpad_horizontal, 
                                           rec_pos_y + vertical_spacing + labelpad_vertical, 
                                           label, fontsize=label_fontsize, va='top', color='white', weight='bold')
                            bb = text.get_window_extent(renderer = fig.canvas.renderer)
                            bb_datacoords = bb.transformed(ax.transData.inverted())
                            text_height = bb_datacoords.height * -1
                            text_width = bb_datacoords.width
            if height > text_height * 2 + labelpad_vertical * 2 and show_vals:
                if max_row_length > 10000:
                    number_label = human_format(height)
                else:
                    number_label = '{:,}'.format(height).replace(',', '.')
                ax.text(rec_pos_x + labelpad_horizontal, 
                        rec_pos_y + vertical_spacing + labelpad_vertical + text_height + labelpad_vertical ,
                       number_label,
                        fontsize=label_fontsize, va='top', color='white')
            rec_pos_y += height + vertical_spacing

        if y_labels:
            ax.text(rec_pos_x, -width / 7,  str(y_labels[i]), fontsize=tick_fontsize)
        rec_pos_x += width + horizontal_spacing
    ax.axis('off')
    return ax