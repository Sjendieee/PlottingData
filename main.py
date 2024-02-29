import matplotlib
from matplotlib import pyplot as plt
import numpy as np
import glob
import os
import csv
import re
import pandas as pd


def importDataFromTxt(filename):
    """
    :param filename: full filepath to .txt file
    :return:
    """
    data = pd.read_csv(filename, sep="\t", encoding = "mbcs", skiprows=7, header='infer')
    data_np = data.to_numpy()
    data_arr = []
    for i in range(0, data.shape[1]):    #iterate over every column
        temp_arr = []
        for ii in range(0, data.shape[0]): #iterate over every row
            temp_arr.append(float(str(data_np[ii][i]).replace(',', '.')))
        data_arr.append(temp_arr)
    return data_arr

def plotGraph(datax, datay, xlabel, ylabel, title, source, b1, b2, outputSpecification, PLOTREGIMES):
    fig1, ax1 = plt.subplots()
    ax1.plot(np.subtract(datax, datax[0]), datay, '.')
    if PLOTREGIMES:
        ax1.axvspan(0, b1, facecolor='blue', alpha=0.3, label='32C')
        ax1.axvspan(b1, b2, facecolor='orange', alpha=0.3, label='33C')
        ax1.axvspan(b2, (max(datax) - datax[0]), facecolor='red', alpha=0.3, label='34C')
        ax1.legend(loc='best')
    ax1.set(xlabel=xlabel, ylabel=ylabel, title=title)
    plt.show()
    fig1.savefig(os.path.join(os.path.dirname(source), f'{outputSpecification} [{os.path.basename(source)}].png'), dpi=600)


def main():
    """
    File for plotting contact angles versus measurement nr. (or time) from a .txt file, obtained from the goneometer at PCF.
    Possibility for inputting regimes with color in plot where e.g. the temperature was differed with b1, b2 (and more if desired).


    *Currently labels & colors for regimes are hardcoded in plotGraph().
    """
    source = 'F:\\2024_02_23_microscopy hexadecane PODMA_2_4_4\\Temp 26 - 34C.txt'  #framerate was like 5.7 frames per second
    #source = 'F:\\2024_02_23_microscopy hexadecane PODMA_2_5_1\\Measered CA PODMA RT 33-34-34_5C.txt'   #framerate was like 5.7 frames per second
    source = 'F:\\2024_02_23_microscopy hexadecane PLMA 2_5_4\\Measered CA PLMA RT.txt' #framerate was like 5.7 frames per second
    data = importDataFromTxt(source)

    #Boundaries for different temps
    b1 = (420 - data[4][0])
    b2 = (640 - data[4][0])
    PLOTREGIMES = False



    #PLOT vs measurement nr.
    plotGraph(data[4], data[0], 'Measurement number', 'Mean contact angle [deg]', 'PODMA: Measured contact angle as a function of time (implicit)', source, b1, b2, "Contact angle vs measurement number", PLOTREGIMES)

    #PLOT vs time (from known framerate camera capture)
    framerate = 5.7         #frames/second
    plotGraph(np.divide(data[4], framerate), data[0], 'Time (s)', 'Mean contact angle [deg]', 'PODMA: Measured contact angle as a function of time', source, b1/framerate, b2/framerate, "Contact angle vs time", PLOTREGIMES)



if __name__ == "__main__":
    main()
    exit()
