import json, urllib.request, time, os

def get(url):
    r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(r, timeout=30))

old = {}
if os.path.exists("data.json"):
    old = json.load(open("data.json"))
d = {"meteo": old.get("meteo"), "ttwo": old.get("ttwo")}

try:
    d["meteo"] = get("https://api.open-meteo.com/v1/forecast?latitude=47.30&longitude=6.07&current=temperature_2m,apparent_temperature,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=Europe%2FParis&forecast_days=5")
except Exception as e:
    print("meteo", e)

try:
    y = get("https://query1.finance.yahoo.com/v8/finance/chart/TTWO?range=1mo&interval=1d")
    res = y["chart"]["result"][0]
    closes = [c for c in res["indicators"]["quote"][0]["close"] if c is not None]
    d["ttwo"] = {"price": res["meta"]["regularMarketPrice"], "series": closes}
except Exception as e:
    print("ttwo", e)

d["maj"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
json.dump(d, open("data.json", "w"))
