#pip install TA-Lib
import pandas as pd
#yahoo finance datos
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

factivos = open("activos", "r")
activos = factivos.read().splitlines()
factivos.close()

datos = pd.DataFrame()
datos = yf.Ticker("BTC-USD").history(period="max")#1y, 2y, 2m

print(datos)

# Precio de cierre y volumen del día
precio = datos["Close"]
volumen = datos["Volume"]


# Media Móvil simple de 30 periodos
MV30 = pd.DataFrame()
MV30['Close'] = datos['Close'].rolling(window=30).mean()# Calculo media al periodo de 30
print("Media movil simple de 30 periodos: ", MV30.index==29)
# Media movil simple de 30 periodos
MV100 = pd.DataFrame()
MV100['Close'] = datos['Close'].rolling(window=100).mean()# Calculo media al periodo de 30
print("Media movil simple de 100 periodos: ", MV100==29)

# Grafica de la Media Movil simple de 30 periodos
plt.figure(figsize=(12,6))
plt.plot(datos['Close'], label="BTC-USD")
plt.plot(MV30['Close'], label="Media móvil 30")
plt.plot(MV100['Close'], label="Media móvil 100")
plt.title('Bitcoin vs. USD')
plt.xlabel('17/09/2014  -  22/12/2023')
plt.ylabel('USD')
plt.legend(loc = 'upper left')
#plt.show()

# Precios de cierre de Media Móvil
data = pd.DataFrame()
data['BTC-USD'] = datos['Close']
data['MV30'] = MV30['Close']
data['MV100'] = MV100['Close']
print(data)


def senal(data):
    compra = []
    venta = []
    condicion = 0 # Bandera para saber choque de Medias Móviles
    
    for dia in range(len(data)):
        if data['MV30'][dia] > data['MV100'][dia]:
            if condicion != 1:
                compra.append(data['BTC-USD'][dia]) # Condicion de compra
                venta.append(np.nan) # Si compramos no vvamos a vender
                condicion = 1
            else:
                compra.append(np.nan)
                venta.append(np.nan)
        elif data['MV30'][dia] < data['MV100'][dia]:
            if condicion != -1:
                venta.append(data['BTC-USD'][dia]) # Condicion de venta
                compra.append(np.nan) # Si vendemos no vamos a comprar
                condicion = -1
            else:
                compra.append(np.nan)
                venta.append(np.nan)
        else:
            compra.append(np.nan)
            venta.append(np.nan)
            condicion = 0
    return (compra, venta)

senales = senal(data)
#print(senales)
data['Compra'] = senales[0]
data['Venta'] = senales[1]
print(data)

# Grafico con senales de compra y venta
plt.figure(figsize=(12,6))
plt.plot(data['BTC-USD'], label="BTC-USD", alpha=0.3)
plt.plot(data['MV30'], label="Media Movil 30" , alpha=0.3)
plt.plot(data['MV100'], label="Media Movil 100" , alpha=0.3)
plt.scatter(x=data.index, y=data['Compra'], label="Precio de Compra", marker='^', color='green', alpha=1) 
plt.scatter(x=data.index, y=data['Venta'], label="Precio de Venta", marker='v', color='red', alpha=1)
plt.title('Bitcoin vs. USD')
plt.show()