from datetime import date
import math

def pricing_contract(in_dates, with_dates, pur_prices, sell_prices, in_rate, 
                     total_vol, store_rate, iwcr):
    """
    Calculates the value of a commodity storage contract.

    Parameters:
    - in_dates: List of injection dates
    - with_dates: List of withdrawal dates
    - pur_prices: List of purchase prices corresponding to injection dates
    - sell_prices: List of selling prices corresponding to withdrawal dates
    - in_rate: Rate of which commodity can be injected 
    - total_vol: Total volume of commodity that can be stored 
    - store_rate: Monthly rate of storage cost 
    - iwcr: Rate of cost for injection/withdrawal

    Returns the value of a contract in dollars.
    """

    # initalizing variables
    volume = 0
    total_cost = 0
    last_transaction_date = min(min(in_dates), min(with_dates))

    # combine and sort all transaction dates
    all_dates = sorted(set(in_dates + with_dates))

    # iterate through all transaction dates
    for current_date in all_dates:
        # check if current_date is in in_dates 
        if current_date in in_dates:
            # check if there is space for injection
            if volume <= total_vol - in_rate:
                # increased stored volume
                volume += in_rate

                # calculate cost to purchase gas and the injection cost
                purchase_price = pur_prices[in_dates.index(current_date)]
                purchase_cost = in_rate * purchase_price
                injection_cost = in_rate * iwcr

                # add purchase cost and injection cost to total cost
                total_cost += purchase_cost + injection_cost
                print(f"Injected gas on {current_date} at a price of {purchase_price}")
            else:
                print(f"Injection is not possible on {current_date} due to insufficient storage space")
        
        elif current_date in with_dates:
            # check if there is enough gas to withdraw
            if volume >= in_rate:
                # decrease the stored volume
                volume -= in_rate

                # calculate revenue from gas withdrawal and withdrawal cost
                withdrawal_price = sell_prices[with_dates.index(current_date)]
                withdrawal_revenue = in_rate * withdrawal_price
                withdrawal_cost = in_rate * iwcr

                # subtract withdrawal cost from total cost 
                total_cost += withdrawal_revenue - withdrawal_cost
                print(f"Extracted gas on {current_date} at a price of {withdrawal_price}")
            else:
                print(f"Extraction is not possible on {current_date} due to insufficient gas volume")
    
    # calculate storage cost based on difference between first injection and last withdrawal
    storage_cost = math.ceil((max(with_dates) - min(in_dates)).days // 30) * store_rate

    # add storage cost to total cost
    total_cost += storage_cost
    return total_cost

# example usage
in_dates = [date(2023, 10, 1), date(2023, 11, 1)]
with_dates = [date(2024, 4, 1), date(2024, 6, 1)]
pur_prices = [2.0, 2.2]
sell_prices = [3.0, 3.5]
in_rate = 1000
total_vol = 500000
storage_rate = 1000
iwcr = 0.0005

result = pricing_contract(in_dates, with_dates, pur_prices, sell_prices, in_rate, 
                          total_vol, storage_rate, iwcr)
print(f"The value of the natural gas storage contract is: ${result}")
