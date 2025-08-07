from flask import Flask, render_template
import redis
import os

app = Flask(__name__)

# Connect to Redis with fallback
redis_host = os.environ.get('REDIS_HOST', 'redis')
redis_port = int(os.environ.get('REDIS_PORT', 6379))

try:
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    # Test connection
    r.ping()
except redis.RedisError as e:
    print(f"Redis connection error: {e}")
    r = None

locations = [
    {
        "name": "Africa",
        "lat": 9.1,
        "lon": 18.2,
        "image": "africa.jfif",
        "info": "Africa is the world's second-largest and second-most populous continent."
    },
    {
        "name": "Europe",
        "lat": 54.5,
        "lon": 15.3,
        "image": "europe.jfif",
        "info": "Europe is known for its rich history, culture, and diverse landscapes."
    },
    {
        "name": "Asia",
        "lat": 34.0,
        "lon": 100.0,
        "image": "asia.jfif",
        "info": "Asia is the largest continent, home to diverse cultures and landscapes."
    },
    {
        "name": "Australia",
        "lat": -25.3,
        "lon": 133.8,
        "image": "australia.jfif",
        "info": "Australia is known for its unique wildlife and vast outback."
    },
    {
        "name": "America",
        "lat": 39.5,
        "lon": -98.35,
        "image": "america.jfif",
        "info": "America refers to both North and South America, diverse in nature and culture."
    },
    {
        "name": "South America",
        "lat": -14.2,
        "lon": -58.4,
        "image": "south_america.jfif",
        "info": "South America is known for the Amazon rainforest and Andes mountains."
    },
]

@app.route("/")
def index():
    pins = locations
    visit_count = 0
    visits_per_region = {}

    if r:
        try:
            r.incr("visit_count")
            for pin in pins:
                r.hincrby("visits_per_region", pin["name"], 1)
            visits_per_region = r.hgetall("visits_per_region") or {}
            visit_count = int(r.get("visit_count") or 0)
        except redis.RedisError as e:
            print(f"Redis error during request: {e}")
    else:
        print("Warning: Redis is not connected. Counts will not be updated.")

    center_lat = 20
    center_lon = 0

    return render_template(
        "index.html",
        pins=pins,
        visits_per_region=visits_per_region,
        center_lat=center_lat,
        center_lon=center_lon,
        visit_count=visit_count,
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)