import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

python_files = [
    ['../../server/python/100/trial1.csv', '../../server/python/100/trial2.csv', '../../server/python/100/trial3.csv'],
    ['../../server/python/150/trial1.csv', '../../server/python/150/trial2.csv', '../../server/python/150/trial3.csv'],
    ['../../server/python/200/trial1.csv', '../../server/python/200/trial2.csv', '../../server/python/200/trial3.csv'],
    ['../../server/python/250/trial1.csv', '../../server/python/250/trial2.csv', '../../server/python/250/trial3.csv'],
    ['../../server/python/300/trial1.csv', '../../server/python/300/trial2.csv', '../../server/python/300/trial3.csv'],
    ['../../server/python/350/trial1.csv', '../../server/python/350/trial2.csv', '../../server/python/350/trial3.csv'],
    ['../../server/python/400/trial1.csv', '../../server/python/400/trial2.csv', '../../server/python/400/trial3.csv'],
    ['../../server/python/450/trial1.csv', '../../server/python/450/trial2.csv', '../../server/python/450/trial3.csv'],
    ['../../server/python/500/trial1.csv', '../../server/python/500/trial2.csv', '../../server/python/500/trial3.csv'],
    ['../../server/python/550/trial1.csv', '../../server/python/550/trial2.csv', '../../server/python/550/trial3.csv'],
    ['../../server/python/600/trial1.csv', '../../server/python/600/trial2.csv', '../../server/python/600/trial3.csv'],
    ['../../server/python/650/trial1.csv', '../../server/python/650/trial2.csv', '../../server/python/650/trial3.csv'],
    ['../../server/python/700/trial1.csv', '../../server/python/700/trial2.csv', '../../server/python/700/trial3.csv'],
    ['../../server/python/750/trial1.csv', '../../server/python/750/trial2.csv', '../../server/python/750/trial3.csv'],
    ['../../server/python/800/trial1.csv', '../../server/python/800/trial2.csv', '../../server/python/800/trial3.csv'],
    ['../../server/python/850/trial1.csv', '../../server/python/850/trial2.csv', '../../server/python/850/trial3.csv'],
    ['../../server/python/900/trial1.csv', '../../server/python/900/trial2.csv', '../../server/python/900/trial3.csv'],
    ['../../server/python/950/trial1.csv', '../../server/python/950/trial2.csv', '../../server/python/950/trial3.csv'],
    ['../../server/python/1000/trial1.csv', '../../server/python/1000/trial2.csv', '../../server/python/1000/trial3.csv'],
]

c_files = [
    ['../../server/c#/100/trial1.csv', '../../server/c#/100/trial2.csv', '../../server/c#/100/trial3.csv'],
    ['../../server/c#/150/trial1.csv', '../../server/c#/150/trial2.csv', '../../server/c#/150/trial3.csv'],
    ['../../server/c#/200/trial1.csv', '../../server/c#/200/trial2.csv', '../../server/c#/200/trial3.csv'],
    ['../../server/c#/250/trial1.csv', '../../server/c#/250/trial2.csv', '../../server/c#/250/trial3.csv'],
    ['../../server/c#/300/trial1.csv', '../../server/c#/300/trial2.csv', '../../server/c#/300/trial3.csv'],
    ['../../server/c#/350/trial1.csv', '../../server/c#/350/trial2.csv', '../../server/c#/350/trial3.csv'],
    ['../../server/c#/400/trial1.csv', '../../server/c#/400/trial2.csv', '../../server/c#/400/trial3.csv'],
    ['../../server/c#/450/trial1.csv', '../../server/c#/450/trial2.csv', '../../server/c#/450/trial3.csv'],
    ['../../server/c#/500/trial1.csv', '../../server/c#/500/trial2.csv', '../../server/c#/500/trial3.csv'],
    ['../../server/c#/550/trial1.csv', '../../server/c#/550/trial2.csv', '../../server/c#/550/trial3.csv'],
    ['../../server/c#/600/trial1.csv', '../../server/c#/600/trial2.csv', '../../server/c#/600/trial3.csv'],
    ['../../server/c#/650/trial1.csv', '../../server/c#/650/trial2.csv', '../../server/c#/650/trial3.csv'],
    ['../../server/c#/700/trial1.csv', '../../server/c#/700/trial2.csv', '../../server/c#/700/trial3.csv'],
    ['../../server/c#/750/trial1.csv', '../../server/c#/750/trial2.csv', '../../server/c#/750/trial3.csv'],
    ['../../server/c#/800/trial1.csv', '../../server/c#/800/trial2.csv', '../../server/c#/800/trial3.csv'],
    ['../../server/c#/850/trial1.csv', '../../server/c#/850/trial2.csv', '../../server/c#/850/trial3.csv'],
    ['../../server/c#/900/trial1.csv', '../../server/c#/900/trial2.csv', '../../server/c#/900/trial3.csv'],
    ['../../server/c#/950/trial1.csv', '../../server/c#/950/trial2.csv', '../../server/c#/950/trial3.csv'],
    ['../../server/c#/1000/trial1.csv', '../../server/c#/1000/trial2.csv', '../../server/c#/1000/trial3.csv'],



]

def load_gap_data(file_list):
    dfs = []
    for file in file_list:
        df = pd.read_csv(file, header=None, names=["INTENDED GAP", "GAP DIFFERENCE"])
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

def prepare_boxplot_data(files_by_gap):
    data = []
    gap_labels = []
    for file_list in files_by_gap:
        df = load_gap_data(file_list)
        data.append(df['GAP DIFFERENCE'].values)
        gap_labels.append(str(df["INTENDED GAP"].iloc[0]))
    return data, gap_labels

def plot_boxplots(py_files_by_gap, c_files_by_gap, output_png):
    py_data, gap_labels = prepare_boxplot_data(py_files_by_gap)
    c_data, _ = prepare_boxplot_data(c_files_by_gap)

    n = len(gap_labels)
    ind = np.arange(n)  # the x locations for the groups

    width = 0.35  # width of each boxplot

    plt.figure(figsize=(16, 8))

    # Plot Python boxplots (shifted left)
    bp_py = plt.boxplot(py_data, positions=ind - width/2, widths=width, patch_artist=True, boxprops=dict(facecolor="skyblue"))
    # Plot C boxplots (shifted right)
    bp_c = plt.boxplot(c_data, positions=ind + width/2, widths=width, patch_artist=True, boxprops=dict(facecolor="lightgreen"))

    plt.xticks(ind, gap_labels, rotation=45, ha='right')
    plt.ylabel('Gap Difference')
    plt.title('Gap Difference Distribution by Gap Setting: Python vs C')
    plt.grid(axis='y')

    # Create custom legend
    import matplotlib.patches as mpatches
    py_patch = mpatches.Patch(color='skyblue', label='Python')
    c_patch = mpatches.Patch(color='lightgreen', label='C')
    plt.legend(handles=[py_patch, c_patch])

    plt.tight_layout()
    plt.savefig(output_png, dpi=300)
    plt.close()
    print(f"Box plot saved as '{output_png}'")

plot_boxplots(python_files, c_files, "comparison_plot.png")
