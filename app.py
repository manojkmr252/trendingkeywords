from flask import Flask, request, jsonify
from pytrends.request import TrendReq
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/trending_keywords', methods=['GET'])
def get_trending_keywords():
    topic = request.args.get('query')
    if not topic:
        return jsonify({"error": "No query provided"}), 400

    pytrends.build_payload([topic], timeframe='now 7-d', geo='US')
    data = pytrends.related_queries()[topic]['top']
    
    if data is not None:
        keywords = data['query'].tolist()
        return jsonify({"keywords": keywords})
    else:
        return jsonify({"keywords": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
