import argparse
import csv
import pandas as pd
import numpy as np

def append_to_csv(filename, intended_gap, value):
    with open(filename, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([intended_gap, value])

def main():
    parser = argparse.ArgumentParser(description="Analyze gap deviation from CSV files.")
    parser.add_argument('csv_files', nargs='+', help="Paths to CSV files.")
    parser.add_argument('--mean', type=str, required=True, help="Path for mean CSV file.")
    parser.add_argument('--median', type=str, required=True, help="Path for median CSV file.")
    parser.add_argument('--iqr', type=str, required=True, help="Path for IQR CSV file.")
    parser.add_argument('--intended', type=float, required=True, help="Intended Gap")

    args = parser.parse_args()

    # csv_files = ['trial1.csv', 'trial2.csv', 'trial3.csv']

    all_data = pd.concat([pd.read_csv(f, header=None) for f in args.csv_files], ignore_index=True)

    all_data.columns = ['intended_gap', 'gap_diff']

    mean_gap = all_data['gap_diff'].mean()
    median_gap = all_data['gap_diff'].median()
    iqr_gap = np.percentile(all_data['gap_diff'], 75) - np.percentile(all_data['gap_diff'], 25)

    print(f"Mean (actual - intended) gap: {mean_gap:.2f} µs")
    print(f"Median (actual - intended) gap: {median_gap:.2f} µs")
    print(f"IQR (actual - intended) gap: {iqr_gap:.2f} µs")

    args.intended = args.intended * 1_000_000
    
    append_to_csv(args.mean, args.intended, mean_gap)
    append_to_csv(args.median, args.intended, median_gap)
    append_to_csv(args.iqr, args.intended, iqr_gap)

if __name__ == '__main__':
    main()

# vim: set sts=4 sw=4 ts=8 expandtab ft=python:
