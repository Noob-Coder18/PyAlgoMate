import math
from scipy.stats import norm
from scipy import optimize


def black_scholes_call(S, K, r, T, sigma):
    """
    Calculate the price of a European call option using the Black-Scholes formula.
    
    Parameters:
    S : float
        Current price of the underlying stock
    K : float
        Strike price of the option
    r : float
        Risk-free interest rate (annualized)
    T : float
        Time to expiration of the option (in years)
    sigma : float
        Volatility of the underlying stock's returns
    
    Returns:
    float
        Price of the European call option
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    
    return call_price


def black_scholes_put(S, K, r, T, sigma):
    """
    Calculate the price of a European put option using the Black-Scholes formula.
    
    Parameters:
    S : float
        Current price of the underlying stock
    K : float
        Strike price of the option
    r : float
        Risk-free interest rate (annualized)
    T : float
        Time to expiration of the option (in years)
    sigma : float
        Volatility of the underlying stock's returns
    
    Returns:
    float
        Price of the European put option
    """
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return put_price




def implied_volatility_call(S, K, r, T, market_price, sigma_est=0.25):

    def difference(sigma):
        return black_scholes_call(S, K, r, T, sigma) - market_price

# Using scipy's bisection method to find the root (i.e., implied sigma)
    try:
        implied_volatility = optimize.brentq(difference, 0.01, 5.0)
    except Exception as err:
        return 0

    return implied_volatility*100




def implied_volatility_put(S, K, r, T, market_price, sigma_est=0.25):

    
    
    def difference(sigma):
        return black_scholes_put(S, K, r, T, sigma) - market_price

    # Using scipy's bisection method to find the root (i.e., implied sigma)
    try:
        implied_volatility = optimize.brentq(difference, 0.01, 5.0)
    except Exception as err:
        return 0

    return implied_volatility*100


def calculate_theta_and_vega(S, K, r, T, sigma,opt_type):

    if sigma == 0:

        return math.nan,math.nan
    
    else:

        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

        d2 = d1 - sigma * math.sqrt(T)
        
        # Calculate Theta
        if opt_type == "c":
            
            theta = -(S * norm.pdf(d1) * sigma / (2 * math.sqrt(T))) - r * K * math.exp(-r * T) * norm.cdf(d2)
        
        elif opt_type == "p":
            
            theta = -(S * norm.pdf(-d1) * sigma / (2 * math.sqrt(T))) + r * K * math.exp(-r * T) * norm.cdf(-d2)
        
        # Calculate Vega
        vega = S * norm.pdf(d1) * math.sqrt(T)

        return vega/100,theta/365
