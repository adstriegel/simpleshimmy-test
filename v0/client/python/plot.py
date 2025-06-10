import matplotlib.pyplot as plt
import csv
import argparse

def plot(csv_file, png_file, plot_title, x_label, y_label):
    x = []
    y = []
    
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    
    plt.figure(figsize=(10,5))
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title(plot_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(png_file)
    plt.show()
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot the graph of local gap between packets vs. average gap between packets received.")
    parser.add_argument('--csv', type=str, help='CSV file to analyze')
    parser.add_argument('--png', type=str, help='PNG file to save')
    parser.add_argument('--title', type=str, help='Plot title')
    parser.add_argument('--x', type=str, help='x label')
    parser.add_argument('--y', type=str, help='y label')
    
    args = parser.parse_args()
    plot(args.csv, args.png, args.title, args.x, args.y)
