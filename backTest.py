# param
starting_wallet = 1000
amount_stocks = 0
number_deals = 0
number_winning = 0
winnings_list = []
losses_list = []
sum_win = 0
sum_loss = 0

smoothing_30 = 2 / (30 + 1)
smoothing_90 = 2 / (90 + 1)
canBuy = True
canSell = False

# TODO foreach all the files for the different stocks - enlist some stuff



def buy_func(starting_wallet, price):
    amount_stocks = starting_wallet / float(price)
    return amount_stocks


def sell_func(amount_stocks, price):
    starting_wallet = amount_stocks * float(price)
    return starting_wallet


with open('XBTUSD.csv', 'r') as csv_file:
    data_list = csv_file.readlines()
    data_list = (data_list[1:])
    data_list.reverse()
    csv_file.close()
    ema_now_30 = float(data_list[0][32:]) * smoothing_30 
    ema_now_90 = float(data_list[0][32:]) * smoothing_90

for line in data_list:

    ema_past_30 = ema_now_30
    ema_now_30 = (float(line.rstrip()[32:]) - ema_past_30) * smoothing_30 + ema_past_30

    ema_past_90 = ema_now_90
    ema_now_90 = (float(line.rstrip()[32:]) - ema_past_90) * smoothing_90 + ema_past_90

    if canBuy:
        if ema_now_30 > ema_past_30:  # check if increasing
            if ema_past_30 < ema_past_90 and ema_now_30 > ema_now_90:  # check if crossing
                amount_stocks = buy_func(starting_wallet, line.rstrip()[32:])
                number_deals += 1
                canBuy = False
                canSell = True

    if canSell:
        if ema_now_30 < ema_past_30:  # check if decreasing
            if ema_past_30 > ema_past_90 and ema_now_30 < ema_now_90:  # check if crossing
                temp = starting_wallet
                starting_wallet = sell_func(amount_stocks, line.rstrip()[32:])
                canBuy = True
                canSell = False

                number_deals += 1
                if starting_wallet - temp > 0:
                    number_winning += 1
                    winnings_list.append(starting_wallet - temp)
                    sum_win += starting_wallet - temp
                else:
                    losses_list.append(starting_wallet - temp)
                    sum_loss += starting_wallet - temp


# Output should be profit, number of deals (buys + sells), winners% and losers%
print("The profit is: ", starting_wallet - 1000)
print("The number of deals is: ", number_deals)
print("The number of winning buy/sell deals is: ", number_winning)
print("The overall winnings and losses are: ", sum_win, sum_loss)
print("The average winning from a buy/sell deal is: ", sum_win / len(winnings_list))
print("The average loss from a buy/sell deal is: ", sum_loss / len(losses_list))
