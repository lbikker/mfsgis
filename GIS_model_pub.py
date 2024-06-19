### ONLY NEEDED IF INPUT LAYERS NEED TO BE CREATED

# Required only when there are SubModel(s)
import sys 
sys.path.append(r"C:\Users\lieke\AppData\Local\Temp\ArcGISProTemp22228")
# -*- coding: utf-8 -*-

import os
import arcpy
from arcpy.sa import *
from arcpy.sa import ZonalStatistics

# Check out any necessary licenses.
arcpy.CheckOutExtension("spatial")
arcpy.CheckOutExtension("ImageAnalyst")
arcpy.ImportToolbox(r"c:\program files\arcgis\pro\Resources\ArcToolbox\toolboxes\Data Management Tools.tbx")

# To allow overwriting outputs change overwriteOutput option to True.
arcpy.env.overwriteOutput = True


## Data input (change to personal path)

#Geographical scope ( Marineregions.org - see article for source)
arch_input = "C:\\Users\\lieke\\Documents\\Marine_areas_CSV\\World_Archipelagic_Waters_v3_20191118\\eez_archipelagic_waters_v3.shp"
ter_input = "C:\\Users\\lieke\\Documents\\Marine_areas_CSV\\World_12NM_v3_20191118_gpkg\\eez_12nm_v3.gpkg\\main.eez_12nm_v3"
int_input = "C:\\Users\\lieke\\Documents\\Marine_areas_CSV\\World_Internal_Waters_v3_20191118_gpkg\\eez_internal_waters_v3.gpkg\\main.eez_internal_waters_v3"

# Bathymetry (GEBCO - see article for source)
wd_input_1 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n0.0_s-90.0_w0.0_e90.0.tif")
wd_input_2 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n0.0_s-90.0_w-90.0_e0.0.tif")
wd_input_3 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n0.0_s-90.0_w90.0_e180.0.tif")
wd_input_4 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n0.0_s-90.0_w-180.0_e-90.0.tif")
wd_input_5 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n90.0_s0.0_w0.0_e90.0.tif")
wd_input_6 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n90.0_s0.0_w-90.0_e0.0.tif")
wd_input_7 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n90.0_s0.0_w90.0_e180.0.tif")
wd_input_8 = arcpy.Raster("C:\\Users\\lieke\\Documents\\GEBCO_global\\gebco_2023_sub_ice_n90.0_s0.0_w-180.0_e-90.0.tif")

# Wave energy (Sayre et al. (2021) / Esri Living Atlas - see article for source)
ECU_input = "https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/Ecological_Coastal_Units__ECU__1km_Segments/FeatureServer/0"

# Wind speed (GWA - see article for source)
windspeed_input = arcpy.Raster("C:\\Users\\lieke\\Documents\\wind\\gwa3_250_windspeed_10m.tif")

#Hs100 (Takbash et al. (2019) - see article for source)
Hs_100_input = arcpy.Raster("C:\\Users\\lieke\\OneDrive\\Documenten\\MATLAB\\Hs_100_young.tif")

#U100 (Takbash et al. (2019) - see article for source)
U10_100_input = arcpy.Raster("C:\\Users\\lieke\\OneDrive\\Documenten\\MATLAB\\U10_100_young.tif")

# Shipping density (World Bank Data - see article for source)
ship_dens_input = arcpy.Raster("C:\\Users\\lieke\\Documents\\shipping routes\\shipdensity_commercial_\\ShipDensity_Commercial1.tif")

# Marine protected areas (Esri Living Atlas)
wdpa_mar_input = "https://services5.arcgis.com/Mj0hjvkNtV7NRhA7/arcgis/rest/services/WDPA_v4/FeatureServer/1"

# Coastal city (United Nations (2018) - see article for source)
cities_input = "C:\\Users\\lieke\\Documents\\growth rate\\WUP2018-F14-Growth_Rate_Cities.xls\\ArcGIS_data$"


## GIS MODEL - PREPROCESSING

# Geographical scope

