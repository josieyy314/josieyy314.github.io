# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# model_script.py
# Created on: 2018-05-09 13:15:55.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: model_script <Route__3_> 
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Local variables:
Navigation_ND = "U:\\GEOG_469\\Routing.gdb\\Navigation\\Navigation_ND"
POI = "U:\\GEOG_469\\Routing.gdb\\POI"
Solve_Succeeded = "true"

# Process: Make Route Layer
arcpy.MakeRouteLayer_na(Navigation_ND, "Route", "Walktime", "FIND_BEST_ORDER", "PRESERVE_BOTH", "NO_TIMEWINDOWS", "", "ALLOW_UTURNS", "'Avoid High';'Prefer Low';'Avoid Medium'", "NO_HIERARCHY", "", "TRUE_LINES_WITH_MEASURES", "")

# Process: Convert InteriorSpace_Points feature class to a layer
arcpy.MakeFeatureLayer_management(POI, "classrooms")

# Create a new geodatabase in your folder
# Process: Convert Merged Schedule Excel Table to a Table in ArcMap
arcpy.env.workspace = "U:\GEOG_469"
arcpy.ExcelToTable_conversion("schedule_ID_excel.xlsx","schedule.dbf")

#IMPORTANT!!!! manually add field to schedule table, name the field as "walk_time".

# Process: Get a list of Sorted and Paired Classroom ID
spaceID_list = [r[0] for r in arcpy.da.SearchCursor("schedule", "space")]

walktime_list = []
def checkIfComputed(class1, class2):
	for row in walktime_list:
		if class1 in (row[0], row[1]) and class2 in (row[0], row[1]):
			return row[2]

count = 0
# Add a new field to the table 
# Process: For each paired classrooms, calculate the walk time
for idx, each_classR in enumerate(spaceID_list):
	if idx < len(spaceID_list) and (idx % 2 == 0):
		next_idx = idx + 1
		class1 = spaceID_list[idx]
		class2 = spaceID_list[next_idx]
		
		computed_time = checkIfComputed(class1, class2)
		walktime = []
		if class1 == class2 or '1126_02' in class1 or '1126_02' in class2:
			walktime = [999.0]
		elif computed_time < 0:
			# Process: Select Layer By Attribute
			arcpy.SelectLayerByAttribute_management("classrooms", "NEW_SELECTION", "SPACEID IN ( '" + class1 + "' , '" + class2 +"' )")

			# Process: Add Locations
			arcpy.AddLocations_na("Route", "Stops", "classrooms", "", "5000 Meters", "", "way SHAPE;Navigation_ND_Junctions NONE", "MATCH_TO_CLOSEST", "CLEAR", "NO_SNAP", "5 Meters", "INCLUDE", "way #;Navigation_ND_Junctions #")

			# Process: Solve
			arcpy.Solve_na("Route", "SKIP", "TERMINATE", "", "")
	
			walktime = [r[0] for r in arcpy.da.SearchCursor(r"Route\Routes", "Total_Walktime")]
			
			walktime_list.append([class1, class2, walktime[0]])
		
		else:
			
			walktime = [computed_time]
			
		update_cursor = arcpy.da.UpdateCursor("schedule_final",["walk_time", "OID@", "space"])
		print(walktime[0])
		for row in update_cursor:
			if row[1] == (idx + 2490):
				row[0] = walktime[0]
				update_cursor.updateRow(row)
				
		del update_cursor
		
		count = count + 1
		
print('Updated total of {} line'.format(count)
