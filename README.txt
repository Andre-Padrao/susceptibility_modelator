In order to use this plugin, the user must have the QGIS software. In case the user doesn't, the most recent version can be found at https://www.qgis.org/en/site/forusers/download.html. Version 3.16 or higher is recommended.
The following Python libraries are also required for the functioning of the plugin. Please do have them installed and accessible to your QGIS Python interpreter, finding  the instruction for installation bellow:
- pandas: https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html;
- matplotlib: https://matplotlib.org/stable/users/installing.html;
- numpy: https://numpy.org/install/

If you wish to create an example susceptibility model, please follow these instructions:
1. After installing the Susceptibility modelator plugin and its respective dependencies, click on the respective icon at the toolbar;
2. Browse for example_geographical_information/Area_treino_3.shp as "Training area";
3. Browse for example_geographical_information/FozCoa.shp as "Modelation area";
4. Browse for example_geographical_information/raster_nulo.tif as "Null variable raster";
5. Browse for example_geographical_information/COS2018_N3.tif as "Variable 1 raster";
6. Browse for example_geographical_information/Declive.tif as "Variable 2 raster";
7. Browse for example_geographical_information/_ardidas2018.tif as "Occurances A";
8. Browse for example_geographical_information/_ardidas2017.tif as "Occurances B";
9. Optionally, add the remaining .tif files for extra years of information on fire occurance;
10. Browse for the directory where the output files will be saved;
11. Click "Run" and await for the processing to complete. This may take some minutes.
Following the instructions above should generate and open two fire susceptibility models (one for the target area and one for the surrounding training area) and four validation graphics.

This plugin is associated to the paper "A GIS plugin for wildfire susceptibility modeling: case study in Vila Nova de Foz Côa", by André Padrão et al., where one can find further details on its development and use. For more information, please contact apadrao@floradata.pt. 