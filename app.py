
import requests, time
TOPIC="peshawar-board-bilal5900996"
def send(m,t="Signal"):
 requests.post(f"https://ntfy.sh/{TOPIC}",data=m.encode('utf-8'),headers={"Title":t,"Priority":"high"})
def get_rsi(p,period=14):
 if len(p)<period+1: return 50
 d=[p[i]-p[i-1] for i in range(1,len(p))]
 g=[x if x>0 else 0 for x in d]; l=[-x if x<0 else 0 for x in d]
 ag=sum(g[-period:])/period; al=sum(l[-period:])/period
 if al==0: return 100
 rs=ag/al; return 100-(100/(1+rs))
coins=["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","AVAXUSDT","DOTUSDT","LINKUSDT","TRXUSDT","MATICUSDT","LTCUSDT","SHIBUSDT","BCHUSDT","UNIUSDT","ATOMUSDT","ETCUSDT","XLMUSDT","FILUSDT","OKBUSDT","HBARUSDT","APTUSDT","ARBUSDT","NEARUSDT","QNTUSDT","VETUSDT","OPUSDT","MKRUSDT","GRTUSDT","AAVEUSDT","ALGOUSDT","EGLDUSDT","SANDUSDT","THETAUSDT","AXSUSDT","FLOWUSDT","XTZUSDT","MANAUSDT","EOSUSDT","KAVAUSDT","CHZUSDT","NEOUSDT","KLAYUSDT","ZILUSDT","ENJUSDT","IOTAUSDT","WAVESUSDT","ONEUSDT"]
send(f"15M SWEEP BOT LIVE {len(coins)} coins","LIVE")
for coin in coins:
 try:
  k=requests.get(f"https://api.binance.com/api/v3/klines?symbol={coin}&interval=15m&limit=50",timeout=10).json()
  highs=[float(x[2]) for x in k]; lows=[float(x[3]) for x in k]; closes=[float(x[4]) for x in k]; vols=[float(x[5]) for x in k]
  price=closes[-1]; rsi=get_rsi(closes)
  recent_high=max(highs[-21:-1]); recent_low=min(lows[-21:-1])
  curr_high=highs[-1]; curr_low=lows[-1]; curr_close=closes[-1]
  avg_vol=sum(vols[-20:])/20; vol_spike=vols[-1]/avg_vol if avg_vol>0 else 1
  ticker=requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={coin}",timeout=10).json()
  liq=float(ticker['quoteVolume'])
  if liq<10000000: continue
  sig=None
  if curr_high>recent_high and curr_close<recent_high and vol_spike>1.5:
   sig=f"💧 BUY SIDE SWEEP -> LONG!\n{coin} 15M\nSweep ${recent_high:.4f} -> ${curr_high:.4f}\nClose ${curr_close:.4f}\nRSI {rsi:.1f} Vol {vol_spike:.1f}x Liq ${liq/1000000:.1f}M\nENTRY ${price:.4f} TP ${price*1.02:.4f} SL ${curr_high*1.002:.4f}"
  elif curr_low<recent_low and curr_close>recent_low and vol_spike>1.5:
   sig=f"💧 SELL SIDE SWEEP -> LONG REVERSAL!\n{coin} 15M\nSweep ${recent_low:.4f} -> ${curr_low:.4f}\nClose ${curr_close:.4f}\nRSI {rsi:.1f} Vol {vol_spike:.1f}x Liq ${liq/1000000:.1f}M\nENTRY ${price:.4f}"
  if sig: send(sig,f"SWEEP {coin}")
  time.sleep(0.5)
 except Exception as e: print(e)
send("✅ 15M Sweep Scan Done","Done")
