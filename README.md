# Minimal ranking plot


## Usage

```python
def rankplot(    
    data=None, labels=None,
    y_labels=None, color=None, color_map=None, grey_color='grey',
    trim=True, show_vals=True, hspace=0, vspace=0, labelpad=0, 
    label_fontsize=5, tick_fontsize=6, ax=None) 
```

#### Parameters

### 1. Minimal example

```python
fig, ax = plt.subplots()
ax = rankplot(data, ax=ax)
ax.set_title('The most popular social media platforms', y=1.05)
```
![](examples/basic.png)
