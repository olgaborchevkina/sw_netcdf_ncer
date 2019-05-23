# -*- coding: utf-8 -*-
"""
NetCDF parser for air temperature by time with constant level, lat and long

@author: Danil Borchevkin
"""

import xarray as xr
import csv
import glob

def select_data_and_save(fin, fout, lat, long, level, needed_var):
    # Open dataset
    ds = xr.open_dataset(fin)
        
    # Check what we have needed data_var in own dataset. Otherwise - raise exception
    if needed_var not in ds.data_vars:
        print("Available data_vars in file")
        print(ds.data_vars)
        raise KeyError("Interested data var <{}> doesn't exist in dataset. Please check your main() function or file".format(needed_var))

    # Select air data by time with constant lat, long and level
    dsloc = ds.sel(lat=lat, lon=long, level=level)
    
    # Resample dataset to day mean values
    # Olga sy what we don't need resamlpe at this time
    #dsday = dsloc.resample("D", dim="time", how="mean")
    
    time = dsloc['time'].data
    needed_data = dsloc[needed_var].data

    # There is some tricky moment. If file is exist then data will append to file
    # Append data to file
    with open(fout, 'a') as file:
        dlm = "    "
        #csvWriter = csv.writer(csvfile, delimiter=";", lineterminator="\n")
        for i in range(len(time)):
            # When we use CSV we can't use delimeter with several chars
            # So in this case we use "bare-metal" write
            file.write(str(time[i]) + 
                       dlm + 
                       format(needed_data[i], ".3f") + 
                       dlm +
                       str(level) + 
                       dlm +
                       str(lat) +
                       dlm + 
                       str(long) +
                       "\n"
                       )

def get_out_file_name(output_path, lat, lon, level, data):
    result = ""

    result += str(lat)
    result += "_"
    result += str(lon)
    result += "_"
    result += str(level)
    result += "_"
    result += str(data)
    result += ".dat"

    return result

def process_all_files_in_folder(in_folder, out_folder, lat, lon, level, data):
    for file_path in glob.glob(in_folder + "/" + "*.nc"):
        out_file_path = out_folder + get_out_file_name(out_folder, lat, lon, level, data)
        print(" >>> Process file '{}' with output path '{}'".format(file_path, out_file_path))
        select_data_and_save(file_path, out_file_path, lat, lon, level, data)
        print("")
    
def main():
    #selectedPath = filedialog.askdirectory()
    
    # Change your parameters here
    input_folder = ".\\input\\"
    output_folder = ".\\output\\"
    lat = 55.0
    lon = 20.0
    level = 10
    data = 'hgt'

    process_all_files_in_folder(input_folder, output_folder, lat, lon, level, data)
    
if __name__=="__main__":
    main()
    
    