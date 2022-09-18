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

- `data` (list or dict): Data for the ranking. 
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
