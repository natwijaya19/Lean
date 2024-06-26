# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from AlgorithmImports import *

from Selection.ManualUniverseSelectionModel import ManualUniverseSelectionModel
from Alphas.ConstantAlphaModel import ConstantAlphaModel
from Portfolio.InsightWeightingPortfolioConstructionModel import InsightWeightingPortfolioConstructionModel
from Execution.ImmediateExecutionModel import ImmediateExecutionModel

### <summary>
### Test algorithm using 'InsightWeightingPortfolioConstructionModel' and 'ConstantAlphaModel'
### generating a constant 'Insight' with a 0.25 weight
### </summary>
class InsightWeightingFrameworkAlgorithm(QCAlgorithm):

    def initialize(self):
        ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

        # Set requested data resolution
        self.universe_settings.resolution = Resolution.MINUTE

        # Order margin value has to have a minimum of 0.5% of Portfolio value, allows filtering out small trades and reduce fees.
        # Commented so regression algorithm is more sensitive
        #self.settings.minimum_order_margin_portfolio_percentage = 0.005

        self.set_start_date(2013,10,7)   #Set Start Date
        self.set_end_date(2013,10,11)    #Set End Date
        self.set_cash(100000)           #Set Strategy Cash

        symbols = [ Symbol.create("SPY", SecurityType.EQUITY, Market.USA) ]

        # set algorithm framework models
        self.set_universe_selection(ManualUniverseSelectionModel(symbols))
        self.set_alpha(ConstantAlphaModel(InsightType.PRICE, InsightDirection.UP, timedelta(minutes = 20), 0.025, None, 0.25))
        self.set_portfolio_construction(InsightWeightingPortfolioConstructionModel())
        self.set_execution(ImmediateExecutionModel())

    def on_end_of_algorithm(self):
        # holdings value should be 0.25 - to avoid price fluctuation issue we compare with 0.28 and 0.23
        if (self.portfolio.total_holdings_value > self.portfolio.total_portfolio_value * 0.28
            or self.portfolio.total_holdings_value < self.portfolio.total_portfolio_value * 0.23):
            raise ValueError("Unexpected Total Holdings Value: " + str(self.portfolio.total_holdings_value))
