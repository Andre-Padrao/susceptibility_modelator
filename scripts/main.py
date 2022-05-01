import os
import pandas

def main(self, ROC, area_treino,area_previsao,nulo,raster_variavel1,raster_variavel2,raster_variavel3,raster_variavel4,ocorrenciasA,ocorrenciasB,ocorrenciasC,ocorrenciasD,ocorrenciasE,ocorrenciasF,ocorrenciasG,ocorrenciasH,ocorrenciasI,ocorrenciasJ, diretorio):
    '''Função principal.'''
    if not os.path.exists(diretorio):
        os.mkdir(diretorio)
    def clip(input,mask,out):
        self.processing.run("gdal:cliprasterbymasklayer", {'INPUT':input,'MASK':mask,'SOURCE_CRS':None,'TARGET_CRS':None,'NODATA':-999999999,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':30,'Y_RESOLUTION':30,'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':out})

    # 0. ACOMODAR VARIÁVEIS VAZIAS
    expressao = '\"A@1\" + \"B@1\" + \"C@1\" + \"D@1\" + \"E@1\" + \"F@1\" + \"G@1\" + \"H@1\" + \"I@1\" + \"J@1\"'
    if ocorrenciasJ == '':
        ocorrenciasJ = nulo
        expressao = '\"B@1\" + \"C@1\" + \"D@1\" + \"E@1\" + \"F@1\" + \"G@1\" + \"H@1\" + \"I@1\"'
    if ocorrenciasI == '':
        ocorrenciasI = nulo
        expressao = '\"B@1\" + \"C@1\" + \"D@1\" + \"E@1\" + \"F@1\" + \"G@1\" + \"H@1\"'
    if ocorrenciasH == '':
        ocorrenciasH = nulo
        expressao = '\"B@1\" + \"C@1\" + \"D@1\" + \"E@1\" + \"F@1\" + \"G@1\"'
    if ocorrenciasG == '':
        ocorrenciasG = nulo
        expressao = '\"B@1\" + \"C@1\" + \"D@1\" + \"E@1\" + \"F@1\"'
    if ocorrenciasF == '':
        ocorrenciasF = nulo
        expressao = '\"A@1\" + \"B@1\" + \"C@1\" + \"D@1\" + \"E@1\"'
    if ocorrenciasE == '':
        ocorrenciasE = nulo
        expressao = '\"A@1\" + \"B@1\" + \"C@1\" + \"D@1\"'
    if ocorrenciasD == '':
        ocorrenciasD = nulo
        expressao = '\"A@1\" + \"B@1\" + \"C@1\"'
    if ocorrenciasC == '':
        ocorrenciasC = nulo
        expressao = '\"A@1\" + \"B@1\"'
    print('expressao ocorrencias: '+expressao)
    expressao_suscet = '\"scores1@1\" + \"scores2@1\" + \"scores3@1\" + \"scores4@1\"'
    if raster_variavel4 == '':
        raster_variavel4 = nulo
        expressao_suscet = '\"scores1@1\" + \"scores2@1\" + \"scores3@1\"'
    if raster_variavel3 == '':
        raster_variavel3 = nulo
        expressao_suscet = '\"scores1@1\" + \"scores2@1\"'
    if raster_variavel2 == '':
        raster_variavel2 = nulo
        expressao_suscet = '\"scores1@1\"'
    print('expressao suscetibilidade: '+expressao_suscet)

    # 1. GERAR BOOLEAN E ANTIBOOLEAN PARA AS ÁREAS DE OCORRÊNCIA

    # 1.1. Definir outputs
    soma = diretorio+'soma_ardidas.tif'
    raster_AA = diretorio+'ardidas_boolean.tif'
    raster_NA = diretorio+'ardidas_antiboolean.tif'

    # 1.2. Somar ocorrências (raster calculator)
    self.iface.addRasterLayer(ocorrenciasA,'A')
    self.iface.addRasterLayer(ocorrenciasB,'B')
    self.iface.addRasterLayer(ocorrenciasC,'C')
    self.iface.addRasterLayer(ocorrenciasD,'D')
    self.iface.addRasterLayer(ocorrenciasE,'E')
    self.iface.addRasterLayer(ocorrenciasF,'F')
    self.iface.addRasterLayer(ocorrenciasG,'G')
    self.iface.addRasterLayer(ocorrenciasH,'H')
    self.iface.addRasterLayer(ocorrenciasI,'I')
    self.iface.addRasterLayer(ocorrenciasJ,'J')

    self.processing.run("qgis:rastercalculator", {'EXPRESSION':expressao,'LAYERS':[ocorrenciasA],'CELLSIZE':0,'EXTENT':None,'CRS':None,'OUTPUT':soma})

    # 1.3. Calcular boolean de ocorrências (raster boolean "or")
    self.iface.addRasterLayer(soma,'soma')
    self.processing.run("native:rasterlogicalor", {'INPUT':[soma],'REF_LAYER':soma,'NODATA_AS_FALSE':False,'NO_DATA':-9999,'DATA_TYPE':5,'OUTPUT':raster_AA})

    # 1.4. Calcular antiboolean de ocorrências (reclassify by table (0 -> 1 ; 1 -> 0))
    self.iface.addRasterLayer(raster_AA,'boolean')
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':raster_AA,'RASTER_BAND':1,'TABLE':[0,0,1,1,1,0],'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':raster_NA})


    self.QgsProject.instance().clear()


    # 2. MODELAR SUSCETIBILIDADE NA ÁREA DE TREINO

    # 2.1. Definir outputs
    treino1 = diretorio+'treino1.tif'
    treino2 = diretorio+'treino2.tif'
    treino3 = diretorio+'treino3.tif'
    treino4 = diretorio+'treino4.tif'
    treino_ocorrencias =  diretorio+'treino_ardidas.tif'
    treino_naoocorrencias =  diretorio+'treino_naoardidas.tif'
    scores1 = diretorio+'scores1.tif'
    scores2 = diretorio+'scores2.tif'
    scores3 = diretorio+'scores3.tif'
    scores4 = diretorio+'scores4.tif'
    tab_scores1 = diretorio+'tab_scores1.csv'
    tab_scores2 = diretorio+'tab_scores2.csv'
    tab_scores3 = diretorio+'tab_scores3.csv'
    tab_scores4 = diretorio+'tab_scores4.csv'
    suscetibilidade_l = diretorio+'suscetibilidade_layout.tif'
    suscetibilidade_v = diretorio+'suscetibilidade_validacao.tif'
    susc_ocorrencias = diretorio+'TrueValuesReport.csv'
    susc_naoocorrencias = diretorio+'FalseValuesReport.csv'
    graf_curvas_susc = diretorio+'suscetibilidadeVsPixeis.png'
    graf_curva_ROC = diretorio+'curvaROC.png'

    # 2.2. Importar camadas
    self.iface.addRasterLayer(raster_variavel1,'raster_variavel1')
    self.iface.addRasterLayer(raster_variavel2,'raster_variavel2')
    self.iface.addRasterLayer(raster_variavel3,'raster_variavel3')
    self.iface.addRasterLayer(raster_variavel4,'raster_variavel4')
    self.iface.addRasterLayer(raster_AA,'raster_AA')
    self.iface.addRasterLayer(raster_NA,'raster_NA')


    # 2.3. Cortar rasters classificados pela área de treino
    clip(raster_variavel1, area_treino, treino1)
    clip(raster_variavel2, area_treino, treino2)
    clip(raster_variavel3, area_treino, treino3)
    clip(raster_variavel4, area_treino, treino4)
    clip(raster_AA, area_treino, treino_ocorrencias)
    clip(raster_NA, area_treino, treino_naoocorrencias)
    self.iface.addRasterLayer(treino1, 'treino1')
    self.iface.addRasterLayer(treino2, 'treino2')
    self.iface.addRasterLayer(treino3, 'treino3')
    self.iface.addRasterLayer(treino4, 'treino4')
    self.iface.addRasterLayer(treino_ocorrencias, 'treino_ocorrencias')
    self.iface.addRasterLayer(treino_naoocorrencias, 'treino_naoocorrencias')

    # 2.4. Transformar rasters classificados em scores de favorabilidade à ocorrência (valor informativo)
    report = diretorio+'report.csv'
    self.processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':treino_ocorrencias,'BAND':1,'OUTPUT_TABLE':report})
    file = pandas.read_csv(report, encoding= 'unicode_escape')# ler .csv
    pixels_naoocorrencias = int(file["count"][0])
    pixels_ocorrencias = int(file["count"][1])
    racio_ocorrencias = str(pixels_ocorrencias/(pixels_ocorrencias+pixels_naoocorrencias))
    formula_scores = 'if( \"sum\"=0, ln( (1/\"count\")/('+racio_ocorrencias+')),  ln( ( \"sum\"/\"count\")/('+racio_ocorrencias+')))'
    zones1 = diretorio+'zones1.tab'
    zones2 = diretorio+'zones2.tab'
    zones3 = diretorio+'zones3.tab'
    zones4 = diretorio+'zones4.tab'
    def calcular_scores(raster_ocorrencias, formula, raster_treino, tab_zones, tab_scores, raster_scores):
        self.processing.run("native:rasterlayerzonalstats", {'INPUT':raster_ocorrencias,'BAND':1,'ZONES':raster_treino,'ZONES_BAND':1,'REF_LAYER':0,'OUTPUT_TABLE':tab_zones})
        try:
            self.processing.run("native:fieldcalculator", {'INPUT':tab_zones,'FIELD_NAME':'score','FIELD_TYPE':0,'FIELD_LENGTH':2,'FIELD_PRECISION':2,'FORMULA':formula,'OUTPUT':tab_scores})
        except:
            self.processing.run("qgis:fieldcalculator", {'INPUT':tab_zones,'FIELD_NAME':'score','FIELD_TYPE':0,'FIELD_LENGTH':2,'FIELD_PRECISION':2,'FORMULA':formula,'OUTPUT':tab_scores})
        self.processing.run("native:reclassifybylayer", {'INPUT_RASTER':raster_treino,'RASTER_BAND':1,'INPUT_TABLE':tab_scores,'MIN_FIELD':'zone','MAX_FIELD':'zone','VALUE_FIELD':'score','NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':raster_scores})
    calcular_scores(treino_ocorrencias, formula_scores, treino1, zones1, tab_scores1, scores1)
    calcular_scores(treino_ocorrencias, formula_scores, treino2, zones2, tab_scores2, scores2)
    calcular_scores(treino_ocorrencias, formula_scores, treino3, zones3, tab_scores3, scores3)
    calcular_scores(treino_ocorrencias, formula_scores, treino4, zones4, tab_scores4, scores4)
    self.iface.addRasterLayer(scores1,'scores1')
    self.iface.addRasterLayer(scores2,'scores2')
    self.iface.addRasterLayer(scores3,'scores3')
    self.iface.addRasterLayer(scores4,'scores4')

    #-------------------------------------------------------------------------------------------------------------
    # 2.5. Gerar mapa de suscetibilidade
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':expressao_suscet,'LAYERS':[scores1],'CELLSIZE':0,'EXTENT':'48448.903700000,121190.901500000,120612.736400000,185795.019900000 [EPSG:3763]','CRS':None,'OUTPUT':suscetibilidade_l})
    self.iface.addRasterLayer(suscetibilidade_l, 'suscetibilidade_layout')
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':suscetibilidade_l,'RASTER_BAND':1,'TABLE':[0,0,0.1],'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':suscetibilidade_v})
    self.iface.addRasterLayer(suscetibilidade_v, 'suscetibilidade_validacao')

    # 2.6. Obter dados para validação
    true_part = diretorio+'true_part.tif'
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':'\"suscetibilidade_validacao@1\" * \"treino_ocorrencias@1\"','LAYERS':[suscetibilidade_v],'CELLSIZE':0,'EXTENT':None,'CRS':None,'OUTPUT':true_part})
    self.processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':true_part,'BAND':1,'OUTPUT_TABLE':susc_ocorrencias})
    false_part = diretorio+'false_part.tif'
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':'\"suscetibilidade_validacao@1\" * \"treino_naoocorrencias@1\"','LAYERS':[suscetibilidade_v],'CELLSIZE':0,'EXTENT':None,'CRS':None,'OUTPUT':false_part})
    self.processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':false_part,'BAND':1,'OUTPUT_TABLE':susc_naoocorrencias})
    self.iface.addVectorLayer(susc_naoocorrencias, 'susc_naoocorrencias', 'ogr')
    self.iface.addVectorLayer(susc_ocorrencias, 'susc_ocorrencias', 'ogr')

    # 2.7. Construir gráficos de validação
    ROC(susc_naoocorrencias,susc_ocorrencias, graf_curvas_susc, graf_curva_ROC)


    self.QgsProject.instance().clear()


    # 3. CALCULAR SUSCETIBILDADE NA ÁREA DE PREVISÃO
    # -*- coding: utf-8 -*-

    # 3.1. Definir outputs
    previsao1 = diretorio+'previsao1.tif'
    previsao2 = diretorio+'previsao2.tif'
    previsao3 = diretorio+'previsao3.tif'
    previsao4 = diretorio+'previsao4.tif'
    previsao_ocorrencias =  diretorio+'previsao_ocorrencias.tif'
    previsao_naoocorrencias =  diretorio+'previsao_naoocorrencias.tif'
    previsao_nulo = diretorio+'previsao_nulo.tif'
    P_scores1 = diretorio+'P_scores1.tif'
    P_scores2 = diretorio+'P_scores2.tif'
    P_scores3 = diretorio+'P_scores3.tif'
    P_scores4 = diretorio+'P_scores4.tif'
    P_suscetibilidade_l = diretorio+'P_suscetibilidade_layout.tif'
    P_suscetibilidade_v = diretorio+'P_suscetibilidade_validacao.tif'
    P_susc_ocorrencias = diretorio+'P_TrueValuesReport.csv'
    P_susc_naoocorrencias = diretorio+'P_FalseValuesReport.csv'
    P_graf_curvas_susc = diretorio+'P_suscetibilidadeVsPixeis.png'
    P_graf_curva_ROC = diretorio+'P_curvaROC.png'

    # 3.2 Obter listas-tabela de reclassificação com scores
    def tabelas_reclass(tabela_scores):
        reclass_table = []
        file = pandas.read_csv(tabela_scores, encoding = 'unicode_escape')
        for n,c in enumerate(file["zone"]):
            reclass_table.append(int(c))
            reclass_table.append(int(c))
            reclass_table.append(float(file["score"][n]))
        print(reclass_table)
        return reclass_table
    reclass_table1 = tabelas_reclass(tab_scores1)
    reclass_table2 = tabelas_reclass(tab_scores2)
    reclass_table3 = tabelas_reclass(tab_scores3)
    reclass_table4 = tabelas_reclass(tab_scores4)


    # 3.3. Cortar rasters classificados pela área de previsao
    self.iface.addRasterLayer(raster_variavel1,'raster_variavel1')
    self.iface.addRasterLayer(raster_variavel2,'raster_variavel2')
    self.iface.addRasterLayer(raster_variavel3,'raster_variavel3')
    self.iface.addRasterLayer(raster_variavel4,'raster_variavel4')
    self.iface.addRasterLayer(raster_AA,'raster_AA')
    self.iface.addRasterLayer(raster_NA,'raster_NA')
    clip(raster_variavel1, area_previsao, previsao1)
    clip(raster_variavel2, area_previsao, previsao2)
    clip(raster_variavel3, area_previsao, previsao3)
    clip(raster_variavel4, area_previsao, previsao4)
    clip(raster_AA, area_previsao, previsao_ocorrencias)
    clip(raster_NA, area_previsao, previsao_naoocorrencias)
    self.iface.addRasterLayer(previsao1, 'previsao1')
    self.iface.addRasterLayer(previsao2, 'previsao2')
    self.iface.addRasterLayer(previsao3, 'previsao3')
    self.iface.addRasterLayer(previsao4, 'previsao4')
    self.iface.addRasterLayer(previsao_ocorrencias, 'previsao_ocorrencias')
    self.iface.addRasterLayer(previsao_naoocorrencias, 'previsao_naoocorrencias')


    # 3.4. Transformar rasters classificados em scores de favorabilidade a incêndios (valor preditivo)
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':previsao1,'RASTER_BAND':1,'TABLE':reclass_table1,'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':P_scores1})
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':previsao2,'RASTER_BAND':1,'TABLE':reclass_table2,'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':P_scores2})
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':previsao3,'RASTER_BAND':1,'TABLE':reclass_table3,'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':P_scores3})
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':previsao4,'RASTER_BAND':1,'TABLE':reclass_table4,'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':P_scores4})
    self.iface.addRasterLayer(P_scores1,'scores1')
    self.iface.addRasterLayer(P_scores2,'scores2')
    self.iface.addRasterLayer(P_scores3,'scores3')
    self.iface.addRasterLayer(P_scores4,'scores4')

    # 3.5. Gerar mapa de suscetibilidade
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':expressao_suscet,'LAYERS':[P_scores1],'CELLSIZE':0,'EXTENT':'48448.903700000,121190.901500000,120612.736400000,185795.019900000 [EPSG:3763]','CRS':None,'OUTPUT':P_suscetibilidade_l})
    self.iface.addRasterLayer(P_suscetibilidade_l, 'P_suscetibilidade_layout')
    self.processing.run("native:reclassifybytable", {'INPUT_RASTER':P_suscetibilidade_l,'RASTER_BAND':1,'TABLE':[0,0,0.1],'NO_DATA':-9999,'RANGE_BOUNDARIES':2,'NODATA_FOR_MISSING':False,'DATA_TYPE':5,'OUTPUT':P_suscetibilidade_v})
    self.iface.addRasterLayer(P_suscetibilidade_v, 'P_suscetibilidade_validacao')

    # 3.6. Obter dados para validação
    P_true_part = diretorio+'P_true_part.tif'
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':'\"P_suscetibilidade_validacao@1\" * \"previsao_ocorrencias@1\"','LAYERS':[P_suscetibilidade_v],'CELLSIZE':0,'EXTENT':None,'CRS':None,'OUTPUT':P_true_part})
    self.processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':P_true_part,'BAND':1,'OUTPUT_TABLE':P_susc_ocorrencias})
    P_false_part = diretorio+'P_false_part.tif'
    self.processing.run("qgis:rastercalculator", {'EXPRESSION':'\"P_suscetibilidade_validacao@1\" * \"previsao_naoocorrencias@1\"','LAYERS':[P_suscetibilidade_v],'CELLSIZE':0,'EXTENT':None,'CRS':None,'OUTPUT':P_false_part})
    self.processing.run("native:rasterlayeruniquevaluesreport", {'INPUT':P_false_part,'BAND':1,'OUTPUT_TABLE':P_susc_naoocorrencias})
    self.iface.addVectorLayer(P_susc_naoocorrencias, 'P_susc_naoardidas', 'ogr')
    self.iface.addVectorLayer(P_susc_ocorrencias, 'P_susc_ardidas', 'ogr')

    # 3.7. Construir gráficos de validação
    ROC(P_susc_naoocorrencias, P_susc_ocorrencias, P_graf_curvas_susc, P_graf_curva_ROC)

    self.QgsProject.instance().clear()
