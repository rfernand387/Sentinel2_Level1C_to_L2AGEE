# Sentinel2_Level1C_to_GEE
Anaconda environment for Windows 10 and python script (should would across systems) to process Sentinel 2 Level 1C data to Level 2A and upload subset to GEE

This contains python based tools to process a downloaded Sentinel 2 Level 1C safe product to Level 2A safe product
and then also a Level 2A simple geotiff subset product that can be uploaded to Google Earth Engine.

Please cite: Fernandes, R.(2020) Sentinel 2 Level 1C to Level 2A Googe Earth Engine Upload.  Government of Canada. 
Restrictions: None.  

There are steps that should ideally be applied to a number of Level 1C scenes that share the same spatial subset.

1.  Prepare processor and directories

1.1 On a fast disk make a directories
./sen2cor  
  ../imports  
  ../working  
  ../exports  

1.2 Download Sen2Cor-02.08.00 or later from http://step.esa.int/main/third-party-plugins-2/sen2cor/sen2cor_v2-8/ and extract unzipped folder in the ./sen2cor directory
1.3 Download S2_L1C_to_L2AGEEbatch.py3
1.4 Download metadata.csv file in ./exports 
1.5 Start an Anaconda 3 terminal,  for the first time import the gdalCCRS environment,

(base) conda env create -f gdalCCRS.yml  

subsequently, activate the enviroment (it will be saved for next time) and bring up the jupyter notebook  

(base) activate gdalCCRS    
(gdalCCRS) 

1.6 Test that gdal and geeup are installed

(gdalCCRS)gdalinfo 

(gdalCCRS) geeup -h 

If they are not installed you will get errors.  In which case you have to resinatll them yourself (see https://github.com/samapriya/geeup) 

2. Download and process products to L2A GEE format

2.1 Download Level 1C files from ESA or USGS and place unzipped products in ./imports

2.2   Process each product using S2L1CTOL2AGEEbatch.py3 script

The code runs by processing all .SAFE files in import directorty

(gdalCCRS)python F:\sen2cor\Sentinel2_Level1C_to_GEE-master\S2L1CTOL2AGEEbatch.py3 -h 


(gdalCCRS) python F:\sen2cor\Sentinel2_Level1C_to_GEE-master\S2L1CTOL2AGEEbatch.py3 -i f:\sen2cor\import\ -w f:\sen2cor\working\ -e f:\sen2cor\export\ -s f:\sen2cor\ -N 45.4 -E -75.56 -r 0.16   


3.  Upload all products in exports to GEE.


(gdalCCRS) geeup init  
(gdalCCRS) C:\Users\rfern>geeup upload --source C:\Users\rfern\gdrive\s2msi\export -m  C:\Users\rfern\gdrive\s2msi\export\metadata.csv --nodata 0 --dest users/rfernand387/export --user rfernand387@gmail.com  

You should see a password prompt for your google account and then confirmation of uploads.  You can check if the asset shows up in GEE.  

Password:  
New collection users/rfernand387/export created  
Processing image 1 out of 2: C:\Users\rfern\gdrive\s2msi\export\S2B_MSIL2A_20180509T155859_N9999_R097_T18TVR_20200522T010435.tif  
Started upload task with ID: GCIITGCRB3QCAYRYZGML6I2Y  
Processing image 2 out of 2: C:\Users\rfern\gdrive\s2msi\export\S2B_MSIL2A_20181026T160339_N9999_R097_T18TVR_20200521T152513.tif  
Started upload task with ID: LJ4KU5QODQ6E6J5LX4JDKW4C  

4.  Delete files from import,working and export directories when no longer needed.
