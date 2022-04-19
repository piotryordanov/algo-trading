from datetime import datetime

# pylint: disable-all
## Internal
index = 1
Assets = ["US30240", "EURUSD240", "AUDUSD240"]
assetClass = ["CFD", "Forex", "Forex"]

# Asset
Asset = Assets[index]
AssetClass = assetClass[index]
# FromDate = datetime(2016, 1, 1)
# ToDate = datetime(2018, 5, 1)

FromDate = datetime(2021, 10, 5)
ToDate = datetime(2021, 10, 7)

# Trade Management
Max_Loss = 5
Max_Lot = 100
Compound = True
Initial_Cash = 10000
Trades_Direction = 1  # 1: Both - 2: Long - 3: Short
One_Position_Per_Time = False

# Trail Management
TakeOnTarget = False

Use_Trail_Stop = True
ATRMultiplier = 4
TrailType = "ATR"  # "Combined", "Fractal", "ATR"

Use_RR_Stop = True
RR_Trail_Amount = 4
RR_Trail_Post_Target = RR_Trail_Amount
RR_StopToScratch = 3

Use_Bounce = False

PlotTrail = False

### ==================== ###
###   Fractal Strategy   ###
### ==================== ###
Fractal_Left_Shift = 30
Fractal_Right_Shift = 7
