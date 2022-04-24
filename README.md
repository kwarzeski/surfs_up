# Surf's Up
## Overview
The purpose of this data analysis is to review temperature data for June and December in Oahu to determine if a surf and ice cream shop business is sustainable year-round.

## Results:
- Maximum and Minimum temperatures in June are higher (64 and 85 vs 56 and 83)
- Average temperature in June is higher (74.94 vs 71.04)
- December temperature range (difference between max and minimum) is greater than June (21 vs 27)

## Summary:
The minimum temperature found in December is 56 and the average temperature is 71, indicating good demand for ice cream and surfing. Temperatures should also be checked for January and February.
- Additional Query 1: session.query(Measurement.tobs).filter(extract('month', Measurement.date)==1).all()
- Additional Query 2: session.query(Measurement.tobs).filter(extract('month', Measurement.date)==2).all()
