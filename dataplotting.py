def firingrates(title, fr1, color1, label1, fr2, color2, label2, fr3, color3, label3):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Firing Rate [Hz]")
    plt.plot(xaxis, fr1.values[i*span:(i+1)*span], color1, label=label1)
    plt.plot(xaxis, fr2.values[i*span:(i+1)*span], color2, label=label2)
    plt.plot(xaxis, fr3.values[i*span:(i+1)*span], color3, label=label3)
    plt.legend()

def cvs(title, cv1, color1, label1, cv2, color2, label2, cv3, color3, label3):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("CV")
    plt.plot(xaxis, cv1.values[i*span:(i+1)*span], color1, label=label1)
    plt.plot(xaxis, cv2.values[i*span:(i+1)*span], color2, label=label2)
    plt.plot(xaxis, cv3.values[i*span:(i+1)*span], color3, label=label3)
    plt.legend()

def sync(title, syn1, color1, label1, syn2, color2, label2, syn3, color3, label3, syn4, color4, label4):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Sync. Value")
    plt.plot(xaxis, syn1.values[i*span:(i+1)*span], color1, label=label1)
    plt.plot(xaxis, syn2.values[i*span:(i+1)*span], color2, label=label2)
    plt.plot(xaxis, syn3.values[i*span:(i+1)*span], color3, label=label3)
    plt.plot(xaxis, syn4.values[i*span:(i+1)*span], color4, label=label4)
    plt.legend()

import matplotlib.pyplot as plt
import pandas
import argparse
import seaborn
from os import path

parser = argparse.ArgumentParser(description="Data Plotting script using .csv files")

parser.add_argument("filename", help="Name of the .csv file", type=str)
parser.add_argument("fixwhat", help="What frequencies to lock?", type=str, choices=["ctxrate","strrate","none"])
parser.add_argument("whattodo", help="What plot should I show?", type=str, choices=["firingrates","beta","cvs","syncs","pivot"])
parser.add_argument("-v", "--verbose", action="count", help="shows what is going on")

args = parser.parse_args()

my_csv_file = args.filename
gen_path = "/home/fvm/Scrivania/"
final_path = path.join(gen_path, my_csv_file)
if args.verbose == 1:
    print(f"Il percorso selezionato è {final_path}\n")

datas_from_csv = pandas.read_csv(final_path)

if args.verbose == 1:
    print(f"Ecco i dati che hai appena importato:\n\n {datas_from_csv}\n")

if args.fixwhat == "ctxrate":
    whichis = "Cortex"
    whatx = "Striatum"
    rateCTX = datas_from_csv["Rate CTX"]
    rateSTR = datas_from_csv["Rate STR"]
    frgpea = datas_from_csv["F.R. GPe A"]
    frgpeb = datas_from_csv["F.R. GPe B"]
    frgpec = datas_from_csv["F.R. GPe C"]
    frstnrb = datas_from_csv["F.R. STN RB"]
    frstnllrs = datas_from_csv["F.R. STN LLRS"]
    frstnnr = datas_from_csv["F.R. STN NR"]
    cvgpea = datas_from_csv["CV GPe A"]
    cvgpeb = datas_from_csv["CV GPe B"]
    cvgpec = datas_from_csv["CV GPe C"]
    cvstnrb = datas_from_csv["CV STN RB"]
    cvstnllrs = datas_from_csv["CV STN LLRS"]
    cvstnnr = datas_from_csv["CV STN NR"]
    betastn = datas_from_csv["Beta % STN"]
    betagpe = datas_from_csv["Beta % GPe"]
    specgpe = datas_from_csv["Spectral Entropy GPe"]
    specstn = datas_from_csv["Spectral Entropy STN"]
    syncgpea = datas_from_csv["Sync. Param. GPe A"]
    syncgpeb = datas_from_csv["Sync. Param. GPe B"]
    syncgpec = datas_from_csv["Sync. Param. GPe C"]
    syncgpe = datas_from_csv["Sync. Param. GPe"]
    syncstnrb = datas_from_csv["Sync. Param. STN RB"]
    syncstnllrs = datas_from_csv["Sync. Param. STN LLRS"]
    syncstnnr = datas_from_csv["Sync. Param. STN NR"]
    syncstn = datas_from_csv["Sync. Param. STN"]

    i = int(input(f"Scegli la frequenza di input di {whichis}: "))
    span = 48

    xaxis = rateSTR.values[i*span:(i+1)*span]

