import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt

index1 = "AMZN" # 아마존
index2 = "AAPL" # 애플
index3 = "005930.KS" # 삼성전자(코스피)
index4 = "068760.KQ" # 셀트리온제약(코스닥)

stockList = [] # 모든 종목 대해서는 미리 받아놓은 파일을 이용하는 것이 용이
stockList.append(index1)
stockList.append(index2)
stockList.append(index3)
stockList.append(index4)

start = dt.datetime(2015, 6, 21)
end = dt.datetime.now()

data = web.DataReader(index1, 'yahoo', start, end)
print(data)

closeData = data['Close']
print(closeData)

i = 0
for index in stockList:
    if i != 0:
        temp = web.DataReader(index, 'yahoo', start, end)['Close']
        closeData = pd.concat([closeData, temp], axis=1)
    i += 1
closeData.columns = stockList

print(closeData)

# 아예 dataframe들 list?
df_list = []
for index in stockList:
    temp = web.DataReader(index, 'yahoo', start, end)
    df_list.append(temp)
print(df_list)

# 클래스 및 백테스팅과 함께 활용???


# 데이터 클리닝 (합쳐진 상태에서 NaN 처리)

closeData.fillna(method='ffill')
print(closeData)
print(closeData.shape) # dimension을 의미 -> (1555, 4) = 1555 x 4 행렬

for i in range(1, closeData.shape[0]):
    for j in range(4): # 4 대신 closeData.shape[1] 가능!
        if np.isnan(closeData.values[i][j]):
            closeData.values[i][j] = closeData.values[i-1][j]

print(closeData)


# 이동평균선, 종가 LINE CHART 시각화

NQ = web.DataReader("^IXIC", "yahoo", "2016-01-01", end) # 나스닥
new_NQ = NQ[NQ['Volume'] !=0 ]

ma5 = new_NQ['Adj Close'].rolling(window=5).mean()
ma20 = new_NQ['Adj Close'].rolling(window=20).mean()
ma60 = new_NQ['Adj Close'].rolling(window=60).mean()
ma120 = new_NQ['Adj Close'].rolling(window=120).mean()

new_NQ.insert(len(new_NQ.columns), "MA5", ma5)
new_NQ.insert(len(new_NQ.columns), "MA20", ma20)
new_NQ.insert(len(new_NQ.columns), "MA60", ma60)
new_NQ.insert(len(new_NQ.columns), "MA120", ma120)

plt.plot(new_NQ.index, new_NQ['Adj Close'], label = 'Adj Close')
plt.plot(new_NQ.index, new_NQ['MA5'], label = 'MA5')
plt.plot(new_NQ.index, new_NQ['MA20'], label = 'MA20')
plt.plot(new_NQ.index, new_NQ['MA60'], label = 'MA60')
plt.plot(new_NQ.index, new_NQ['MA120'], label = 'MA120')

plt.legend(loc = "best")
plt.grid()
plt.show()


# Subplot 기능 기초

x = np.arange(0.0, 2*np.pi, 0.1)
sin_y = np.sin(x)
cos_y = np.cos(x)

fig = plt.figure()
ax1 = fig.add_subplot(2, 1, 1)
ax2 = fig.add_subplot(2, 1, 2)

ax1.plot(x, sin_y, 'b--')
ax2.plot(x, cos_y, 'r--')

ax1.set_xlabel('x')
ax1.set_ylabel('sin(x)')

ax2.set_xlabel('x')
ax2.set_ylabel('cos(x)')

plt.show()