def prep_scope():  # Define model for preprocessing geographical scope

    # Process: Project 
    arch_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\arch_project"
    arcpy.management.Project(in_dataset=arch_input, out_dataset=arch_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")

    # Process: Project  
    terri_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\ter_project"
    arcpy.management.Project(in_dataset=ter_input, out_dataset=terri_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")

    # Process: Project
    int_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\int_project"
    arcpy.management.Project(in_dataset=int_input, out_dataset=int_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]")

    # Process: Merge 
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    arcpy.management.Merge(inputs=[arch_project, terri_project, int_project], output=waters_shp, field_mappings="MRGID \"MRGID\" true true false 20 Double 0 20,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,MRGID,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,MRGID,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,MRGID,-1,-1;GEONAME \"GEONAME\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,GEONAME,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,GEONAME,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,GEONAME,0,80;POL_TYPE \"POL_TYPE\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,POL_TYPE,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,POL_TYPE,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,POL_TYPE,0,80;MRGID_TER1 \"MRGID_TER1\" true true false 20 Double 0 20,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,MRGID_TER1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,MRGID_TER1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,MRGID_TER1,-1,-1;TERRITORY1 \"TERRITORY1\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,TERRITORY1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,TERRITORY1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,TERRITORY1,0,80;MRGID_SOV1 \"MRGID_SOV1\" true true false 20 Double 0 20,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,MRGID_SOV1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,MRGID_SOV1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,MRGID_SOV1,-1,-1;SOVEREIGN1 \"SOVEREIGN1\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,SOVEREIGN1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,SOVEREIGN1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,SOVEREIGN1,0,80;ISO_TER1 \"ISO_TER1\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,ISO_TER1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,ISO_TER1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,ISO_TER1,0,80;X_1 \"X_1\" true true false 32 Double 5 31,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,X_1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,X_1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,X_1,-1,-1;Y_1 \"Y_1\" true true false 32 Double 5 31,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,Y_1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,Y_1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,Y_1,-1,-1;MRGID_EEZ \"MRGID_EEZ\" true true false 20 Double 0 20,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,MRGID_EEZ,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,MRGID_EEZ,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,MRGID_EEZ,-1,-1;AREA_KM2 \"AREA_KM2\" true true false 20 Double 0 20,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,AREA_KM2,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,AREA_KM2,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,AREA_KM2,-1,-1;ISO_SOV1 \"ISO_SOV1\" true true false 80 Text 0 0,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,ISO_SOV1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,ISO_SOV1,0,80,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,ISO_SOV1,0,80;UN_SOV1 \"UN_SOV1\" true true false 11 Double 0 11,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,UN_SOV1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,UN_SOV1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,UN_SOV1,-1,-1;UN_TER1 \"UN_TER1\" true true false 11 Double 0 11,First,#,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\arch_water,UN_TER1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\ter_water,UN_TER1,-1,-1,C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\project_files\\int_water,UN_TER1,-1,-1")


#-----------------------------------------------------------------------------------------SLS----------------------------------------------------------------------------------------------------------

# Bathymetry
def prep_bathymetry():   # Define function for preprocessing bathymetry layer

    wd_split_folder = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_split"
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    final_input_layers_folder = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers"
    
    list_min = []
    list_max = []
    
    for i in range(1,9):
        # Process: Project Raster 
        wd_project = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_project\\wd_project_{i}"
        arcpy.management.ProjectRaster(in_raster=locals()["wd_input_" + str(i)], out_raster=wd_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", resampling_type="BILINEAR")
        wd_project = arcpy.Raster(wd_project)
        
        # Process: Split Raster 
        wd_split_name = f"GB_{i}"
        wd_split = arcpy.management.SplitRaster(in_raster=wd_project, out_folder=wd_split_folder, out_base_name=wd_split_name, split_method="NUMBER_OF_TILES", format="TIFF", resampling_type="BILINEAR", num_rasters="4 4")[0]
        
        # Loop through all split files; try- except built in for files not within spatial extent
        for j in range(0,16):
            try:
                # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters 
                # Define extent parameter
                rasterfile = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_split\\GB_{i}{j}.TIF"
                e = arcpy.Describe(rasterfile)
                extent = e.extent
                
                wd_extract = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_extract\\wd_extr_{i}{j}"
                Extract_by_Mask = wd_extract
                with arcpy.EnvManager(snapRaster=f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_split\\GB_{i}{j}.TIF"):
                    wd_extract = arcpy.sa.ExtractByMask(rasterfile, waters_shp, "INSIDE", extent)
                    
                    # Check if raster is not empty: calculate statistics
                    arcpy.management.CalculateStatistics(wd_extract)
                    max_pixel_value = wd_extract.maximum
                    print(f"Maximale pixelwaarde: {max_pixel_value}")
                
                    # Check if the raster is not empty: check for maximum pixel value
                    if max_pixel_value is not None:                
                        wd_extract.save(Extract_by_Mask)
                            
                        # Process: Aggregate: aggregate for correct resolution preserving maximum value in pixel
                        wd_max= f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_ag\\max\\wd_max_{i}{j}"
                        Aggregate = wd_max
                        wd_max = arcpy.sa.Aggregate(wd_extract, 3, "MAXIMUM", "EXPAND", "NODATA")
                        wd_max.save(Aggregate)
                        list_max.append(wd_max)
                
                        # Process: Aggregate: aggregate for correct resolution, preserving minimum value in pixel 
                        wd_min = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_ag\\min\\wd_min_{i}{j}"
                        Aggregate = wd_min
                        wd_min = arcpy.sa.Aggregate(wd_extract, 3, "MINIMUM", "EXPAND", "NODATA")
                        wd_min.save(Aggregate)
                        list_min.append(wd_min)
    
                        # Process: Raster to Point: prepare for wave energy layer
                        wd_rp = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\wave_energy\\raster_point\\wd_rp_{i}{j}.shp"
                        arcpy.conversion.RasterToPoint(in_raster=wd_min, out_point_features=wd_rp)
                    else:
                        print(f"{i}{j} empty raster")
                        pass
                     
            except:
                print(f"{i}{j} outside extent")
                pass      

    # Process: Mosaic To New Raster: mosaic all split rasters to one global raster
    wd_max_total = arcpy.management.MosaicToNewRaster(input_rasters= list_max, output_location=final_input_layers_folder, raster_dataset_name_with_extension="wd_max", number_of_bands=1)[0]
    wd_max_total = arcpy.Raster(wd_max_total)
    
    # Process: Extract by Mask:
    ex_we = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wd_max"
    Extract_by_Mask = ex_we
    ex_we = arcpy.sa.ExtractByMask(wd_max_total, waters, "INSIDE", "-180 -56.725289742 179.99895834582 83.87428964035 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    ex_we.save(Extract_by_Mask)

    # Process: Mosaic To New Raster: mosaic all split rasters to one global raster
    wd_min_total = arcpy.management.MosaicToNewRaster(input_rasters= list_min, output_location=final_input_layers_folder, raster_dataset_name_with_extension="wd_min", number_of_bands=1)[0]
    wd_min_total = arcpy.Raster(wd_min_total)
    
    # Process: Extract by Mask:
    ex_we = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wd_min"
    Extract_by_Mask = ex_we
    ex_we = arcpy.sa.ExtractByMask(wd_min_total, waters, "INSIDE", "-180 -56.725289742 179.99895834582 83.87428964035 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    ex_we.save(Extract_by_Mask)

# Wave energy

def prep_wave_energy(): # Define function for preprocessing wave energy layer
    
    we_list = []
    final_input_layers_folder = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers"
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    
    # Loop through all split files; try- except built in for not existing files
    for i in range (7,8):
        for j in range (0,16):
            try:
                # Process: Spatial Join: join ECU attributes to points
                wd_rp =  f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\wave_energy\\raster_point\\wd_rp_{i}{j}.shp"
                ecu_sj = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\wave_energy\\sj\\ecu_sj_{i}{j}.shp"
                arcpy.analysis.SpatialJoin(target_features=wd_rp, join_features=ECU_input, out_feature_class=ecu_sj, field_mapping="", match_option="CLOSEST", search_radius="10 DecimalDegrees")
            
                # Process: Point to Raster: convert point file to raster file with correct resolution
                wd_min = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\bathymetry\\wd_ag\\min\\wd_min_{i}{j}"
                we_pr = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\wave_energy\\wave_energy\\point_raster\\we_{i}{j}_pr"
                arcpy.conversion.PointToRaster(in_features=ecu_sj, value_field="wave_label", out_rasterdataset=we_pr, cellsize=wd_min)
                
                # Process: Reclassify: reclassify the wave energy strings to numbers
                rc_ecu = f"C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\wave_energy\\rc_we_pr_{i}{j}"
                Reclassify = rc_ecu
                rc_ecu = arcpy.sa.Reclassify(we_pr, "WAVE_LABEL", "'quiescent' 0;'very low wave energy' 1;'low wave energy' 2;'moderate wave energy' 3;'moderately high wave energy' 4;'high wave energy' 5;'very high wave energy' 6", "NODATA")
                rc_ecu.save(Reclassify)
                we_list.append(rc_ecu)
                
            except:
                print(f"{i}{j} no file")
                pass

    # Process: Mosaic To New Raster: mosaic all split rasters to one global raster 
    we = arcpy.management.MosaicToNewRaster(input_rasters=we_list, output_location=final_input_layers_folder, raster_dataset_name_with_extension="we", coordinate_system_for_the_raster="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", number_of_bands=1)[0]
    we = arcpy.Raster(we)
    
    # Process: Extract by Mask:
    ex_we = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\we"
    Extract_by_Mask = ex_we
    ex_we = arcpy.sa.ExtractByMask(we, waters, "INSIDE", "-180 -56.725289742 179.99895834582 83.87428964035 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    ex_we.save(Extract_by_Mask)



# Wind speed

def prep_windspeed():  # Define function for preprocessing wind speed layer

    windspeed_input = arcpy.Raster("C:\\Users\\lieke\\Documents\\wind\\gwa3_250_windspeed_10m.tif")
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    
    # Process: Project Raster
    ws_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\windspeed\\ws_project"
    arcpy.management.ProjectRaster(in_raster=windspeed_input, out_raster=ws_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", resampling_type="BILINEAR")
    ws_project = arcpy.Raster(ws_project)
    print('project done')
    
    # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters 
    ws_ex = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\windspeed\\ws_ex"
    Extract_by_Mask = ws_ex
    with arcpy.EnvManager(snapRaster=windspeed_input):
        ws_ex = arcpy.sa.ExtractByMask(ws_project, waters_shp, "INTERSECT", "-180 -56.725289742 180 81.5107687477372 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
        ws_ex.save(Extract_by_Mask)
        print('extract done')

    # Process: Aggregate: aggregate for correct resolution, preserving maximum value in pixel 
    ws = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws"
    Aggregate = ws
    ws = arcpy.sa.Aggregate(ws_ex, 5, "MAXIMUM", "EXPAND", "DATA")
    ws.save(Aggregate)
    print('aggregate done')

#-----------------------------------------------------------------------------------------ULS----------------------------------------------------------------------------------------------------------

# HS100

def prep_hs100():     # Define function for preprocessing hs100 layer
    
    ws = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws")
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
   
    # Process: Raster Calculator: set nodata values to NoData 
    hs100_sn = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\hs100\\hs100_sn"
    result = Hs_100_input*1
    Hs_100_input.save(hs100_sn)
    
    # Process: Raster Calculator: extrapolate for gaps at coast 
    hs100_ex = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\hs100\\hs100_ex"
    outFocalStat = Con(IsNull(hs100_sn), FocalStatistics(hs100_sn, NbrRectangle(3,3, "CELL"), "MEAN"), hs100_sn)
    outFocalStat.save(hs100_ex)

    # Process: Project Raster 
    hs100_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\hs100\\hs100_project"
    arcpy.management.ProjectRaster(in_raster=hs100_ex, out_raster=hs100_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", vertical="NO_VERTICAL")
    hs100_project = arcpy.Raster(hs100_project)
    
    
    # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters, with correct resolution  
    hs100 = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\hs100"
    Extract_by_Mask = hs100
    with arcpy.EnvManager(cellSize=ws):
        hs100 = arcpy.sa.ExtractByMask(hs100_project, waters_shp, "INSIDE", "-180 -56.725289742 180 81.5107687477372 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
        hs100.save(Extract_by_Mask)
    

# U100

def prep_u100():        # Define function for preprocessing u100 layer
    
    ws = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws")
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    
    # Process: Raster Calculator: set nodata values to NoData
    u100_sn = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\u100\\u100_sn"
    result = U10_100_input*1
    U10_100_input.save(u100_sn)
    
    # Process: Raster Calculator: extrapolate for gaps at coast 
    u100_ex = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\u100\\u100_ex"
    outFocalStat = Con(IsNull(u100_sn), FocalStatistics(u100_sn, NbrRectangle(3,3, "CELL"), "MEAN"), u100_sn)
    outFocalStat.save(u100_ex)

    # Process: Project Raster 
    u100_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\u100\\u100_project"
    arcpy.management.ProjectRaster(in_raster=u100_ex, out_raster=u100_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", vertical="NO_VERTICAL")
    u100_project = arcpy.Raster(u100_project)
    
    
    # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters, with correct resolution 
    u100 = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\u100"
    Extract_by_Mask = u100
    with arcpy.EnvManager(cellSize=ws):
        u100 = arcpy.sa.ExtractByMask(u100_project, waters_shp, "INSIDE", "-180 -56.725289742 180 81.5107687477372 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
        u100.save(Extract_by_Mask)

#-----------------------------------------------------------------------------------------OCEAN PLANNING----------------------------------------------------------------------------------------------------------

# Ship density

def prep_ship_density():     # Define function for preprocessing ship density layer

    ws = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws")
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"
    
    # Process: Project Raster
    ship_project = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\shipping\\ship_project"
    arcpy.management.ProjectRaster(in_raster=ship_dens_input, out_raster=ship_project, out_coor_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]", cell_size="0,0125 0,0125")
    ship_project = arcpy.Raster(ship_project)
    
    # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters
    ship_dens = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ship_dens"
    Extract_by_Mask_2_ = ship_dens
    ship_dens = arcpy.sa.ExtractByMask(ship_project, waters_shp, "INSIDE", "-180 -56.725289742 180 81.5107687477372 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    ship_dens.save(Extract_by_Mask_2_)

# Marine protected areas

def prep_marine_protected_areas():# Define function for preprocessing marine protected areas layer
    
    ws = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws")    
    
    # Process: Extract by Mask: spatial extent to territorial, internal and argipelagic waters
    wdpa_ex = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\protected_areas\\wdpa_ex"
    Extract_by_Mask = wdpa_ex
    wdpa_ex = arcpy.sa.ExtractByMask(ws, wdpa_mar_input, "INSIDE", "-179.999988540844 -56.739752108935 179.999988540844 83.8852478910649 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    wdpa_ex.save(Extract_by_Mask)
    print("extract by mask done")
    
    # Raster Calculator: set all cells representing marine protected areas to 0
    wdpa = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wdpa"
    result = Con(wdpa_ex >= 0, 0)
    result.save(wdpa)

#------------------------------------------------------------------------------------------MOTIVATION----------------------------------------------------------------------------------------------------------

def prep_cities(): # Define function for preprocessing cities layer
    
    waters_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\scope_waters\\waters.shp"

    # Process: XY Table To Point: load table into ArcGIS pro
    cities_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\cities\\cities.shp"
    arcpy.management.XYTableToPoint(in_table=cities_input, out_feature_class=cities_shp, x_field="Longitude", y_field="Latitude", coordinate_system="GEOGCS[\"GCS_WGS_1984\",DATUM[\"D_WGS_1984\",SPHEROID[\"WGS_1984\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision")
    print("load done")
    
    # Process: Pairwise Buffer: create buffer of 15 km from shoreline 
    coast_15km = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\cities\\coast_15km"
    arcpy.analysis.PairwiseBuffer(in_features=waters_shp, out_feature_class=coast_15km, buffer_distance_or_field="15 Kilometers", dissolve_option="ALL", method="PLANAR", max_deviation="0 DecimalDegrees")
    print("buffer done")
    
    # Process: Pairwise Clip: clip cities to 15 km buffer for coastal cities selection
    cities_coast_shp = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\cities\\cities_coast.shp"
    arcpy.analysis.PairwiseClip(in_features=cities_shp, clip_features=coast_15km, out_feature_class=cities_coast_shp)

    # Process: Pairwise Buffer: create buffer with radius 35 km around city centre
    prox_cities = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\prox_cities"
    arcpy.analysis.PairwiseBuffer(in_features=cities_coast_shp, out_feature_class=prox_cities, buffer_distance_or_field="35 Kilometers", method="GEODESIC")
    print("prep cities done")

if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\scratch_workspace", workspace="C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\MFS.gdb"):
#         prep_scope()
#         prep_bathymetry()
#         prep_windspeed()
#         prep_wave_energy()
#         prep_hurricane()
#         prep_hs100()
#         prep_u100()
#         prep_ship_density()
#         prep_marine_protected_areas()
#         prep_cities()


        

## GIS MODEL - TECHNICAL POTENTIAL AND MOTIVATION

# Required only when there are SubModel(s)
import sys 
sys.path.append(r"C:\Users\lieke\AppData\Local\Temp\ArcGISProTemp22228")
# -*- coding: utf-8 -*-

import os
import arcpy
from arcpy.sa import *

# Check out any necessary licenses.
arcpy.CheckOutExtension("spatial")

    
# To allow overwriting outputs change overwriteOutput option to True.
arcpy.env.overwriteOutput = True

## Set boundaries for bathymetry, wind speed, wave energy, 100-year return significant waveheight, 100-year return wind speed.

# Bathymetry (m)
bd_wd_min = "-2500" 
bd_wd_max = "-15"

# Wind speed (m/s)
bd_ws = "9" #m/s

# Wave energy (yes (1) / no (0))
bd_we_quiescent = "1"
bd_we_verylow = "1" 
bd_we_low = "1" 
bd_we_moderate = "1" 
bd_we_moderatelyhigh = "0" 
bd_we_high = "0" 
bd_we_veryhigh = "0"

# Hs100 (m)
bd_hs100_calm = "4.5" 
bd_hs100_open = "8.5" 

# U100 (m/s)
bd_u100 = "30" 

#-----------------------------------------------------------------------TECHNICAL POTENTIAL----------------------------------------------------------------------------------------------------------

# Technical potential SLS
def tp_sls():          # Define function for technical potential SLS
    
    wd_min = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wd_min")
    wd_max = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wd_max")
    ws = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ws")
    we = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\we")
    rc_hur = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\MFS.gdb\\rc_hur")
    
    # Process: Reclassify: reclassify maximum bathymetry to not suitable / suitable 
    rc_max = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_wd_max"
    Reclassify = rc_max
    rc_max = arcpy.sa.Reclassify(wd_max, "VALUE", f"-12000 {bd_wd_max} 1;{bd_wd_max} 501 0", "NODATA")
    rc_max.save(Reclassify)
    
    # Process: Reclassify: reclassify minimum bathymetry to not suitable / suitable 
    rc_min = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_wd_min"
    Reclassify = rc_min
    rc_min = arcpy.sa.Reclassify(wd_min, "VALUE", f"-12000 {bd_wd_min} 0;{bd_wd_min} 501 1", "NODATA")
    rc_min.save(Reclassify)
 
    # Process: Reclassify: reclassify wave energy to not suitable / suitable 
    rc_we = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_we"
    Reclassify = rc_we
    rc_we = arcpy.sa.Reclassify(we, "VALUE", f"0 {bd_we_quiescent};1 {bd_we_verylow};2 {bd_we_low};3 {bd_we_moderate};4 {bd_we_moderatelyhigh}; 5 {bd_we_high};6 {bd_we_veryhigh}", "NODATA")
    rc_we.save(Reclassify)

    # Process: Reclassify: reclassify wind speed to not suitable / suitable 
    rc_ws = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_ws"
    Reclassify = rc_ws
    rc_ws = arcpy.sa.Reclassify(ws, "VALUE", f"0 {bd_ws} 1;{bd_ws} 30 0", "NODATA")
    rc_ws.save(Reclassify)
    
    # Process: Weighted Overlay: SLS without hurricane risk
    sls_overlay = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_sls"
    Weighted_Overlay = sls_overlay
    overlay = arcpy.sa.WeightedOverlay(WOTable([[rc_ws, 25 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', '1']])], [rc_we, 25 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', 'NODATA']])], [rc_min, 25 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', 'NODATA']])], [rc_max, 25 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', 'NODATA']])]], [1, 9, 1]))
    overlay.save(Weighted_Overlay)

def tp_uls():             # Define function for technical potential ULS
    
    hs100 = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\hs100")
    u100 = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\u100")
    sls_overlay = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_sls")
    
    # Process: Reclassify: reclassify 100- year return significant wave height to not suitable / suitable
    rc_hs100 = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_hs100"
    Reclassify = rc_hs100
    rc_hs100 = arcpy.sa.Reclassify(hs100, "VALUE", f"0 {bd_hs100_calm} 1;{bd_hs100_calm} {bd_hs100_open} 2; {bd_hs100_open} 30 0", "NODATA")
    rc_hs100.save(Reclassify)
   
    # Process: Reclassify: reclassify 100-year return wind speed to not suitable / suitable
    rc_u100 = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_u100"
    Reclassify = rc_u100
    rc_u100 = arcpy.sa.Reclassify(u100, "VALUE", f"0 {bd_u100} 1;{bd_u100} 70 0", "NODATA")
    rc_u100.save(Reclassify)  
    
    # Process: Weighted Overlay: ULS
    uls_overlay = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_uls"
    Weighted_Overlay = uls_overlay
    uls_overlay = arcpy.sa.WeightedOverlay(WOTable([[sls_huroverlay, 33 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], [2, 1], ['NODATA', 'NODATA']])], [rc_hs100, 33 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], [2, 3], ['NODATA', 'NODATA']])], [rc_u100, 33 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', 'NODATA']])]], [1, 9, 1]))
    uls_overlay.save(Weighted_Overlay)
    print("weighted overlay sls uls done")

def tp_ocean_planning(): # Define function for technical potential Ocean planning
    
    ship_dens = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\ship_dens")
    wdpa = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\wdpa")
    uls_overlay = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_uls"
    
    # Process: Reclassify: reclassify shipping density to not suitable / suitable
    rc_ship_dens = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\reclass\\rc_ship_dens"
    Reclassify = rc_ship_dens
    rc_ship_dens = arcpy.sa.Reclassify(ship_dens, "VALUE", "0 5000000 1;5000000  70000000 0", "NODATA")
    rc_ship_dens.save(Reclassify)   
    
    # Process: Weighted Overlay: reclassify marine protected areas to not suitable / suitable
    ocpl_overlay = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_final"
    Weighted_Overlay = ocpl_overlay
    with arcpy.EnvManager(snapRaster=uls_overlay):
        ocpl_overlay = arcpy.sa.WeightedOverlay(WOTable([[uls_overlay, 33 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], [2, 3], ['NODATA', 'NODATA']])], [rc_ship_dens, 33 , 'Value' , RemapValue([[0, 'Restricted'], [1, 1], ['NODATA', 1]])], [wdpa, 33 , 'Value' , RemapValue([[0, 'Restricted'], ['NODATA', 1]])]], [1, 9, 1]))
        ocpl_overlay.save(Weighted_Overlay)
    print("weighted overlay final done")

#-----------------------------------------------------------------------MOTIVATION----------------------------------------------------------------------------------------------------------

    
def prox_cities():
    
    prox_cities = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\preprocessing\\final_input_layers\\prox_cities"
    tech_sls = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_sls")
    tech_sls_uls = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_uls")
    tech_final = arcpy.Raster("C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\overlay\\tech_final")
    
    # Process: Extract by Mask (6): exclude areas > 35 km from city centre SLS
    tech_mot = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\mot\\sls_mot"
    Extract_by_Mask = tech_mot
    tech_mot = arcpy.sa.ExtractByMask(tech_sls, prox_cities, "INSIDE", "-180.000927317815 -56.726731252263 180.011572682185 81.510768747737 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    tech_mot.save(Extract_by_Mask)
    print("motivation sls done")
    
    # Process: Extract by Mask (7): exclude areas > 35 km from city centre ULS
    tech_mot = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\mot\\uls_mot"
    Extract_by_Mask = tech_mot
    tech_mot = arcpy.sa.ExtractByMask(tech_sls_uls, prox_cities, "INSIDE", "-180.000927317815 -56.726731252263 180.011572682185 81.510768747737 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    tech_mot.save(Extract_by_Mask)
    print("motivation uls done")
    
    # Process: Extract by Mask (8): exclude areas > 35 km from city centre SLS, ULS, Ocean planning
    tech_mot = "C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\tech_pot\\mot\\final_mot"
    Extract_by_Mask = tech_mot
    tech_mot = arcpy.sa.ExtractByMask(tech_final, prox_cities, "INSIDE", "-180.000927317815 -56.726731252263 180.011572682185 81.510768747737 GEOGCS[\"GCS_WGS_1984\".DATUM[\"D_WGS_1984\".SPHEROID[\"WGS_1984\".6378137.0.298.257223563]].PRIMEM[\"Greenwich\".0.0].UNIT[\"Degree\".0.0174532925199433]]")
    tech_mot.save(Extract_by_Mask)
    print("motivation final done")

    
if __name__ == '__main__':
    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\MFS.gdb", workspace="C:\\Users\\lieke\\Documents\\ArcGIS_projects\\MFS\\MFS.gdb"):
        # tp_sls()
        # tp_uls()
        # tp_ocean_planning()
        # prox_cities()


