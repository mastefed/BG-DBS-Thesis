def firingrates(title, fr1, color1, fr2, color2, fr3, color3):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Firing Rate [Hz]")
    plt.plot(xaxis, fr1.values[i*span:(i+1)*span], color1)
    plt.plot(xaxis, fr2.values[i*span:(i+1)*span], color2)
    plt.plot(xaxis, fr3.values[i*span:(i+1)*span], color3)

def cvs(title, cv1, color1, cv2, color2, cv3, color3):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("CV")
    plt.plot(xaxis, cv1.values[i*span:(i+1)*span], color1)
    plt.plot(xaxis, cv2.values[i*span:(i+1)*span], color2)
    plt.plot(xaxis, cv3.values[i*span:(i+1)*span], color3)

def sync(title, syn1, color1, syn2, color2, syn3, color3, syn4, color4):
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Sync. Value")
    plt.plot(xaxis, syn1.values[i*span:(i+1)*span], color1)
    plt.plot(xaxis, syn2.values[i*span:(i+1)*span], color2)
    plt.plot(xaxis, syn3.values[i*span:(i+1)*span], color3)
    plt.plot(xaxis, syn4.values[i*span:(i+1)*span], color4)

import matplotlib.pyplot as plt
import pandas
import argparse
from os import path

parser = argparse.ArgumentParser(description="Data Plotting script using .csv files")

parser.add_argument("filename", help="Name of the .csv file", type=str)
parser.add_argument("fixwhat", help="What frequencies to lock?", type=str, choices=["ctxrate","strrate"])
parser.add_argument("whattodo", help="What plot should I show?", type=str, choices=["firingrates","beta","cvs","syncs"])
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
    firingrates("F.R. GPe A (r) B (g) C (b)", frgpea, "r", frgpeb, "g", frgpec, "b")
    plt.figure(2)
    firingrates("F.R. STN RB (r) LLRS (g) NR (b)", frstnrb, "r", frstnllrs, "g", frstnnr, "b")
    plt.show()
elif args.whattodo == "cvs":
    plt.figure(1)
    cvs("Coeff. Var. GPe A (r) B (g) C (b)", cvgpea, "r", cvgpeb, "g", cvgpec, "b")
    plt.figure(2)
    cvs("Coeff. Var. STN RB (r) LLRS (g) NR (c)", cvstnrb, "r", cvstnllrs, "g", cvstnnr, "b")
    plt.show()
elif args.whattodo == "syncs":
    plt.figure(1)
    sync("Sync. Val. GPe A (r) B (g) C (b) All (k)", syncgpea, "r", syncgpeb, "g", syncgpec, "b", syncgpe, "k")
    plt.figure(2)
    sync("Sync. Val. STN RB (r) LLRS (g) NR (b) All (k)", syncstnrb, "r", syncstnllrs, "g", syncstnnr, "b", syncstn, "k")
    plt.show()
elif args.whattodo == "beta":
    plt.figure(1)
    plt.title("Beta % in PSD STN (r) GPe (g)")
    plt.xlabel(f"Input Freq. Rate of {whatx} [Hz]")
    plt.ylabel("Beta %")
    plt.plot(xaxis, betastn.values[i*span:(i+1)*span], "r")
    plt.plot(xaxis, betagpe.values[i*span:(i+1)*span], "g")
    plt.show()