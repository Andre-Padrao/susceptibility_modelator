# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SusceptibilityModelator
                                 A QGIS plugin
 Produces and validates susceptibility models for various risk factors
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-10-17
        git sha              : $Format:%H$
        copyright            : (C) 2021 by André Padrão
        email                : andre27.f@hotmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .susceptibility_modelator_dialog import SusceptibilityModelatorDialog
import os.path
# Importar bibliotecas criadas pelo autor
from .scripts.main import main
from .scripts.validacao import ROC

class SusceptibilityModelator:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # import libraries for main.py
        import processing
        self.processing = processing
        from qgis.core import QgsProject
        self.QgsProject = QgsProject
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SusceptibilityModelator_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Susceptibility Modelator')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SusceptibilityModelator', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/susceptibility_modelator/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Susceptibility modelator'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Susceptibility Modelator'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = SusceptibilityModelatorDialog()

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Definir inputs
            area_treino = self.dlg.training_area.filePath()#'D:/biblioteca_suscetibilidade/Area_treino_3.shp'#
            area_previsao = self.dlg.modelation_area.filePath()#D:/biblioteca_suscetibilidade/FozCoa.shp
            nulo = self.dlg.null_variable_raster.filePath()#D:/biblioteca_suscetibilidade/raster_nulo.tif
            raster_variavel1 = self.dlg.variable_1_raster.filePath()#D:/biblioteca_suscetibilidade/COS2018_N3.tif
            raster_variavel2 = self.dlg.variable_2_raster.filePath()#D:/biblioteca_suscetibilidade/Declive.tif
            raster_variavel3 = self.dlg.variable_3_raster.filePath()#
            raster_variavel4 = self.dlg.variable_4_raster.filePath()#
            ocorrenciasA = self.dlg.occurances_A.filePath()#D:/biblioteca_suscetibilidade/_ardidas2018.tif
            ocorrenciasB = self.dlg.occurances_B.filePath()#D:/biblioteca_suscetibilidade/_ardidas2017.tif
            ocorrenciasC = self.dlg.occurances_C.filePath()
            ocorrenciasD = self.dlg.occurances_D.filePath()
            ocorrenciasE = self.dlg.occurances_E.filePath()
            ocorrenciasF = self.dlg.occurances_F.filePath()
            ocorrenciasG = self.dlg.occurances_G.filePath()
            ocorrenciasH = self.dlg.occurances_H.filePath()
            ocorrenciasI = self.dlg.occurances_I.filePath()
            ocorrenciasJ = self.dlg.occurances_J.filePath()
            # Definir diretório de destino
            diretorio = self.dlg.out_dir.filePath()#D:/biblioteca_suscetibilidade/teste/
            if diretorio != '\\':
                diretorio = str(diretorio)+'\\'
            # Chamar a função principal
            main(self, ROC, area_treino,area_previsao,nulo,raster_variavel1,raster_variavel2,raster_variavel3,raster_variavel4,ocorrenciasA,ocorrenciasB,ocorrenciasC,ocorrenciasD,ocorrenciasE,ocorrenciasF,ocorrenciasG,ocorrenciasH,ocorrenciasI,ocorrenciasJ, diretorio)

            self.iface.addRasterLayer(diretorio+'suscetibilidade_layout.tif', 'susceptibility - target area')
            self.iface.addRasterLayer(diretorio+'P_suscetibilidade_layout.tif', 'susceptibility - training area')