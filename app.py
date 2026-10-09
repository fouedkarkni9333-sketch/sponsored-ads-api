from datetime import datetime
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# قاعدة بيانات مؤقتة للإعلانات
database = [
    {
        "id": 1,
        "title": "إعلان صيانة معدات صناعية",
        "is_sponsored": True,
        "expiry_date": "2026-12-31",
    },
    {
        "id": 2,
        "title": "منشور عرض مبيع أجهزة",
        "is_sponsored": False,
        "expiry_date": "2026-05-01",
    },
]


@app.route("/", methods=["GET"])
def home():
  current_date = datetime.now().strftime("%Y-%m-%d")

  # تحديث حالة الإعلانات المنتهية
  for item in database:
    if item["is_sponsored"] and item["expiry_date"] < current_date:
      item["is_sponsored"] = False

  # ترتيب النتائج: الممولة أولاً
  sorted_items = sorted(database, key=lambda x: x["is_sponsored"], reverse=True)

  # استدعاء ملف الـ HTML المستقل
  return render_template("index.html", items=sorted_items)


@app.route("/items", methods=["GET"])
def get_items_json():
  return jsonify(database)


if __name__ == "__main__":
  app.run(debug=True)
