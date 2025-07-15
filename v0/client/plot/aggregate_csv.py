import sys
import csv

def process_file(input_csv, output_csv):
    with open(input_csv, 'r') as f:
        reader = csv.reader(f)
        values = [float(row[1]) for row in reader if len(row) >= 2]
    
    if not values:
        print(f"No data found in {input_csv}")
        return
    
    average = sum(values) / len(values)
    
    with open(input_csv, 'r') as f:
        first_row = f.readline().strip().split(',')
        intended_gap = float(first_row[0]) if len(first_row) > 1 else 0.0
    
    with open(output_csv, 'a') as f:
        writer = csv.writer(f)
        writer.writerow([f"{intended_gap:.6f}", f"{average:.6f}"])
        
    print(f"Appended average of {input_csv} to {output_csv}")
    
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 aggregate_csv.py <input_csv> <output_csv>")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_csv = sys.argv[2]
    process_file(input_csv, output_csv)
