#IMPORTS#
import os
import requests
import json
import time

#SIMPLE MOVING AVG FUNCTION -- INCLUDES SHORT SELLING#
def SimpleMovingAvg (prices):
    i = 1
    buy = 0
    sell = 0
    position = 0
    total = 0
    buys = []
    
    for price in prices:
        if i > 5:
            Avg1 = (((prices[i-5]) + prices[i-4] + prices[i-3] + prices[i-2] + prices[i-1]) / 5)
    
            if price < Avg1 and position != 1:
                print("Buy:", price)
                buy = price
                buys.append(buy)
                if sell != 0 and buy != 0:
                    profit = sell - buy
                    profit = round(profit, 2)
                    total += profit
                    shortsell = price - buy
                    print("Trade profit:", round(shortsell,2))
                position = 1
                if i == len(prices) - 1:
                    print("Buy this today!")
            
            elif price > Avg1 and position != -1:
                sell = price
                print("Sell:", price)
                if sell != 0 and buy != 0:
                    profit = sell - buy
                    profit = round(profit, 2)
                    total += profit
                    shortsell = price - buy
                    print("Trade profit:", round(shortsell),2)
                position = -1
                if i == len(prices) - 1:
                    print("Sell this today!")
        
            else:
                pass
        i += 1
        
    print("----------------------------")
    print("Total Profit:", round(total,2))
    print("First Buy:", buys[0])
    print("Percentage Return:", round((total / buys[0])*100, 2), "%")
    
    return round(total,2), round((total / buys[0])*100, 2)
    
#MEAN REVERSION STRATEGY FUNCITON#
def MeanReversion (prices):
    i = 1
    buy = 0
    total = 0
    buys = []
    
    for price in prices:
        if i > 5:
            Avg2 = (((prices[i-5]) + prices[i-4] + prices[i-3] + prices[i-2] + prices[i-1]) / 5)
    
            if price < (Avg2 * 0.98) and buy == 0:
                print("Buy:", price)
                buy = price
                buys.append(buy)
                if i == len(prices) - 1:
                    print("Buy this today!")
            
            elif price > (Avg2 * 0.98) and buy != 0:
                profit = price - buy
                profit = round(profit, 2)
                total += profit
                print("Sell:", price)
                print("Trade profit:", profit)
                buy = 0
                if i == len(prices) - 1:
                    print("Sell this today!")
        
            else:
                pass
            
        i += 1
        
    print("----------------------------")
    print("Total Profit:", round(total,2))
    print("First Buy:", buys[0])
    print("Percentage Return:", round((total / buys[0])*100, 2), "%")
    
    return round(total,2), round((total / buys[0])*100, 2)

#BOLLINGER BAND STRATEGY FUNCITON#
def BollingerBandsAvg (prices):
    i = 1
    buy = 0
    total = 0
    buys = []
    
    for price in prices:
        if i > 5:
            try:
                Avg1 = (((prices[i-5]) + prices[i-4] + prices[i-3] + prices[i-2] + prices[i-1]) / 5)
    
                if price < (Avg1 * 1.05) and buy == 0:
                    print("Buy:", price)
                    buy = price
                    buys.append(buy)
            
                elif price > (Avg1 * 0.95) and buy != 0:
                    profit = price - buy
                    profit = round(profit, 2)
                    total += profit
                    print("Sell:", price)
                    print("Trade profit:", profit)
                    buy = 0
        
                else:
                    pass
            except:
                pass
        i += 1
        
    print("----------------------------")
    print("Total Profit:", round(total,2))
    print("First Buy:", buys[0])
    print("Percentage Return:", round((total / buys[0])*100, 2), "%")
    
    return round(total,2), round((total / buys[0])*100, 2)

#PULL DATA FROM WEB JSON API#
def CreateData(ticker):
    times_series_function = "TIME_SERIES_DAILY_ADJUSTED"
    time_interval = "365"
    output_size = "compact"
    api_key = "JJ6P7PSEA1F8K6BU"
    adj_key = "5. adjusted close"
    time_key = "Time Series (Daily)"
    
    url = ("https://www.alphavantage.co/query?function=" + times_series_function + "&symbol=" + ticker + "&interval=" + time_interval +"min&outputsize=" + output_size + "&apikey=" + api_key)
    req = requests.get(url)
    time.sleep(12)
    data_set = json.loads(req.text)
    
    prices = []
    csv_fil = open("/home/ubuntu/environment/final_project/data/" + ticker + ".csv","w")
    
    for data in data_set[time_key]:
        prices.append(data + "," + data_set[time_key][data][adj_key] + "\n")
        
    prices.reverse()
    
    for price in prices:
        csv_fil.write(price)
    return csv_fil.close()
    
#APPEND DATA FROM WEB JSON API -- ALPHAVANTAGE.com#
def AppendData(ticker):
    times_series_function = "TIME_SERIES_DAILY_ADJUSTED"
    time_interval = "7"
    output_size = "compact"
    api_key = "JJ6P7PSEA1F8K6BU"
    adj_key = "5. adjusted close"
    time_key = "Time Series (Daily)"
    
    url = ("https://www.alphavantage.co/query?function=" + times_series_function + "&symbol=" + ticker + "&interval=" + time_interval +"min&outputsize=" + output_size + "&apikey=" + api_key)
    req = requests.get(url)
    time.sleep(12)
    data_set = json.loads(req.text)
    
    prices = []
    csv_fil = open("/home/ubuntu/environment/final_project/data/" + ticker + ".csv","r")
    
    last_date = csv_fil.readlines()[-1].split(",")[0]
    csv_fil.close()
    
    for data in data_set[time_key]:
        if data > last_date:
            prices.append(data + "," + data_set[time_key][data][adj_key] + "\n")
        
    prices.reverse()
    
    csv_fil = open("/home/ubuntu/environment/final_project/data/" + ticker + ".csv","a")
    for price in prices:
        csv_fil.write(price)
    return csv_fil.close()
    