elif args.fixwhat == "strrate":
    whichis = "Striatum"
    whatx = "Cortex"
    datas_from_csv = datas_from_csv.sort_values(["Rate STR","Rate CTX"])
    rateCTX = datas_from_csv["Rate CTX"]
    rateSTR = datas_from_csv["Rate STR"]
    frgpea = datas_from_csv["F.R. GPe A"]
    frgpeb = datas_from_csv["F.R. GPe B"]
    frgpec = datas_from_csv["F.R. GPe C"]
    frstnrb = datas_from_csv["F.R. STN RB"]
    frstnllrs = datas_from_csv["F.R. STN LLRS"]
    frstnnr = datas_from_csv["F.R. STN NR"]
    cvgpea = datas_from_csv["CV GPe A"]
    cvgpeb = datas_from_csv["CV GPe B"]
    cvgpec = datas_from_csv["CV GPe C"]
    cvstnrb = datas_from_csv["CV STN RB"]
    cvstnllrs = datas_from_csv["CV STN LLRS"]
    cvstnnr = datas_from_csv["CV STN NR"]
    betastn = datas_from_csv["Beta % STN"]
    betagpe = datas_from_csv["Beta % GPe"]
    syncgpea = datas_from_csv["Sync. Param. GPe A"]
    syncgpeb = datas_from_csv["Sync. Param. GPe B"]
    syncgpec = datas_from_csv["Sync. Param. GPe C"]
    syncgpe = datas_from_csv["Sync. Param. GPe"]
    syncstnrb = datas_from_csv["Sync. Param. STN RB"]
    syncstnllrs = datas_from_csv["Sync. Param. STN LLRS"]
    syncstnnr = datas_from_csv["Sync. Param. STN NR"]
    syncstn = datas_from_csv["Sync. Param. STN"]

    i = int(input(f"Scegli la frequenza di input di {whichis}: "))
    span = 41

    xaxis = rateCTX.values[i*span:(i+1)*span]

if args.whattodo == "firingrates":
    plt.figure(1)
    firingrates(f"F.R. GPe; {whichis} Rate = {i} Hz", frgpea, "r", "F.R. GPe A", frgpeb, "g", "F.R. GPe B", frgpec, "b", "F.R. GPe C")
    plt.figure(2)
    firingrates(f"F.R. STN; {whichis} Rate = {i} Hz", frstnrb, "r", "F.R. STN RB", frstnllrs, "g", "F.R. STN LLRS", frstnnr, "b", "F.R. STN NR")
    plt.show()
elif args.whattodo == "cvs":
    plt.figure(1)
    cvs(f"Coeff. Var.; {whichis} Rate = {i} Hz", cvgpea, "r", "GPe A", cvgpeb, "g", "GPe B", cvgpec, "b", "GPe C")
    plt.figure(2)
    cvs(f"Coeff. Var.; {whichis} Rate = {i} Hz", cvstnrb, "r", "STN RB", cvstnllrs, "g", "STN LLRS", cvstnnr, "b", "STN NR")
    plt.show()
elif args.whattodo == "syncs":
    plt.figure(1)
    sync(f"Sync. Val.; {whichis} Rate = {i} Hz", syncgpea, "r", "GPe A", syncgpeb, "g", "GPe B", syncgpec, "b", "GPe C", syncgpe, "k", "GPe")
    plt.figure(2)
    sync(f"Sync. Val.; {whichis} Rate = {i} Hz", syncstnrb, "r", "STN RB", syncstnllrs, "g", "STN LLRS", syncstnnr, "b", "STN NR", syncstn, "k", "STN")
    plt.show()
elif args.whattodo == "beta":
    plt.figure(1)
    plt.title(f"Beta % in PSD STN and GPe; {whichis} Rate = {i} Hz")
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Beta %")
    plt.plot(xaxis, betastn.values[i*span:(i+1)*span], "r", label="Beta STN")
    plt.plot(xaxis, betagpe.values[i*span:(i+1)*span], "g", label="Beta GPe")
    plt.legend()
    plt.show()
