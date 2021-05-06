def get_size(self, riskSize):
    assetClass = self.p.assetClass
    if assetClass == 'CFD':
        defaultSize = 1
        pipsLost = int(riskSize * defaultSize)
    elif assetClass == 'Forex':
        defaultSize = 100000
        pipsLost = round(riskSize * defaultSize, 4)


    if self.p.compound:
        loss = (self.cash * self.p.max_loss / 100)
    else:
        loss = (self.p.initial_cash * self.p.max_loss / 100)
    ratio = loss / pipsLost
    size = defaultSize * ratio
    if size / defaultSize > 100:
        return 100 * defaultSize
    rounded = round(size, 4)
    # return size
    return rounded