#SAVE RESULTS FUNCTION#
def SaveResults(insertDictionary):
    filePath = "/home/ubuntu/environment/final_project/results.json"
    json.dump(FinalDictionary, open(filePath, "w"),indent = 4)

#CHECK FOR MOST PROFITABLE STOCK/STRAT#
def ProfitRank(val1, val2, val3, HighestProfit, BestTickerStrat):
    if HighestProfit == 0:
        if Stored["TotalProfitMR"] > Stored["TotalProfitSA"]: 
            if Stored["TotalProfitMR"] > Stored["TotalProfitBB"]:
                HighestProfit = Stored["TotalProfitMR"]
                BestTickerStrat = ticker + " Mean Reversion"
                BestStrat.append(BestTickerStrat)
                BestStratProfit.append(HighestProfit)

        elif Stored["TotalProfitSA"] > Stored["TotalProfitMR"]: 
            if Stored["TotalProfitSA"] > Stored["TotalProfitBB"]:
                HighestProfit = Stored["TotalProfitSA"]
                BestTickerStrat = ticker + " Simple Moving Average"
                BestStrat.append(BestTickerStrat)
                BestStratProfit.append(HighestProfit)

        elif Stored["TotalProfitBB"] > Stored["TotalProfitMR"]:
            if Stored["TotalProfitBB"] > Stored["TotalProfitSA"]:
                HighestProfit = Stored["TotalProfitBB"]
                BestTickerStrat = ticker + " Bollinger Bands Average"
                BestStrat.append(BestTickerStrat)
                BestStratProfit.append(HighestProfit)

    elif HighestProfit != 0:
        if Stored["TotalProfitMR"] > Stored["TotalProfitSA"]:
            if Stored["TotalProfitMR"] > Stored["TotalProfitBB"]:
                if Stored["TotalProfitMR"] > HighestProfit:
                    HighestProfit = Stored["TotalProfitMR"]
                    BestTickerStrat = ticker + " Mean Reversion"
                    BestStrat.append(BestTickerStrat)
                    BestStratProfit.append(HighestProfit)
                else:
                    pass
            
        elif Stored["TotalProfitSA"] > Stored["TotalProfitMR"]:
            if Stored["TotalProfitSA"] > Stored["TotalProfitBB"]:
                if Stored["TotalProfitSA"] > HighestProfit:
                    HighestProfit = Stored["TotalProfitSA"]
                    BestTickerStrat = ticker + " Simple Moving Average"
                    BestStrat.append(BestTickerStrat)
                    BestStratProfit.append(HighestProfit)
                else:
                    pass
        
        elif Stored["TotalProfitBB"] > Stored["TotalProfitMR"]:
            if Stored["TotalProfitBB"] > Stored["TotalProfitSA"]:
                if Stored["TotalProfitBB"] > HighestProfit:
                    HighestProfit = Stored["TotalProfitBB"]
                    BestTickerStrat = ticker + " Simple Moving Average"
                    BestStrat.append(BestTickerStrat)
                    BestStratProfit.append(HighestProfit)
                else:
                    pass
                
    return
    
#LOOP THROUGH TICKERS, EXECUTE STRATEGIES, STORE STRATEGY RESULTS TO JSON FILE, BEST RESULTS#
tickers = ["AAPL", "ADBE","AMZN","BA","COST","CSCO","GOOG","MSFT","NVDA","TWTR"]
FinalDictionary = {}
BestStrat = []
BestStratProfit = []

for ticker in tickers:
    Stored = {}
    HighestProfit = 0
    BestTickerStrat = "nothing"
    CreateData(ticker)
    AppendData(ticker)
    tick = open("/home/ubuntu/environment/final_project/data/" + ticker + ".csv", "r")
    lines = tick.readlines()
    prices = []
    
    for line in lines:
        new_line = line.split(",")[1]
        prices.append(round(float(new_line),2))

    
    print(ticker, "Mean Reversion Strategy Output:")
    MRresults = MeanReversion(prices)

    Stored["TotalProfitMR"] = MRresults[0]
    Stored["PrecentReturnMR"] = MRresults[1]
    print("")
    
    print(ticker, "Simple Moving Average Strategy Output:")
    SAresults = SimpleMovingAvg(prices)
    Stored["TotalProfitSA"] = SAresults[0]
    Stored["PrecentReturnSA"] = SAresults[1]
    print("")
    
    print(ticker, "Bollinger Bands Average Strategy Output:")
    BBresults = BollingerBandsAvg(prices)
    Stored["TotalProfitBB"] = BBresults[0]
    Stored["PercentReturnBB"] = BBresults[1]
    print("")
    
    ProfitRank(Stored["TotalProfitMR"], Stored["TotalProfitSA"], Stored["TotalProfitBB"], HighestProfit, BestTickerStrat)
    
    FinalDictionary[ticker] = Stored
    
SaveResults(FinalDictionary)
print("The best strategy was " + BestStrat[-1] + " profiting $" + str(BestStratProfit[-1]))
