import random
from scipy import stats

HV = 100000000
TF = 300

print("Ingrese cantidad de mesas (NM) y cantidad de lugares en la barra (NN):")
NM = int(input())
NB = int(input())

tpllm = 0
tpllb = 0
tpsm = [HV] * (NM)
tpsb = [HV] * (NB)

stom = [0] * (NM)
stob = [0] * (NB)

itom = [0] * (NM)
itob = [0] * (NB)

ptom = [0] * (NM)
ptob = [0] * (NB)

stllb = 0
stllm = 0

ms = 0
bs = 0

T = 0

stsm = 0
stsb = 0

stcm = 0
stcb = 0

mt = 0
bt = 0

tpem = 0
tpeb = 0

b2m = 0

pb2m = 0

def barra_libre():
    try:
        return tpsb.index(HV)
    except:
        return -1

def IAB():
    # foldcauchy distribution
    f_iab_c = 1.4989669253762021
    f_iab_loc = 2.9999999894637073
    f_iab_scale = 1.978240296417321
    return round(stats.foldcauchy.ppf(random.random(),  f_iab_c, loc=f_iab_loc, scale=f_iab_scale))

def IAM():
    #n cx2 distribution
    random_float = random.random()
    f2_df = 0.886551685942953
    f2_nc = 1.3962346932965461
    f2_loc = 0.9999999999999999
    f2_scale = 1.978240296417321
    return round(stats.ncx2.ppf(random_float, f2_df, f2_nc, loc=f2_loc, scale=f2_scale))

def mesa_libre():
    try:
        return tpsm.index(HV)
    except:
        return -1

def min_tpll():
    if tpllm <= tpllb:
        return tpllm, "mesa"
    else:
        return tpllb, "barra"
    

def min_tps():
    minm = min(tpsm)
    minb = min(tpsb)
    if minm <= minb:
        return minm, "mesa", tpsm.index(minm)
    else:
        return minb, "barra", tpsb.index(minb)
    

def TCB():
    f_tcb_loc = 16
    f_tcb_scale = 24
    return round(stats.uniform.ppf(random.random(),  f_tcb_loc, f_tcb_scale))

def TCM():
    f_tcm_a = 1.2906427065990094
    f_tcm_b = 0.9533143680120876
    f_tcm_loc = 51.390356168638924
    f_tcm_scale = 49.60964383136108
    return round(stats.beta.ppf(random.random(),  f_tcm_a, f_tcm_b, loc=f_tcm_loc, scale=f_tcm_scale))

# main
while True:
    while True:
        mintps, mintps_tipo, mintps_idx = min_tps()
        mintpll, mintpll_tipo = min_tpll()
        print("{} - {} - {} - {} - {} - {}".format(str(mintpll), mintpll_tipo,str(mintps),mintpll_tipo,str(ms),str(bs)))
        if mintpll <= mintps and mintpll != HV:
            if tpllm <= tpllb: # o mintps_tipo == "mesa"
                T = tpllm
                stllm = stllm + T
                iAM = IAM()
                # print(iAM)
                tpllm = T + iAM
                # print(tpllm)
                ms = ms + 1
                mt = mt + 1
                if ms <= NM: 
                    ML = mesa_libre()
                    tcm = TCM()
                    stcm = stcm + tcm
                    tpsm[ML] = T + tcm
                    stom[ML] = stom[ML] + (T - itom[ML])
            else:
                T = tpllb
                stllb = stllb + T
                iab = IAB()
                # print(iab)
                tpllb = T + iab
                bs = bs + 1
                if bs <= NB:
                    bt = bt + 1
                    BL = barra_libre()
                    tcb = TCB()
                    stcb = stcb + tcb
                    tpsb[BL] = T + tcb
                    stob[BL] = stob[BL] + (T - itob[BL])
                else:
                    if ms < NM:
                        b2m = b2m + 1
                        stllb = stllb - T
                        stllm = stllm + T
                        bs = bs - 1
                        ms = ms + 1
                        mt = mt + 1
                        ML = mesa_libre()
                        tcm = TCM()
                        stcm = stcm + tcm
                        tpsm[ML] = T + tcm
                        stom[ML] = stom[ML] + (T - itom[ML])
        else:
            if mintps_tipo == "barra":
                T = tpsb[mintps_idx]
                stsb = stsb + T
                bs = bs - 1
                if bs >= NB:
                    tcb = TCB()
                    stcb = stcb + tcb
                    tpsb[mintps_idx] = T + tcb
                else:
                    itob[mintps_idx] = T
                    tpsb[mintps_idx] = HV
            else:
                T = tpsm[mintps_idx]
                stsm = stsm + T
                ms = ms - 1
                if ms >= NM:
                    tcm = TCM()
                    stcm = stcm + tcm
                    tpsm[mintps_idx] = T + tcm
                else:
                    if bs > NB:
                        bs = bs - 1
                        b2m = b2m + 1
                        ms = ms + 1
                        tcm = TCM()
                        stcb = stcb + tcm
                        tpsm[mintps_idx] = T + tcm
                        stsb = stsb + T + tcm
                        stsm = stsm - (T + tcm)
                    else:
                        itom[mintps_idx] = T
                        tpsm[mintps_idx] = HV
        if T >= TF: break
    if ms <= 0 and bs <= 0: break
    tpllm = HV
    tpllb = HV
print("RESULTADOS")
print("==========")
print("Escenario: {} mesas y {} lugares en la barra. [BT: {} - MT: {}]".format(str(NM),str(NB),str(bt),str(mt)))
tpem = (stsm - stllm - stcm) / mt
print("TPEM: {:0.2f} minutos".format(tpem))
tpeb = (stsb - stllb - stcb) / bt
print("TPEB: {:0.2f} minutos".format(tpeb))
pb2m = (b2m/(b2m + bt)) * 100
print("PB2M: {:0.2f}%".format(pb2m))
for i in range(0, NM, 1):
    # para los no usados
    if stom[i] == 0 and itom[i] == 0:
        stom[i] = T
    ptom[i] = (stom[i] / T) * 100
    print("PTO Mesa {}: {:0.2f}%".format(str(i+1),ptom[i]))
for i in range(0, NB, 1):
    if stob[i] == 0 and itob[i] == 0:
        stob[i] = T
    ptob[i] = (stob[i] / T) * 100
    print("PTO Barra {}: {:0.2f}%".format(str(i+1),ptob[i]))
