import pandas as pd
import random
import time
import os
import numpy as np

# Function to generate random numbers in specified ranges
def generate_random_numbers():
    random_negative_15_to_25 = random.randint(-25, -15)
    random_0_to_3 = random.randint(0, 3)
    return random_negative_15_to_25, random_0_to_3

def generate_random_numbers1():
    random_negative_15_to_25_1 = random.randint(-25, -15)
    random_0_to_3_1 = random.randint(0, 3)
    return random_negative_15_to_25_1, random_0_to_3_1



# Function to modify the TSV file
def modify_tsv_file(main_filename):
    # Read the main TSV file to get its structure
    df = pd.read_csv(main_filename, sep='\t')
    random_numbers_for_mean = np.random.normal(loc=-22, scale=1, size=1000)
    random_numbers_for_std_dev = np.random.normal(loc=1.5, scale=.75, size=1000)
    mean = np.mean(random_numbers_for_mean)
    std_dev=np.mean(random_numbers_for_std_dev)

    random_numbers_for_mean1 = np.random.normal(loc=-22, scale=1, size=1000)
    random_numbers_for_std_dev1 = np.random.normal(loc=1.5, scale=.75, size=1000)
    mean1=np.mean(random_numbers_for_mean1)
    std_dev1=np.mean(random_numbers_for_std_dev1)


    # Generate random numbers for modification
    #random_num1, random_num2 = generate_random_numbers()
    #random_num1= random.randint(-25,-15)
    #random_num2= random.randint(0,3)
    #random_num3= random.randint(-25,-15)
    #random_num4=random.randint(0,3)
    #random_num3, random_num4 = generate_random_numbers1()
    #For a normal distribution of numbers
    random_num1= mean
    random_num2= std_dev
    random_num3= mean1
    random_num4= std_dev1


    # Modify the specified rows and columns
    df.iloc[9, 2] = random_num1
    df.iloc[10, 2] = random_num2
    df.iloc[11, 2] = random_num3
    df.iloc[12, 2] = random_num4

    return df

# Specify the location of the 'data' folder
data_folder_path = r'C:\Users\Sebma\OneDrive\Desktop\Raw_Data'

# Create the 'data' directory if it doesn't exist
if not os.path.exists(data_folder_path):
    os.makedirs(data_folder_path)

# Path to the main TSV file
main_tsv_file = r'C:\Users\Sebma\OneDrive\Desktop\spill_001855691_Acnet.tsv'

# Counter to keep track of generated TSV files
num_generated_files = 0

# Main loop to generate and save modified TSV files every 10 seconds
while num_generated_files < 10:
    # Generate and save modified TSV files
    modified_df = modify_tsv_file(main_tsv_file)
    modified_filename = os.path.join(data_folder_path, f'modified_file_{num_generated_files + 1}.tsv')
    modified_df.to_csv(modified_filename, sep='\t', index=False)
    print(f"Generated and saved {modified_filename}")
    
    num_generated_files += 1
    time.sleep(10)

print("Generated 10 TSV files. Exiting the script.")
