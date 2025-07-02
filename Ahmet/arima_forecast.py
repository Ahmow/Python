import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from statsmodels.tsa.stattools import adfuller
from Ahmet.user_request import get_data_from_sql
import datetime as dt
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import seaborn as sns
from statsmodels.stats.diagnostic import acorr_ljungbox


################################         1            #########################################################
#Augmented dickey fuller test - Wir schauen, ob unsere Daten stationär sind.
#stationär = Die statistischen Eigenschaften (Mittelwert, Varianz, Autokorrelation) 
#der Zeitreihe ändern sich im Zeitverlauf nicht.

start_dt = dt.datetime(2024, 3, 3)
end_dt =dt.datetime(2025, 3, 23) # FRAGE: Habe versucht es aus den anderen Codes zuziehen. Wie macht man es?

df= get_data_from_sql(start_dt , end_dt , symbol='MSFT')
adf= df["close"]

################### wie der erste versuch(siehe unten) nur eine schleife (differenzierung) ######################

def make_stationary(adf, max_diff=3):
    d=0
    while d < max_diff:
        result = adfuller(adf)#--> adfuller ist eine tupel mit 6 Elementen -->siehe result unter strg+click auf adfuller
        if result[1] < 0.05:
            print(f"Stationör nach {d} Differenzierung(en)")
            return adf, d
        adf = adf.diff().dropna()
        d = d + 1
    print( "nicht stationär trotz mehrfacher Differenzierugen")
    return adf, d

adf_stationary, d_used = make_stationary(adf)
print(f"Verwendete Differenzierung: {d_used}")

###########################       2        ##############################################################

# Parameter Estimation (Parameterschätzung)
# Fit das Modell: Nutze z.B. model.fit() in Python, um die Parameter zu schätzen.
# Ziel: Bestimme die Werte für p, d, q, die die Daten am besten erklären.

plot_acf(adf_stationary) #ACF (Autokorrelationsfunktion) 
plot_pacf(adf_stationary) #PACF (partielle Autokorrelationsfunktion)
plt.show()
plt.pause(5)           
plt.close() 

#Wir wollen ein ARIMA-Modell bauen. Dafür brauchen wir ():

# p = wie viele vergangene Werte beeinflussen den heutigen Wert? = 2
# Wenn heute mit gestern und gestern mit vorgestern stark zusammenhängt, prüft PACF:
# „Gibt es wirklich einen direkten Zusammenhang zwischen heute und vorgestern, oder ist das nur eine 
# indirekte Kette über gestern?“

# q = wie viele vergangene Fehler beeinflussen den heutigen Wert? =
# Wenn heute (Lag 0) stark mit gestern (Lag 1) korreliert ist, und gestern wiederum mit vorgestern (Lag 2), 
# dann zeigt ACF auch eine Korrelation mit Lag 2, auch wenn die gar nicht direkt ist.

# Mithilfe des oben beschriebenen Codes, kann man ein Diagramm erstellen lassen, welches aufzeigt, wie hoch p und q sind
# das heißt, wie viele Korrelationen sind signifikant.


############################          3       ##########################################################
#Model Checking (Modellüberprüfung)
# Residualanalyse: Prüfe die Residuen (Fehler) des Modells.
# Ziel:
# Die Residuen sollten wie „weißes Rauschen“ aussehen, also keine Autokorrelation aufweisen.
# Nutze Tests wie Ljung-Box-Test, um Autokorrelation in den Residuen zu prüfen.
# Überprüfe, ob das Modell alle Strukturen der Zeitreihe erfasst hat.

# Modell erstellen mit (p=2, d=1, q=2)
model= ARIMA(adf, order =(2, 1, 2))

model_fit =  model.fit() #passt das ARIMA-Modell an meine Daten an.

print(model_fit.summary())

# Erklärung vom print:
# coef: Der geschätzte Wert des jeweiligen Parameters (AR (autoregressive) oder MA(moving average))
# P>|z|: Wenn kleiner als 0.05, dann ist der Parameter statistisch signifikant
# [0.025, 0.975]: 95%-Konfidenzintervall
# Ljung-Box (Q) → Test auf Autokorrelation der Residuen
# p > 0.05: gut → Residuen sind unkorreliert
# Jarque-Bera (JB) → Test auf Normalverteilung der Residuen
# p > 0.05: gut → Residuen normalverteilt



#Residuen prüfen

residals = model_fit.resid

# plot residuen

plt.figure(figsize=(12,8))
plt.subplot(2, 2, 1)
plt.plot(residals)
plt.title("Residuen")


plt.subplot(2, 2, 2)
sns.histplot(residals, bins=30, kde=True)#bins=teilt den Bereich der Residuen in 30 Intervalle („Kästchen“) ein, 
#KDE= Kern-Dichteschätzung
plt.title("Histogramm der Residuen")

# ACF der Residuen (sollte KEINE Signifikanz zeigen)
plt.subplot(2, 1, 2)
plot_acf(residals, ax=plt.gca(), lags=40)
plt.title("ACF der Residuen")

# Ljung-Box-Test
lb_test = acorr_ljungbox(residals, lags=[10], return_df=True)
print("\nLjung-Box-Test:")
print(lb_test)

plt.tight_layout()
plt.subplots_adjust(hspace=0.4, wspace=0.4)
plt.show()


########################   ERSTER VERSUCH ################################
# adf= df["close"]
# result= adfuller(adf) #--> adfuller ist eine tupel mit 6 Elementen -->siehe result unter strg+click auf adfuller
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])
# print('Critical Values:', result[4])

# if result[1] < 0.05:
#     print("Die Zeitreihe ist wahrscheinlich stationär.")
# else:
#     adf_diff= adf.diff().dropna() 
#     #testen, ob der differenzierte Wert stationär ist
#     result_diff = adfuller(adf_diff)
#     print('ADF Statistic nach 1. Differenzierung:', result_diff[0])
#     print('p-value (diff):', result_diff[1])
#     print('Critical Values(diff):', result_diff[4])
#     if result_diff[1] < 0.05:
#         print("Die differenzierte Zeitreihe ist jetzt stationär.")
#     else:
#         print("Auch nach der Differenzierung ist die Zeitreihe nicht stationär – evtl. zweite Differenz nötig.")

