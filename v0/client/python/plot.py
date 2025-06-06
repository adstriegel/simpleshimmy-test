import matplotlib.pyplot as plt
import csv
import argparse

def plot(csv_file):
    x = []
    y = []
    
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            x.append(float(row[0]))
            y.append(float(row[1]))
    
    plt.figure(figsize=(10,5))
    plt.plot(x, y, marker='o', linestyle='-')
    plt.title("Theoretic vs Actual Gap Between Packets")
    plt.xlabel("Theoretic gap between packets")
    plt.ylabel("Actual gap between packets")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plot.png")
    plt.show()
        
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot the graph of local gap between packets vs. average gap between packets received.")
    parser.add_argument('--csv', type=str, help='CSV file to analyze')
    
    args = parser.parse_args()
    plot(args.csv)