elif args.whattodo == "pivot":
    frgpea_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. GPe A"]
    frgpeb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. GPe B"]
    frgpec_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. GPe C"]

    frstnrb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. STN RB"]
    frstnllrs_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. STN LLRS"]
    frstnnr_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["F.R. STN NR"]

    cvgpea_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV GPe A"]
    cvgpeb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV GPe B"]
    cvgpec_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV GPe C"]

    cvstnrb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV STN RB"]
    cvstnllrs_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV STN LLRS"]
    cvstnnr_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["CV STN NR"]

    betastn_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Beta % STN"]
    betagpe_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Beta % GPe"]

    specstn_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Spectral Entropy STN"]
    specgpe_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Spectral Entropy GPe"]

    syncgpea_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. GPe A"]
    syncgpeb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. GPe B"]
    syncgpec_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. GPe C"]
    syncgpe_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. GPe"]

    syncstnrb_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. STN RB"]
    syncstnllrs_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. STN LLRS"]
    syncstnnr_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. STN NR"]
    syncstn_pivot = datas_from_csv.pivot(index="Rate CTX", columns="Rate STR")["Sync. Param. STN"]

    colors = seaborn.color_palette("coolwarm")
    
    plt.figure("Firing Rate GPe B")
    plt.title("Firing Rate GPe B [Hz]")
    ax1 = seaborn.heatmap(frgpeb_pivot, cmap=colors)

    plt.figure("Firing Rate GPe A")
    plt.title("Firing Rate GPe A [Hz]")
    ax2 = seaborn.heatmap(frgpea_pivot, cmap=colors)

    plt.figure("Firing Rate GPe C")
    plt.title("Firing Rate GPe C [Hz]")
    ax3 = seaborn.heatmap(frgpec_pivot, cmap=colors)

    plt.figure("Firing Rate STN RB")
    plt.title("Firing Rate STN RB [Hz]")
    ax4 = seaborn.heatmap(frstnrb_pivot, cmap=colors)

    plt.figure("Firing Rate STN LLRS")
    plt.title("Firing Rate STN LLRS [Hz]")
    ax5 = seaborn.heatmap(frstnllrs_pivot, cmap=colors)

    plt.figure("Firing Rate STN NR")
    plt.title("Firing Rate STN NR [Hz]")
    ax6 = seaborn.heatmap(frstnnr_pivot, cmap=colors)
    
    plt.figure("CV GPe A")
    plt.title("CV GPe A")
    ax7 = seaborn.heatmap(cvgpea_pivot, cmap=colors)

    plt.figure("CV GPe B")
    plt.title("CV GPe B")
    ax8 = seaborn.heatmap(cvgpeb_pivot, cmap=colors)

    plt.figure("CV GPe C")
    plt.title("CV GPe C")
    ax9 = seaborn.heatmap(cvgpec_pivot, cmap=colors)

    plt.figure("CV STN RB")
    plt.title("CV STN RB")
    ax10 = seaborn.heatmap(cvstnrb_pivot, cmap=colors)

    plt.figure("CV STN LLRS")
    plt.title("CV STN LLRS")
    ax11 = seaborn.heatmap(cvstnllrs_pivot, cmap=colors)

    plt.figure("CV STN NR")
    plt.title("CV STN NR")
    ax12 = seaborn.heatmap(cvstnnr_pivot, cmap=colors)
    
    plt.figure("Beta STN")
    plt.title("Beta STN")
    ax13 = seaborn.heatmap(betastn_pivot, cmap=colors)

    plt.figure("Beta GPe")
    plt.title("Beta GPe")
    ax14 = seaborn.heatmap(betagpe_pivot, cmap=colors)

    plt.figure("Spectral Entropy STN")
    plt.title("Spectral Entropy STN")
    ax15 = seaborn.heatmap(specstn_pivot, cmap=colors)

    plt.figure("Spectral Entropy GPe")
    plt.title("Spectral Entropy GPe")
    ax16 = seaborn.heatmap(specgpe_pivot, cmap=colors)

    plt.figure("Sync. Parameter GPe A")
    plt.title("Sync. Parameter GPe A")
    ax17 = seaborn.heatmap(syncgpea_pivot, cmap=colors)

    plt.figure("Sync. Parameter GPe B")
    plt.title("Sync. Parameter GPe B")
    ax18 = seaborn.heatmap(syncgpeb_pivot, cmap=colors)

    plt.figure("Sync. Parameter GPe C")
    plt.title("Sync. Parameter GPe C")
    ax19 = seaborn.heatmap(syncgpec_pivot, cmap=colors)

    plt.figure("Sync. Parameter GPe")
    plt.title("Sync. Parameter GPe")
    ax20 = seaborn.heatmap(syncgpe_pivot, cmap=colors)

    plt.figure("Sync. Parameter STN RB")
    plt.title("Sync. Parameter STN RB")
    ax21 = seaborn.heatmap(syncstnrb_pivot, cmap=colors)

    plt.figure("Sync. Parameter STN LLRS")
    plt.title("Sync. Parameter STN LLRS")
    ax22 = seaborn.heatmap(syncstnllrs_pivot, cmap=colors)

    plt.figure("Sync. Parameter STN NR")
    plt.title("Sync. Parameter STN NR")
    ax23 = seaborn.heatmap(syncstnnr_pivot, cmap=colors)
    
    plt.figure("Sync. Parameter STN")
    plt.title("Sync. Parameter STN")
    ax24 = seaborn.heatmap(syncstn_pivot, cmap=colors)
    
    plt.show()

""" Report con tutte le mappe, con caratterizzazione di input CTX STR
    Che minchia succede?
    Link rilevanza parkinson (tipo cambiamento sulle beta, also sync)
"""