import csv
import matplotlib.pyplot as plt
import numpy

# CONSTRUÇÃO DO GRÁFICO DE FREQUÊNCIA DE SUSCETIBILIDADES
# função gera 1º gráfico e retorna tupla com all positives, all negatives e max negative
def curvas(real_false_path, real_true_path, graf_curvas_susc):
    all_positives = 0
    all_negatives = 0
    max_negative = -100
    min_negative = 100

    filename = real_true_path# ler .csv com scores dos píxeis com ocorrências
    with open(filename, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        # print(header_row) # ['value', 'count', 'mÂ²']
        realTrue = []
        for registo in reader:
            if float(registo[0]) != 0:# excluir píxeis correspondentes à parte false (multiplicados por 0)
                if float(registo[0]) == 0.1:
                    valor = 0
                else:
                    valor = registo[0]
                tupla = (float(valor), float(registo[1]))# tupla = (value, count)
                realTrue.append(tupla)
                all_positives += float(registo[1])
        # realTrue.sort(reverse=True)

    filename = real_false_path# ler .csv com scores dos píxeis com não-ocorrências
    with open(filename, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        # print(header_row) # ['value', 'count', 'mÂ²']
        realFalse = []
        for registo in reader:
            if float(registo[0]) != 0:# excluir píxeis correspondentes à parte true (multiplicados por 0)
                if float(registo[0]) == 0.1:
                    valor = 0
                else:
                    valor = registo[0]
                tupla = (float(valor), float(registo[1]))# tupla = (value, count)
                realFalse.append(tupla)
                all_negatives += float(registo[1])
                if float(valor) > max_negative:
                    max_negative = float(valor)
                if float(valor) < min_negative:
                    min_negative = float(valor)
                

    countT = []
    probT = []
    countF = []
    probF = []
    for c in realTrue:
        probT.append(c[0])
        countT.append(c[1])
    for c in realFalse:
        probF.append(c[0])
        countF.append(c[1])

    # Gerar gráfico e retorno

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    # ax.plot(x, y, etc)
    ax.plot(probF, countF, c='blue', linewidth=3, label = 'Pixels without occurances (real false)')
    ax.plot(probT, countT, c='red', linewidth=2, label = 'Pixels with occurances (real true)')
    ax.legend(loc="best", bbox_to_anchor=(0.4,-0.2))
    plt.subplots_adjust(bottom=0.25)

    ax.set_title('Susceptibility vs Nr. of pixels', fontsize=16)
    ax.set_xlabel('Susceptibility of pixel being True in the prediction', fontsize=12)
    ax.set_ylabel('Pixel count', fontsize=12)

    print('Saving the graphic...')
    plt.savefig(graf_curvas_susc,bbox_inches='tight')
    print('real positive pixels: ',all_positives,'  real negative pixels:',all_negatives, '  max. negative score: ', max_negative, '  min. negative score: ', min_negative)
    return (all_positives, all_negatives, max_negative, min_negative)


# GERAÇÃO DE PONTOS DA REGRESSIVE OPERATING CHARACTERISTIC (ROC) CURVE
# função devolve FPR (x) e TPR (y) de cada ponto da curva ROC
def gerar_ponto(threshold, real_false_path, real_true_path, all_negatives, all_positives, maximo, minimo):
    true_positives = 0
    false_positives = 0

    filename = real_false_path
    with open(filename, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        # print(header_row) # ['value', 'count', 'mÂ²']
        for registo in reader:
            if float(registo[0]) != 0:# excluir píxeis correspondentes à parte true (multiplicados por 0)
                if float(registo[0]) == 0.1:
                    valor = 0
                else:
                    valor = registo[0]
                if float(valor) < threshold:
                    continue
                elif float(valor) == threshold:
                    if float(valor) == maximo:
                        continue
                    elif float(valor) == minimo:
                        false_positives += float(registo[1])
                    else:
                        continue
                else:
                    false_positives += float(registo[1])

    filename = real_true_path
    with open(filename, encoding="utf8", errors='ignore') as f:
        reader = csv.reader(f)
        header_row = next(reader)
        # print(header_row) # ['value', 'count', 'mÂ²']
        realTrue = []
        for registo in reader:
            if float(registo[0]) != 0:# excluir píxeis correspondentes à parte true (multiplicados por 0)
                if float(registo[0]) == 0.1:
                    valor = 0
                else:
                    valor = registo[0]
                if float(valor) < threshold:
                    continue
                elif float(valor) == threshold:
                    if float(valor) == maximo:
                        continue
                    elif float(valor) == minimo:
                        true_positives += float(registo[1])
                    else:
                        continue
                else:
                    true_positives += float(registo[1])
    FPR = false_positives / all_negatives
    TPR = true_positives / all_positives
    return (FPR, TPR)


# CONSTRUÇÃO E ANÁLISE DA REGRESSIVE OPERATING CHARACTERISTIC (ROC) CURVE
#função ROC, gera 2º gráfico e calcula AUC
def ROC(real_false_path, real_true_path, graf_curvas_susc, graf_curva_ROC):
    global curvas
    global gerar_ponto
    stats = curvas(real_false_path, real_true_path, graf_curvas_susc)
    all_positives = stats[0]
    all_negatives = stats[1]
    max_negative = stats[2]
    min_negative = stats[3]
    centesima = (max_negative-min_negative)/100
    FPRs = []
    TPRs = []
    threshold = max_negative
    while threshold > min_negative:
        ponto = gerar_ponto(threshold, real_false_path, real_true_path, all_negatives, all_positives, max_negative, min_negative)
        FPRs.append(ponto[0])
        TPRs.append(ponto[1])
        threshold -= centesima

    # Calcular Area Under Curve com a composite trapezoidal rule do numpy
    ordenadas = numpy.array(TPRs)
    abcissas = numpy.array(FPRs)
    AUC = numpy.trapz(ordenadas, x=abcissas)

    # Gerar gráfico

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    # ax.plot(x, y, etc)
    ax.plot(FPRs, TPRs, c='green', linewidth=2)

    ax.set_title(f'ROC curve (AUC = {round(AUC,2)})', fontsize=16)
    ax.set_xlabel('False Positive Ratio', fontsize=12)
    ax.set_ylabel('True Positive Ratio', fontsize=12)
    
    print('Saving the graphic...')
    plt.savefig(graf_curva_ROC, bbox_inches='tight')
    plt.show()