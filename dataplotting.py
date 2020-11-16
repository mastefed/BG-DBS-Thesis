def firingrates(title, fr1, color1, fr2, color2, fr3, color3):
    plt.figure()
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whichis} [Hz]")
    plt.ylabel("CV")
    plt.plot(xaxis, fr1.values, color1)
    plt.plot(xaxis, fr2.values, color2)
    plt.plot(xaxis, fr3.values, color3)

def cvs(title, cv1, color1, cv2, color2, cv3, color3):
    plt.figure()
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whichis} [Hz]")
    plt.ylabel("Firing Rate [Hz]")
    plt.plot(xaxis, cv1.values, color1)
    plt.plot(xaxis, cv2.values, color2)
    plt.plot(xaxis, cv3.values, color3)

def sync(title, syn1, color1, syn2, color2, syn3, color3, syn4, color4):
    plt.figure()
    plt.title(title)
    plt.xlabel(f"Input Freq. Rate of {whichis} [Hz]")
    plt.ylabel("Sync. Value")
    plt.plot(xaxis, syn1.values, color1)
    plt.plot(xaxis, syn2.values, color2)
    plt.plot(xaxis, syn3.values, color3)
    plt.plot(xaxis, syn4.values, color4)

import matplotlib.pyplot as plt
import pandas
import argparse
from os import path

parser = argparse.ArgumentParser(description="Data Plotting script using .csv files")

parser.add_argument("filename", help="Name of the .csv file", type=str)
parser.add_argument("withrespectto", help="Plotting with respect to?", type=str, choices=["ctxrate","strrate"])
parser.add_argument("whattodo", help="What plot should I show?", type=str, choices=["firingrates","beta","cvs","syncs"])
parser.add_argument("-v", "--verbosity", action="count", help="shows what is going on")

args = parser.parse_args()

my_csv_file = args.filename
gen_path = "/home/fvm/Scrivania/"
final_path = path.join(gen_path, my_csv_file)
if args.verbosity == 1:
    print(f"Il percorso selezionato è {final_path}\n")

datas_from_csv = pandas.read_csv(final_path)

if args.verbosity == 1:
    print(f"Ecco i dati che hai appena importato:\n\n {datas_from_csv}\n")

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

if args.withrespectto == "ctxrate":
    xaxis = rateCTX.values
    whichis = "Cortex"
elif args.withrespectto == "strrate":
    xaxis = rateSTR.values
    whichis = "Striatum"

if args.whattodo == "firingrates":
    firingrates("F.R. GPe A (r) B (g) C (b)", frgpea, "r", frgpeb, "g", frgpec, "b")
    firingrates("F.R. STN RB (r) LLRS (g) NR (b)", frstnrb, "r", frstnllrs, "g", frstnnr, "b")
    plt.show()
elif args.whattodo == "cvs":
    cvs("Coeff. Var. GPe A (r) B (g) C (b)", cvgpea, "r", cvgpeb, "g", cvgpec, "b")
    cvs("Coeff. Var. STN RB (r) LLRS (g) NR (c)", cvstnrb, "r", cvstnllrs, "g", cvstnnr, "b")
    plt.show()
elif args.whattodo == "syncs":
    sync("Sync. Val. GPe A (r) B (g) C (b) All (k)", syncgpea, "r", syncgpeb, "g", syncgpec, "b", syncgpe, "k")
    sync("Sync. Val. STN RB (r) LLRS (g) NR (b) All (k)", syncstnrb, "r", syncstnllrs, "g", syncstnnr, "b", syncstn, "k")
    plt.show()
elif args.whattodo == "beta":
    plt.figure()
    plt.title("Beta % in PSD STN (r) GPe (g)")
    plt.xlabel(f"Input Freq. Rate of {whichis} [Hz]")
    plt.ylabel("Beta %")
    plt.plot(xaxis, betastn.values, "r")
    plt.plot(xaxis, betagpe.values, "g")
    plt.show()