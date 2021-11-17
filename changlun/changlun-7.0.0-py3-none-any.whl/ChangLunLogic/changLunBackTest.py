from ChangLunLogic.ChangLun import ChangLun

def getHistTradeFeatures(df,windows=250):
    featureList = []
    if len(df) < 250:
        return []
    for i in range(len(df)-windows+1):
        tempDf = df.iloc[i:i+windows]
        model = ChangLun(tempDf,'D','M')
        isRun = model.run(True)
        if not isRun:
            continue
        isBuy = model.isPenBuyPoint()
        if not isBuy:
            continue
        feature = model.genFeature()
        if len(feature) == 0:
            continue
        featureList.append(feature)
    featureList = markFeautures(featureList,df)
    return featureList

def markFeautures( featureList, df ):
    if featureList is None or len(featureList) == 0:
        return []
    model = ChangLun(df,'D','M')
    model.run()
    lastPen = model.penList[-1]
    penSet = set([x['endDate'] for x in model.penList[0:-1]])
    for feature in featureList:
        penEndDate = feature['pen_end_date']
        isTruePen = penSet.__contains__(penEndDate)
        feature['label_is_pen_true'] = isTruePen
        feature['label_is_last_pen'] = (penEndDate == lastPen['endDate'])
    return featureList
