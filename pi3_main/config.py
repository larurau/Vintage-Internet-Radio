# Mouse device configuration
MOUSE_VENDOR_ID = 1133
MOUSE_PRODUCT_ID = 49256
SPEED_ADJUSTMENT_FACTOR = 0.2

# WS2812 LED configuration:
LED_COUNT = 1
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 155  # 0 for dark, 255 for bright
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

LED_LOCKFILE = "/tmp/led_strip.lock"

# Initial position settings
INITIAL_POSITION_RANDOM = True
INITIAL_POSITION = 1000 # gets overwritten if INITIAL_POSITION_RANDOM is True
INBETWEEN_DISTANCE_MIN = 100
INBETWEEN_DISTANCE_MAX = 300
POSITION_CALCULATION_SEED = 42

# MPD ports
MPD_PORT_1 = 6600
MPD_PORT_2 = 6601

# Background noise file
BACKGROUND_NOISE_FILE = 'noise.mp3'

# Colors

COLOR_PERFECT_SELECT = 'Color(255,180,50)'
COLOR_NOISE = 'Color(255,194,50)'
COLOR_STARTUP = 'Color(255,224,50)'

# Channel list configuration
CHANNEL_LIST = [
    {
        "perfect_range": 50,
        "perception_range": 400,
        "name": "J-Pop Sakura",
        "stream_url": "https://cast1.torontocast.com:2170/;.mp3"
    },
    {
        "perfect_range": 40,
        "perception_range": 500,
        "name": "Hunter FM - LOFI",
        "stream_url": "https://live.hunter.fm/lofi_high"
    },
    {
        "perfect_range": 30,
        "perception_range": 600,
        "name": "Jazz Club Bandstand - 1930s 1940s Big Band and Swing",
        "stream_url": "https://cast1.torontocast.com:2060/;.mp3"
    },
    {
        "perfect_range": 20,
        "perception_range": 100,
        "name": "Noise Radio",
        "animation": "special_noise",
        "stream_url": "https://a5.asurahosting.com:7640/radio.mp3"
    },
    {
        "perfect_range": 40,
        "perception_range": 120,
        "name": "GDS.FM",
        "stream_url": "https://gdsfm.out.airtime.pro/gdsfm_a"
    },
    {
        "perfect_range": 30,
        "perception_range": 300,
        "name": "ChillHop",
        "stream_url": "https://fluxfm.streamabc.net/flx-chillhop-mp3-128-8581707"
    },
    {
        "perfect_range": 35,
        "perception_range": 300,
        "name": "WDR 3",
        "stream_url": "https://d131.rndfnk.com/ard/wdr/wdr3/live/mp3/256/stream.mp3?cid=01FBS0C9GMJJE2D5WXZHFQY7HG&sid=2mWCflOalLM9LXhKf9632QyAynQ&token=RsxqgsulZbSV98AQb66MyDowQSO6A2fgi4ppYtvFEB0&tvf=b0DuiHpD-BdkMTMxLnJuZGZuay5jb20"
    },
    {
        "perfect_range": 35,
        "perception_range": 300,
        "name": "Deutschlandfunk Kultur",
        "stream_url": "https://f121.rndfnk.com/ard/dlf/02/mp3/128/stream.mp3?cid=01FBPXKD7AYM1NKT2H60NVGHEQ&sid=2mWCZEPTLrnvCVr5CXeYuYIZNoa&token=GK3TlHWJEbi6GkJcRW_8IecgHtHwaAC8Akvp1Y3wDQg&tvf=8ICcaG5D-BdmMTIxLnJuZGZuay5jb20"
    },
    {
        "perfect_range": 60,
        "perception_range": 300,
        "name": "somafm - Deep Space One",
        "color": "(13,32,71)",
        "stream_url": "https://ice1.somafm.com/deepspaceone-128-mp3"
    },
    {
        "perfect_range": 90,
        "perception_range": 150,
        "name": "Shirley & Spinoza",
        "stream_url": "https://s2.radio.co/sec5fa6199/listen"
    },
    {
        "perfect_range": 70,
        "perception_range": 130,
        "name": "Salsa Son Timba",
        "stream_url": "https://cast1.my-control-panel.com/proxy/salsason/stream"
    },
    {
        "perfect_range": 45,
        "perception_range": 130,
        "name": "France Culture",
        "stream_url": "https://icecast.radiofrance.fr/franceculture-midfi.mp3"
    },
    {
        "perfect_range": 80,
        "perception_range": 200,
        "name": "Vintage Obscura Radio",
        "stream_url": "https://radio.vintageobscura.net/stream"
    },
    {
        "perfect_range": 35,
        "perception_range": 300,
        "name": "SWR Kultur (2)",
        "stream_url": "https://f121.rndfnk.com/ard/swr/swr2/live/mp3/256/stream.mp3?aggregator=web&cid=01FC1X4J91VJW1CVH6588MZEE3&sid=2mWCTENJOjSpFHrtCyXO12GYj5P&token=JlsPrW_sd6CUvvkGSE4RYHJioljaLUU2bUFtr2ZhhsE&tvf=0ZKCLWND-BdmMTIxLnJuZGZuay5jb20"
    },
    {
        "perfect_range": 20,
        "perception_range": 100,
        "name": "NOAA Weather Radio KIG-86, Columbus, Ohio",
        "color": "(231,195,235)",
        "stream_url": "https://radio.weatherusa.net/NWR/KIG86.mp3"
    },
    {
        "perfect_range": 50,
        "perception_range": 400,
        "name": "Retro PC Game Music Streaming Radio for Gyusyabu",
        "stream_url": "http://gyusyabu.ddo.jp:8000/;stream.mp3"
    },
    {
        "perfect_range": 100,
        "perception_range": 200,
        "name": "ashiya.radio",
        "stream_url": "https://s3.radio.co/sc8d895604/listen"
    },
    {
        "perfect_range": 60,
        "perception_range": 160,
        "name": "Capital Salsa",
        "stream_url": "https://stream.integracionvirtual.com/proxy/capitalsalsa?mp=/stream"
    },
    {
        "perfect_range": 70,
        "perception_range": 400,
        "name": "Arctic Outpost AM1270 -Direct Air Monitor",
        "color": "(14,46,45)",
        "stream_url": "http://radio.streemlion.com:3710/stream"
    },
    {
        "perfect_range": 50,
        "perception_range": 350,
        "name": "somafm - Vaporwaves",
        "stream_url": "https://ice6.somafm.com/vaporwaves-128-mp3"
    },
    {
        "perfect_range": 60,
        "perception_range": 350,
        "name": "Bloop, London Radio",
        "stream_url": "https://radio.canstream.co.uk:8058/live.mp3"
    },
    {
        "perfect_range": 30,
        "perception_range": 240,
        "name": "Ancient FM",
        "stream_url": "https://mediaserv73.live-streams.nl:18058/stream"
    },
    {
        "perfect_range": 35,
        "perception_range": 300,
        "name": "Deutschlandfunk",
        "stream_url": "https://d121.rndfnk.com/ard/dlf/01/mp3/128/stream.mp3?cid=01FBPWZ12X2XN8SDSMBZ7X0ZTT&sid=2mWCGxOqJS2HPJnb7UkwMBfc7Ty&token=wphjA721LWy4ikf-vdk9bxj75JvHGdb3j_8HS5ARMio&tvf=fS5MSkxD-BdkMTIxLnJuZGZuay5jb20"
    },
    {
        "perfect_range": 45,
        "perception_range": 100,
        "name": "Dr Dick's Dub Shack",
        "stream_url": "https://streamer.radio.co/s0635c8b0d/listen"
    },
    {
        "perfect_range": 50,
        "perception_range": 150,
        "name": "Nostalgie - Le Plus Grands Tubes Francais",
        "stream_url": "https://scdn.nrjaudio.fm/fr/30705/mp3_128.mp3?origine=radiogarden&cdn_path=adswizz_lbs10&adws_out_3&access_token=26d8df4e108c4d0ebae0e07d0d222d82"
    },
    {
        "perfect_range": 40,
        "perception_range": 440,
        "name": "Nonstop Casiopea",
        "stream_url": "https://nonstopcasiopea.radioca.st/;"
    },
    {
        "perfect_range": 35,
        "perception_range": 300,
        "name": "Nordic Lodge Copenhagen",
        "stream_url": "http://radio.streemlion.com:1160/stream"
    },
    {
        "perfect_range": 20,
        "perception_range": 120,
        "name": "Spinning seal FM",
        "animation" : "rainbow",
        "stream_url": "https://stream-153.zeno.fm/9q3ez3k3fchvv?zt=eyJhbGciOiJIUzI1NiJ9.eyJzdHJlYW0iOiI5cTNlejNrM2ZjaHZ2IiwiaG9zdCI6InN0cmVhbS0xNTMuemVuby5mbSIsInJ0dGwiOjUsImp0aSI6InFYeTZZdEZQU2hDTVN3ampEbUtvM3ciLCJpYXQiOjE3MjcwMTY4MDksImV4cCI6MTcyNzAxNjg2OX0.aeG5_KZQwVg_ImMkX6s-5ly83pua1F-tMMcY0VuDmoM"
    },
]