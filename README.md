# Minimal ranking plot


### 1. Minimal example

```python
fig, ax = plt.subplots()
ax = rankplot(data, ax=ax)
ax.set_title('The most popular social media platforms', y=1.05)
```
![](examples/basic.png)

### Usage

```python
rankplot(data=None, labels=None,
    y_labels=None, color=None, color_map=None, grey_color='grey',
    trim=True, show_vals=True, hspace=0, vspace=0, labelpad=0, 
    label_fontsize=5, tick_fontsize=6, ax=None) 
```

#### Parameters

- *data* (`list` or `dict`): The ranking data. Can be a list of dicts with the label as key (`[{"John": 2, "Ali": 5}]`),
         a nested dictionary with the column label as key `{'2010': {'John': 2, 'Ali': 2}}` or a 2D array (`[[2, 5]]`). 
- `labels`
- `y_labels`
- `color`
- `color_map`
- `grey_color`
- `trim`
- `show_vals`
- `hspace`
- `vspace`
- `labelpad`
- `label_fontsize`
- `tick_fontsize`
- `ax`
