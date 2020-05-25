# Sentinel2_Level1C_to_GEE
Anaconda environment and jupyter notebook to process Sentinel 2 Level 1C data to Level 2A and Upload subset to GEE

This contains python based tools to process a downloaded Sentinel 2 Level 1C safe product to Level 2A safe product
and then also a Level 2A simple geotiff subset product that can be uploaded to Google Earth Engine.

There are steps that should ideally be applied to a number of Level 1C scenes that share the same spatial subset.

1.  Prepare processor and directories

On a fast disk make a directories
./sen2cor  
  ../imports  
  ../working  
  ../exports  

Download Sen2Cor-02.08.00 and extract unzipped folder in the ./sen2cor directory
Download S2_L1C_to_L2A.ipynb 
Download metadata.csv file in ./exports
Download Level 1C files from ESA or USGS and place unzipped products in ./imports

2.  For each product 

2.1 Start an Anaconda 3 terminal,  for the first time importthe gdalCCRS environment,

(base) conda env create -f gdalCCRS2.yml  

subsequently, activate the enviroment (it will be saved for next time) and bring up the jupyter notebook  

(base) activate gdalCCRS    
(gdalCCRS) jupyter lab    

The notebook environment will pop up in a web page.  

2.2  Open Navigate  S2_L1C_to_L2A.ipynb, edit the first box as required and run the notebook.  If you dont want to delet the L2A products from the working directory do not run the last box.

3.  Upload all products in exports to GEE.

2.1 Open anaconda and active gdalCCRS

2.2 Authenticate earth engine  

(gdalCCRS) earthengine authenticate  

web browser will pop up a page with google log in  

log in to account with earth engine access  

a web page with credentials will pop up   
e.g 4/0AHf8A9Y4gGTJM5bmn1JUlefTg7Poe9lRcn1CXwbOofNt1qG5xYwsdw  

copy and paste at prompt in anaconda terminal  

2.3 initialize geeup  and upload data

(gdalCCRS) geeup init  
(gdalCCRS) C:\Users\rfern>geeup upload --source C:\Users\rfern\gdrive\s2msi\export -m  C:\Users\rfern\gdrive\s2msi\export\metadata.csv --nodata 0 --dest users/rfernand387/export --user rfernand387@gmail.com  

You should see a password prompt for your google account and then confirmation of uploads.  You can check if the asset shows up in GEE.  

Password:  
New collection users/rfernand387/export created  
Processing image 1 out of 2: C:\Users\rfern\gdrive\s2msi\export\S2B_MSIL2A_20180509T155859_N9999_R097_T18TVR_20200522T010435.tif  
Started upload task with ID: GCIITGCRB3QCAYRYZGML6I2Y  
Processing image 2 out of 2: C:\Users\rfern\gdrive\s2msi\export\S2B_MSIL2A_20181026T160339_N9999_R097_T18TVR_20200521T152513.tif  
Started upload task with ID: LJ4KU5QODQ6E6J5LX4JDKW4C  
