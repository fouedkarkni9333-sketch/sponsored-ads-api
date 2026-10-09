from datetime import datetime
from flask import Flask, jsonify, request

app = Flask(__name__)

# قاعدة بيانات مؤقتة
database = [
    {
        "id": 1,
        "title": "إعلان صيانة معدات",
        "is_sponsored": True,
        "expiry_date": "2026-12-31",
    },
    {
        "id": 2,
        "title": "منشور عرض عادي",
        "is_sponsored": False,
        "expiry_date": "2026-05-01",
    },
]


@app.route("/items", methods=["GET"])
def get_items():
  current_date = datetime.now().strftime("%Y-%m-%d")

  # تحديث حالة الإعلانات المنتهية
  for item in database:
    if item["is_sponsored"] and item["expiry_date"] < current_date:
      item["is_sponsored"] = False

  # استقبال كلمة البحث من الرابط (إن وجدت) مثل: /items?search=صيانة
  search_query = request.args.get("search", "").lower()

  filtered_items = database
  if search_query:
    filtered_items = [
        item for item in database if search_query in item["title"].lower()
    ]

  # ترتيب النتائج: الممولة النشطة أولاً
  sorted_items = sorted(
      filtered_items, key=lambda x: x["is_sponsored"], reverse=True
  )
  return jsonify(sorted_items)


@app.route("/items", methods=["POST"])
def add_item():
  data = request.json
  new_item = {
      "id": len(database) + 1,
      "title": data.get("title"),
      "is_sponsored": data.get("is_sponsored", False),
      "expiry_date": data.get("expiry_date"),
  }
  database.append(new_item)
  return jsonify({"message": "تمت الإضافة بنجاح", "item": new_item}), 201


if __name__ == "__main__":
  app.run(debug=True)
