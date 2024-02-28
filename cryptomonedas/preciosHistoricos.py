import pandas as pd
#yahoo finance datos
import yfinance as yf
import matplotlib.pyplot as plt

factivos = open("activos", "r")
activos = factivos.read().splitlines()
factivos.close()

for i in activos:
    datos = yf.Ticker(i).history(period="max")#1y, 2y, 2m

    #precio de cierre y volumen del día
    precio = datos["Close"]
    volumen = datos["Volume"]

    plt.figure(figsize=(12,6))
    plt.plot(precio, label="")
    plt.show()
    