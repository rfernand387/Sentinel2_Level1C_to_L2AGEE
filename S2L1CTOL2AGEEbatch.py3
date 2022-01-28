from optparse import OptionParser
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
from osgeo import gdal_array
from osgeo import gdalconst
import gdal
import ogr
import osr
import gdalnumeric
import gdalconst
import os
import glob
from shutil import rmtree
from shutil import copyfile
from pathlib import Path
import xml.etree.ElementTree as ET
from datetime import datetime
import csv


# determine directory size
def dirSize(dirName):
    root_directory = Path(dirName)
    size = sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    return(size)


# determine time between dateText and 1970,1,1,0,0,0 in milliseconds
def systemTime(dateText):
    date2 =  dateText;
    year = int(date2[0:4]);
    month = int(date2[5:7]);
    day = int(date2[8:10]);
    hour =  int(date2[11:13]);
    minute = int(date2[14:16]);
    second = int(date2[17:19]);
    systemTime= ((datetime(year,month,day,hour,minute,second)-datetime(1970,1,1,0,0,0))).total_seconds() * 1000.0
    return systemTime

# Add a metadata row to metadata.csv
def addMetadata(L2name,exportName,metadataName):
    #open the metadata files
    tree0= ET.parse(L2name[0]+'\MTD_MSIL2A.xml')
    root0= tree0.getroot()
    tree1= ET.parse(L2name[0]+'\\'+root0[0][0][11][0][0][0].text[0:42]+'\\MTD_TL.xml')
    root1= tree1.getroot()
    
    #parse the metadata files
    AOT_RETRIEVAL_ACCURACY= float(root0[3][3][14].text)
    CLOUDY_PIXEL_PERCENTAGE= float(root1[2][0][0].text)
    CLOUD_COVERAGE_ASSESSMENT= float(root0[3][0].text)
    CLOUDY_SHADOW_PERCENTAGE= float(root0[3][3][3].text)
    DARK_FEATURES_PERCENTAGE= float(root0[3][3][2].text)
    DATASTRIP_ID= root0[0][0][11][0][0].attrib
    DATASTRIP_ID= DATASTRIP_ID["datastripIdentifier"]
    DATATAKE_IDENTIFIER= root0[0][0][9].attrib
    DATATAKE_IDENTIFIER= DATATAKE_IDENTIFIER["datatakeIdentifier"]
    DATATAKE_TYPE= root0[0][0][9][1].text
    DEGRADED_MSI_DATA_PERCENTAGE= float(root1[2][0][1].text)
    FORMAT_CORRECTNESS= root0[3][2][0][0].text
    GENERAL_QUALITY= root0[3][2][0][1].text
    GENERATION_TIME= systemTime(root0[0][0][6].text)
    GEOMETRIC_QUALITY= root0[3][2][0][2].text
    GRANULE_ID= root0[0][0][11][0][0].attrib   
    GRANULE_ID= GRANULE_ID["granuleIdentifier"]
    HIGH_PROBA_CLOUDS_PERCENTAGE= float(root0[3][3][9].text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B1= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="0"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B2= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="3"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B3= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="4"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B4= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="5"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B5= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="6"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B6= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="7"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B7= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="8"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B8= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="9"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="10"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B9= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="11"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B10= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="12"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B11= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="1"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_AZIMUTH_ANGLE_B12= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="2"]/AZIMUTH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B1= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="0"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B2= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="3"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B3= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="4"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B4= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="5"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B5= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="6"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B6= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="7"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B7= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="8"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B8= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="9"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B8A= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="10"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B9= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="11"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B10= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="12"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B11= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="1"]/ZENITH_ANGLE').text)
    MEAN_INCIDENCE_ZENITH_ANGLE_B12= float(root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="2"]/ZENITH_ANGLE').text)
    MEAN_SOLAR_AZIMUTH_ANGLE= float(root1[1][1][1][1].text)
    MEAN_SOLAR_ZENITH_ANGLE= float(root1[1][1][1][0].text)
    MEDIUM_PROBA_CLOUDS_PERCENTAGE= float(root0[3][3][10].text)
    MGRS_TILE= root0[0][0][2].text
    MGRS_TILE= MGRS_TILE[39:44]
    NODATA_PIXEL_PERCENTAGE= float(root0[3][3][0].text)
    NOT_VEGETATED_PERCENTAGE= float(root0[3][3][5].text)
    PROCESSING_BASELINE= root0[0][0][5].text
    PRODUCT_ID= root0[0][0][2].text
    PRODUCT_ID= PRODUCT_ID[0:len(PRODUCT_ID)-5]
    RADIATIVE_TRANSFER_ACCURACY= float(root0[3][3][12].text)
    RADIOMETRIC_QUALITY= root0[3][2][0][3].text
    REFLECTANCE_CONVERSION_CORRECTION= root0[0][1][4][0].text
    SATURATED_DEFECTIVE_PIXEL_PERCENTAGE= float(root0[3][3][1].text)
    SENSING_ORBIT_DIRECTION= root0[0][0][9][4].text
    SENSING_ORBIT_NUMBER= float(root0[0][0][9][3].text)
    SENSOR_QUALITY= root0[3][2][0][4].text
    SOLAR_IRRADIANCE_B1= float(root0[0][1][4][1][0].text)
    SOLAR_IRRADIANCE_B2= float(root0[0][1][4][1][1].text)
    SOLAR_IRRADIANCE_B3= float(root0[0][1][4][1][2].text)
    SOLAR_IRRADIANCE_B4= float(root0[0][1][4][1][3].text)
    SOLAR_IRRADIANCE_B5= float(root0[0][1][4][1][4].text)
    SOLAR_IRRADIANCE_B6= float(root0[0][1][4][1][5].text)
    SOLAR_IRRADIANCE_B7= float(root0[0][1][4][1][6].text)
    SOLAR_IRRADIANCE_B8= float(root0[0][1][4][1][7].text)
    SOLAR_IRRADIANCE_B8A= float(root0[0][1][4][1][8].text)
    SOLAR_IRRADIANCE_B9= float(root0[0][1][4][1][9].text)
    SOLAR_IRRADIANCE_B10= float(root0[0][1][4][1][10].text)
    SOLAR_IRRADIANCE_B11= float(root0[0][1][4][1][11].text)
    SOLAR_IRRADIANCE_B12= float(root0[0][1][4][1][12].text)
    SNOW_ICE_PERCENTAGE= float(root0[3][3][11].text)
    SPACECRAFT_NAME= root0[0][0][9][0].text    
    THIN_CIRRUS_PERCENTAGE= float(root0[3][3][10].text)
    UNCLASSIFIED_PERCENTAGE= float(root0[3][3][7].text)
    VEGETATION_PERCENTAGE= float(root0[3][3][4].text)
    WATER_PERCENTAGE= float(root0[3][3][6].text)
    system_index= root0[0][0][2].text
    system_index= system_index[0:37]
    system_time_end= systemTime(root0[0][0][0].text)
    system_time_start= systemTime(root0[0][0][1].text)
    
    # fieldnames
    fieldnames = [        'id_no',         'AOT_RETRIEVAL_ACCURACY',         'CLOUDY_PIXEL_PERCENTAGE',         'CLOUD_COVERAGE_ASSESSMENT',         'CLOUDY_SHADOW_PERCENTAGE',         'DARK_FEATURES_PERCENTAGE',         'DATASTRIP_ID',         'DATATAKE_IDENTIFIER',         'DATATAKE_TYPE',         'DEGRADED_MSI_DATA_PERCENTAGE',         'FORMAT_CORRECTNESS',         'GENERAL_QUALITY',         'GENERATION_TIME',         'GEOMETRIC_QUALITY',         'GRANULE_ID',         'HIGH_PROBA_CLOUDS_PERCENTAGE',         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B1',         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B2',         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B3',         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B4',         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B5',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B6',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B7',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B9',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B10',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B11',        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B12',        'MEAN_INCIDENCE_ZENITH_ANGLE_B1',        'MEAN_INCIDENCE_ZENITH_ANGLE_B2',        'MEAN_INCIDENCE_ZENITH_ANGLE_B3',        'MEAN_INCIDENCE_ZENITH_ANGLE_B4',        'MEAN_INCIDENCE_ZENITH_ANGLE_B5',        'MEAN_INCIDENCE_ZENITH_ANGLE_B6',        'MEAN_INCIDENCE_ZENITH_ANGLE_B7',        'MEAN_INCIDENCE_ZENITH_ANGLE_B8',        'MEAN_INCIDENCE_ZENITH_ANGLE_B8A',        'MEAN_INCIDENCE_ZENITH_ANGLE_B9',        'MEAN_INCIDENCE_ZENITH_ANGLE_B10',        'MEAN_INCIDENCE_ZENITH_ANGLE_B11',        'MEAN_INCIDENCE_ZENITH_ANGLE_B12',        'MEAN_SOLAR_AZIMUTH_ANGLE',        'MEAN_SOLAR_ZENITH_ANGLE',        'MEDIUM_PROBA_CLOUDS_PERCENTAGE',        'MGRS_TILE',        'NODATA_PIXEL_PERCENTAGE',        'NOT_VEGETATED_PERCENTAGE',        'PROCESSING_BASELINE',        'PRODUCT_ID',        'RADIATIVE_TRANSFER_ACCURACY',        'RADIOMETRIC_QUALITY',        'REFLECTANCE_CONVERSION_CORRECTION',        'SATURATED_DEFECTIVE_PIXEL_PERCENTAGE',        'SENSING_ORBIT_DIRECTION',        'SENSING_ORBIT_NUMBER',        'SENSOR_QUALITY',        'SOLAR_IRRADIANCE_B1',        'SOLAR_IRRADIANCE_B2',        'SOLAR_IRRADIANCE_B3',        'SOLAR_IRRADIANCE_B4',        'SOLAR_IRRADIANCE_B5',        'SOLAR_IRRADIANCE_B6',        'SOLAR_IRRADIANCE_B7',        'SOLAR_IRRADIANCE_B8',        'SOLAR_IRRADIANCE_B8A',        'SOLAR_IRRADIANCE_B9',        'SOLAR_IRRADIANCE_B10',        'SOLAR_IRRADIANCE_B11',        'SOLAR_IRRADIANCE_B12',        'SNOW_ICE_PERCENTAGE',        'SPACECRAFT_NAME',        'THIN_CIRRUS_PERCENTAGE',        'UNCLASSIFIED_PERCENTAGE',        'VEGETATION_PERCENTAGE',        'WATER_PERCENTAGE',        'system:index',        'system:time_end',        'system:time_start']     
    
    #write a row of metadata
    with open(metadataName, 'a', newline='') as csvfile:  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({        'id_no':exportName,        'AOT_RETRIEVAL_ACCURACY':AOT_RETRIEVAL_ACCURACY,         'CLOUDY_PIXEL_PERCENTAGE':CLOUDY_PIXEL_PERCENTAGE,         'CLOUD_COVERAGE_ASSESSMENT':CLOUD_COVERAGE_ASSESSMENT,         'CLOUDY_SHADOW_PERCENTAGE':CLOUDY_SHADOW_PERCENTAGE,         'DARK_FEATURES_PERCENTAGE':DARK_FEATURES_PERCENTAGE,         'DATASTRIP_ID':DATASTRIP_ID,         'DATATAKE_IDENTIFIER':DATATAKE_IDENTIFIER,         'DATATAKE_TYPE':DATATAKE_TYPE,         'DEGRADED_MSI_DATA_PERCENTAGE':DEGRADED_MSI_DATA_PERCENTAGE,         'FORMAT_CORRECTNESS':FORMAT_CORRECTNESS,         'GENERAL_QUALITY':GENERAL_QUALITY,         'GENERATION_TIME':GENERATION_TIME,         'GEOMETRIC_QUALITY':GEOMETRIC_QUALITY,         'GRANULE_ID':GRANULE_ID,         'HIGH_PROBA_CLOUDS_PERCENTAGE':HIGH_PROBA_CLOUDS_PERCENTAGE,         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B1':MEAN_INCIDENCE_AZIMUTH_ANGLE_B1,         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B2':MEAN_INCIDENCE_AZIMUTH_ANGLE_B2,         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B3':MEAN_INCIDENCE_AZIMUTH_ANGLE_B3,         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B4':MEAN_INCIDENCE_AZIMUTH_ANGLE_B4,         'MEAN_INCIDENCE_AZIMUTH_ANGLE_B5':MEAN_INCIDENCE_AZIMUTH_ANGLE_B5,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B6':MEAN_INCIDENCE_AZIMUTH_ANGLE_B6,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B7':MEAN_INCIDENCE_AZIMUTH_ANGLE_B7,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8':MEAN_INCIDENCE_AZIMUTH_ANGLE_B8,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A':MEAN_INCIDENCE_AZIMUTH_ANGLE_B8A,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B9':MEAN_INCIDENCE_AZIMUTH_ANGLE_B9,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B10':MEAN_INCIDENCE_AZIMUTH_ANGLE_B10,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B11':MEAN_INCIDENCE_AZIMUTH_ANGLE_B11,        'MEAN_INCIDENCE_AZIMUTH_ANGLE_B12':MEAN_INCIDENCE_AZIMUTH_ANGLE_B12,        'MEAN_INCIDENCE_ZENITH_ANGLE_B1':MEAN_INCIDENCE_ZENITH_ANGLE_B1,        'MEAN_INCIDENCE_ZENITH_ANGLE_B2':MEAN_INCIDENCE_ZENITH_ANGLE_B2,        'MEAN_INCIDENCE_ZENITH_ANGLE_B3':MEAN_INCIDENCE_ZENITH_ANGLE_B3,        'MEAN_INCIDENCE_ZENITH_ANGLE_B4':MEAN_INCIDENCE_ZENITH_ANGLE_B4,        'MEAN_INCIDENCE_ZENITH_ANGLE_B5':MEAN_INCIDENCE_ZENITH_ANGLE_B5,        'MEAN_INCIDENCE_ZENITH_ANGLE_B6':MEAN_INCIDENCE_ZENITH_ANGLE_B6,        'MEAN_INCIDENCE_ZENITH_ANGLE_B7':MEAN_INCIDENCE_ZENITH_ANGLE_B7,        'MEAN_INCIDENCE_ZENITH_ANGLE_B8':MEAN_INCIDENCE_ZENITH_ANGLE_B8,        'MEAN_INCIDENCE_ZENITH_ANGLE_B8A':MEAN_INCIDENCE_ZENITH_ANGLE_B8A,        'MEAN_INCIDENCE_ZENITH_ANGLE_B9':MEAN_INCIDENCE_ZENITH_ANGLE_B9,        'MEAN_INCIDENCE_ZENITH_ANGLE_B10':MEAN_INCIDENCE_ZENITH_ANGLE_B10,        'MEAN_INCIDENCE_ZENITH_ANGLE_B11':MEAN_INCIDENCE_ZENITH_ANGLE_B11,        'MEAN_INCIDENCE_ZENITH_ANGLE_B12':MEAN_INCIDENCE_ZENITH_ANGLE_B12,        'MEAN_SOLAR_AZIMUTH_ANGLE':MEAN_SOLAR_AZIMUTH_ANGLE,        'MEAN_SOLAR_ZENITH_ANGLE':MEAN_SOLAR_ZENITH_ANGLE,        'MEDIUM_PROBA_CLOUDS_PERCENTAGE':MEDIUM_PROBA_CLOUDS_PERCENTAGE,        'MGRS_TILE':MGRS_TILE,        'NODATA_PIXEL_PERCENTAGE':NODATA_PIXEL_PERCENTAGE,        'NOT_VEGETATED_PERCENTAGE':NOT_VEGETATED_PERCENTAGE,        'PROCESSING_BASELINE':PROCESSING_BASELINE,        'PRODUCT_ID':PRODUCT_ID,        'RADIATIVE_TRANSFER_ACCURACY':RADIATIVE_TRANSFER_ACCURACY,        'RADIOMETRIC_QUALITY':RADIOMETRIC_QUALITY,        'REFLECTANCE_CONVERSION_CORRECTION':REFLECTANCE_CONVERSION_CORRECTION,        'SATURATED_DEFECTIVE_PIXEL_PERCENTAGE':SATURATED_DEFECTIVE_PIXEL_PERCENTAGE,        'SENSING_ORBIT_DIRECTION':SENSING_ORBIT_DIRECTION,        'SENSING_ORBIT_NUMBER':SENSING_ORBIT_NUMBER,        'SENSOR_QUALITY':SENSOR_QUALITY,        'SOLAR_IRRADIANCE_B1':SOLAR_IRRADIANCE_B1,        'SOLAR_IRRADIANCE_B2':SOLAR_IRRADIANCE_B2,        'SOLAR_IRRADIANCE_B3':SOLAR_IRRADIANCE_B3,        'SOLAR_IRRADIANCE_B4':SOLAR_IRRADIANCE_B4,        'SOLAR_IRRADIANCE_B5':SOLAR_IRRADIANCE_B5,        'SOLAR_IRRADIANCE_B6':SOLAR_IRRADIANCE_B6,        'SOLAR_IRRADIANCE_B7':SOLAR_IRRADIANCE_B7,        'SOLAR_IRRADIANCE_B8':SOLAR_IRRADIANCE_B8,        'SOLAR_IRRADIANCE_B8A':SOLAR_IRRADIANCE_B8A,        'SOLAR_IRRADIANCE_B9':SOLAR_IRRADIANCE_B9,        'SOLAR_IRRADIANCE_B10':SOLAR_IRRADIANCE_B10,        'SOLAR_IRRADIANCE_B11':SOLAR_IRRADIANCE_B11,        'SOLAR_IRRADIANCE_B12':SOLAR_IRRADIANCE_B12,        'SNOW_ICE_PERCENTAGE':SNOW_ICE_PERCENTAGE,        'SPACECRAFT_NAME':SPACECRAFT_NAME,        'THIN_CIRRUS_PERCENTAGE':THIN_CIRRUS_PERCENTAGE,        'UNCLASSIFIED_PERCENTAGE':UNCLASSIFIED_PERCENTAGE,        'VEGETATION_PERCENTAGE':VEGETATION_PERCENTAGE,        'WATER_PERCENTAGE':WATER_PERCENTAGE,           'system:index':system_index,        'system:time_end':system_time_end,        'system:time_start':system_time_start
                            })

def showMetadata(L2name,exportName,metadataName):
    #open the metadata files
    tree0= ET.parse(L2name[0]+'\MTD_MSIL2A.xml')
    root0= tree0.getroot()
    tree1= ET.parse(L2name[0]+'\\'+root0[0][0][11][0][0][0].text[0:42]+'\\MTD_TL.xml')
    root1= tree1.getroot();
    e1 = root1.find('.//Mean_Viewing_Incidence_Angle[@bandId="1"]/AZIMUTH_ANGLE').text
    #print(e1)

def getEPSG(L2name):
    tree0= ET.parse(L2name+'\MTD_MSIL2A.xml')
    root0 = tree0.getroot()
    tree1= ET.parse(L2name+'\\'+root0[0][0][11][0][0][0].text[0:42]+'\\MTD_TL.xml')
    root1= tree1.getroot()
    epsg= (root1.find('.//HORIZONTAL_CS_CODE').text)
    return(epsg)

def jp2tifBand(tifName,tifRes,bandName,bandRes,bandType,L2name,workDirname,rocWin):

    #get the dummy band depending on resolution and make a safe copy
    if bandRes == '10':
        dummyName = 'B04_10m'
    elif bandRes == '60':
        dummyName = 'B01_60m'
    else:
        dummyName = 'B05_20m'



    #print('Step 1 '+dummyName)
    #print(gdal.Info('SENTINEL2_L2A:'+L2name+'\MTD_MSIL2A.xml'+':'+bandRes+'m:EPSG_32618'))
    #wait = input("Press ENTER")

    if (bandName+'_'+bandRes+'m') != dummyName: 

        #copy the dummy file so we can later restore it
        dummyFile = next((glob.iglob(L2name+'\\**\\*_'+dummyName+'.jp2',recursive = True)))
        copyfile(dummyFile,workDirname+'temp.jp2')
        #print('step2 '+dummyFile)
        #print(workDirname+'temp.jp2')
        #wait = input("Press ENTER")

        #copy the target band over the dummy file
        targetFile = next((glob.iglob(L2name+'\\**\\*_'+bandName+'_'+bandRes+'m.jp2',recursive=True)))
        copyfile(targetFile,dummyFile)
        #print('step3 '+targetFile)
        #wait = input("Press ENTER")

    #export this file as a geotiff
    epsg = getEPSG(L2name)
    f = gdal.Open('SENTINEL2_L2A:'+L2name+'\MTD_MSIL2A.xml'+':'+bandRes+'m:'+epsg.replace(':','_'))
    gdal.Translate(workDirname+tifName+'.tif',f,bandList=[1],projWin = rocWin, projWinSRS = 'EPSG:4236', \
        xRes=tifRes,yRes=tifRes,outputType=bandType)
    f = None
    #print('step4 export '+workDirname+tifName+'.tif')
    #wait = input("Press ENTER")

    #restore the copied file
    if (bandName+'_'+bandRes+'m') != dummyName: 
        copyfile(workDirname+'temp.jp2',dummyFile)
        #print('step5 recopy')
        #wait = input('Press ENTER')

def main():
    #parse command line
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-i", "--iDir",type="string", dest="iDirname",
                      help="import directory path")
    parser.add_option("-w", "--wDir",type="string", dest="wDirname",
                      help="working directory path")
    parser.add_option("-e", "--eDir",type="string", dest="eDirname",
                      help="export directory path")
    parser.add_option("-s", "--sDir",type="string", dest="sDirname",
                      help="Sen2Cor directory path")
    parser.add_option("-N",type="float", dest="centerLat",
                      help="center latitude")
    parser.add_option("-E",type="float", dest="centerLon",
                      help="center longitude")
    parser.add_option("-r",type="float", dest="roiW",
                      help="region of interest width")
    parser.add_option("-v", "--verbose",action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",action="store_false", dest="verbose")
    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("incorrect number of arguments")
    if options.verbose:
        print("running")
    

    
    # define export window
    rocWin = [options.centerLon-options.roiW, options.centerLat+options.roiW, options.centerLon+options.roiW, options.centerLat-options.roiW]
    
    #iterate over all .SAFE directors in import directory
    for entry in os.scandir(options.iDirname):
        if (entry.path.endswith(".SAFE")):
            L1name = entry.name
            workDirname  = options.wDirname+L1name[0:len(L1name)-5]+'\\'
            L2path = workDirname+L1name[0:8]+'2A'+L1name[10:24]

            #make a work directory and run sen2cor and find the L2 product name
            os.mkdir(workDirname)
            cmd = options.sDirname  +  "\\L2A_Process.bat "+options.iDirname+L1name+" --output_dir "+workDirname+'\\'
            print(cmd)
            #os.system(cmd)
            L2name = glob.glob(workDirname+L1name[0:8]+'2A'+L1name[10:24]+'*.SAFE')


            # add a row to metadata file
            exportName = (L2name[0][len(workDirname):(len(L2name[0])-5)])
            addMetadata(L2name,exportName,options.eDirname+'metadata.csv')

            #Open and subset L2A data surface reflectance bands
            gdal.UseExceptions()    # Enable exceptions
            # determine projection
            epsg = getEPSG(L2name[0])
            f10m = gdal.Open('SENTINEL2_L2A:'+L2name[0]+'\MTD_MSIL2A.xml'+':10m:'+epsg.replace(':','_'))
            f20m = gdal.Open('SENTINEL2_L2A:'+L2name[0]+'\MTD_MSIL2A.xml'+':20m:'+epsg.replace(':','_'))
            f60m = gdal.Open('SENTINEL2_L2A:'+L2name[0]+'\MTD_MSIL2A.xml'+':60m:'+epsg.replace(':','_'))
            gdal.Translate(workDirname+'b1.tif',f60m,bandList=[1],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=60,yRes=60)
            gdal.Translate(workDirname+'b2.tif',f20m,bandList=[3],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=10,yRes=10)
            gdal.Translate(workDirname+'b3.tif',f10m,bandList=[2],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=10,yRes=10)
            gdal.Translate(workDirname+'b4.tif',f10m,bandList=[1],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=10,yRes=10)
            gdal.Translate(workDirname+'b5.tif',f20m,bandList=[1],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            gdal.Translate(workDirname+'b6.tif',f20m,bandList=[2],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            gdal.Translate(workDirname+'b7.tif',f20m,bandList=[3],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            gdal.Translate(workDirname+'b8.tif',f10m,bandList=[4],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=10,yRes=10)
            gdal.Translate(workDirname+'b8a.tif',f20m,bandList=[4],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            gdal.Translate(workDirname+'b9.tif',f60m,bandList=[2],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=60,yRes=60)
            gdal.Translate(workDirname+'b11.tif',f20m,bandList=[5],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            gdal.Translate(workDirname+'b12.tif',f20m,bandList=[6],projWin = rocWin, projWinSRS = 'EPSG:4236',xRes=20,yRes=20)
            band = f10m.GetRasterBand(1)
            print("Band Type={}".format(gdal.GetDataTypeName(band.DataType)))

            # close files
            f10m = None 
            f20m = None 
            f60m = None 

            #ancillary bands
#12: "AOT", unsigned int16, EPSG:32635, 10980x10980 px
#13: "WVP", unsigned int16, EPSG:32635, 10980x10980 px
#14: "SCL", unsigned int8, EPSG:32635, 5490x5490 px
#15: "TCI_R", unsigned int8, EPSG:32635, 10980x10980 px
#16: "TCI_G", unsigned int8, EPSG:32635, 10980x10980 px
#17: "TCI_B", unsigned int8, EPSG:32635, 10980x10980 px
#18: "QA10", unsigned int16, EPSG:32635, 10980x10980 px
#19: "QA20", unsigned int32, EPSG:32635, 5490x5490 px
#20: "QA60", unsigned int16, EPS

            jp2tifBand('AOT',10,'AOT','20',2,L2name[0],workDirname,rocWin)
            print('aot')
            jp2tifBand('WVP',10,'WVP','20',2,L2name[0],workDirname,rocWin) 
            print('wvp')
            jp2tifBand('SCL',20,'SCL','20',2,L2name[0],workDirname,rocWin)
            print('scl')
            jp2tifBand('TCI_R',10,'B04','10',2,L2name[0],workDirname,rocWin)
            print('tci_r')
            jp2tifBand('TCI_G',10,'B03','10',2,L2name[0],workDirname,rocWin)
            print('tci_g')
            jp2tifBand('TCI_B',10,'B02','10',2,L2name[0],workDirname,rocWin)
            print('tci_b') 
            jp2tifBand('QA10',10,'SCL','20',2,L2name[0],workDirname,rocWin)
            print('qa10')
            jp2tifBand('QA20',20,'SCL','20',2,L2name[0],workDirname,rocWin)
            print('qa20')
            jp2tifBand('QA60',60,'SCL','20',2,L2name[0],workDirname,rocWin)
            print('qa60')               
                   #copy the dummy file back

                # ancillary bands cant be accessed from the S2A driver so we copy them over reflectance bands and then translate
                # to ensure L2A product is not messed up permanently we copy them into temp files
                #path1 = os.scandir(options.iDirname)
                #print(path1.name)
                #shutil.copyfile('SENTINEL2_L2A:'+L2name[0]+'\GRANULE\*\IMG_DATA\10m\*B02*.JP2', 'SENTINEL2_L2A:'+L2name[0]+'\GRANULE\*\IMG_DATA\10m\*B02*.JP2'
            vrtOptions = gdal.BuildVRTOptions(separate=True)
            gdal.BuildVRT(workDirname+'merged.vrt',[workDirname+'b1.tif',workDirname+'b2.tif',workDirname+'b3.tif', \
                workDirname+'b4.tif', workDirname+'b5.tif',workDirname+'b6.tif',workDirname+'b7.tif', \
                workDirname+'b8.tif', workDirname+'b8a.tif',workDirname+'b9.tif',workDirname+'b11.tif', \
                workDirname+'b12.tif', workDirname+'AOT.tif',workDirname+'WVP.tif',workDirname+'SCL.tif', \
                workDirname+'TCI_R.tif',workDirname+'TCI_G.tif',workDirname+'TCI_B.tif', \
                workDirname+'QA10.tif',workDirname+'QA20.tif',workDirname+'QA60.tif'],options=vrtOptions)
            gdal.Translate(options.eDirname+exportName+'.tif',workDirname+'merged.vrt')
            gdal.Info(workDirname+'merged.vrt')


if __name__ == "__main__":
    main()
