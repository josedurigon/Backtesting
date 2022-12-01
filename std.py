from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override()

import pandas as pd
import numpy as np

from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import base_optimizer

import vectorbt as vbt

# Define os ativos e o período do benchmark
ticker = ["VALE3.SA", "BBDC4.SA", "ITSA4.SA"]
start = "2016-01-01"
end = "2022-01-21"

# Importa os ativos

ohlc = pdr.get_data_yahoo(ticker, start = start, end = end)

# Extrai os preços de fechamento

prices = ohlc['Close']

# Calcula os retornos

returns = prices.vbt.to_returns()

# Importa o benchmark (Ibovespa)

bench = pdr.get_data_yahoo(['^BVSP'], start = start, end = end)

# Extrai os dados de fechamento

bench_ret = bench['Close'].vbt.to_returns()

# Calcula o retorno esperado

expec_return = expected_returns.mean_historical_return(prices)

# Calcula a matriz de covariância

cov_mat = risk_models.sample_cov(prices)

# Calcula a fronteira eficiente

ef = EfficientFrontier(expec_return, cov_mat)

# Obtém os pesos ótimos minimizando a volatilidade do portfolio

w = ef.min_volatility()

# Manipula e limpa o array dos pesos

clean_weights = ef.clean_weights()

pyopt_weights = np.array([clean_weights[symbol] for symbol in ticker])

pyopt_size = np.full_like(prices, np.nan)

pyopt_size[0, :] = pyopt_weights

# Utiliza o vectorbt para construir um objeto de ordens com base no portfólio

pyopt_pf = vbt.Portfolio.from_orders(
    close = prices,
    size = pyopt_size,
    size_type = 'targetpercent',
    group_by = True,
    cash_sharing = True
)

# Principais indicadores de backtesting
print(pyopt_pf.stats(settings = dict(benchmark_rets = bench_ret)))

# Plota os principais gráficos

pyopt_pf.plot(
    subplots = 'all'
    ).show()
