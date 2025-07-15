import argparse
import matplotlib.pyplot as plt
import csv

def read_csv(filename):
    intended = []
    diff = []
    
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 2:
                continue
            try:
                intended.append(float(row[0]))
                diff.append(float(row[1]))
            except ValueError:
                continue
    
    return intended, diff

def main(filename1, filename2, png_file, title, x, y):
    intended1, diff1 = read_csv(filename1)
    intended2, diff2 = read_csv(filename2)
    
    plt.scatter(intended1, diff1, label='Python', color='blue', alpha=0.7)
    plt.scatter(intended2, diff2, label='C', color='red', alpha=0.7)
    
    plt.xlabel(x)
    plt.ylabel(y)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.savefig(png_file)
    
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot the graph of local gap between packets vs. the gap difference between packets received.")
    parser.add_argument('--csv1', type=str, help='CSV file to analyze')
    parser.add_argument('--csv2', type=str, help='CSV file to analyze')
    parser.add_argument('--png', type=str, help='PNG file to save')
    parser.add_argument('--title', type=str, help='Plot title')
    parser.add_argument('--x', type=str, help='x label')
    parser.add_argument('--y', type=str, help='y label')
    
    args = parser.parse_args()
    main(args.csv1, args.csv2, args.png, args.title, args.x, args.y)
    
# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
