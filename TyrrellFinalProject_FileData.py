# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 16:18:23 2022

@author: Emma Tyrrell
"""
import arcpy
from arcpy.sa import *
import os 

print ("imported arcpy")

#define workspace and parameters
arcpy.env.workspace = "C:\\PennStateGIS\\GEOG485\\FINAL\\ProcessedPolygons"
arcpy.env.overwriteOutput = True

demFiles = arcpy.GetParameterAsText(0)
if demFiles == None or demFiles == '':
    demFiles = "C:\\PennStateGIS\\GEOG485\\FINAL\\GroupDEMFiles"

walk = arcpy.da.Walk(demFiles, topdown=True, datatype="RasterDataset")
sr = arcpy.SpatialReference(2232)

print (item for item in walk)

#for loop for getting path directories
for dirpath, dirnames, filenames in walk:
    
    for filename in filenames:
        print (filename)
        
        shapefile = f"avalanche_{filename[:-4]}_Polygons.shp"
      
        #run the slope tool on the DEM
        try: 
            outSlope = Slope(os.path.join(dirpath, filename), "DEGREE", "", "", "")
            
            print ("slope executed")
            
            #save outSlope
            outSlope.save((arcpy.env.workspace + "\\DEMslope"))
        
            print ("slope saved")
        
            print (arcpy.GetMessages())
        
            #reclassify , check to confirm value
            reclass_raster = Reclassify(outSlope, "Value", RemapRange([[0,30,"NODATA"], [30,40,1], [40,50,2], [50,60,3]]))
            print ("rasters reclassified")
        
            #convert polygons to rasters
            arcpy.conversion.RasterToPolygon(reclass_raster, shapefile)
            print (f"polygons {shapefile} created")
            
        except Exception as ex:  
            print (ex)