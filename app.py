from datetime import datetime
from flask import Flask, jsonify, render_template_string, request

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

# تصميم صفحة الويب البسيطة والجميلة
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منصة الإعلانات</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; direction: rtl; }
        .container { max-width: 600px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; text-align: center; }
        ul { list-style: none; padding: 0; }
        li { background: #fafafa; margin-bottom: 10px; padding: 15px; border-radius: 6px; border: 1px solid #ddd; display: flex; justify-content: space-between; align-items: center; }
        .sponsored { border-right: 5px solid #ff9800; background: #fff9e6; }
        .badge { background: #ff9800; color: white; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
        .normal { background: #e0f7fa; color: #00796b; padding: 3px 8px; border-radius: 4px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>قائمة الإعلانات والمنشورات</h1>
        <ul>
            {% for item in items %}
                <li class="{% if item.is_sponsored %}sponsored{% endif %}">
                    <div>
                        <strong>{{ item.title }}</strong><br>
                        <small style="color: #666;">تاريخ الانتهاء: {{ item.expiry_date }}</small>
                    </div>
                    <div>
                        {% if item.is_sponsored %}
                            <span class="badge">ممول</span>
                        {% else %}
                            <span class="normal">عادي</span>
                        {% endif %}
                    </div>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():
  current_date = datetime.now().strftime("%Y-%m-%d")

  # تحديث حالة الإعلانات المنتهية
  for item in database:
    if item["is_sponsored"] and item["expiry_date"] < current_date:
      item["is_sponsored"] = False

  # ترتيب النتائج: الممولة أولاً
  sorted_items = sorted(database, key=lambda x: x["is_sponsored"], reverse=True)

  # عرض الصفحة بتصميم HTML مباشرة
  return render_template_string(HTML_TEMPLATE, items=sorted_items)


@app.route("/items", methods=["GET"])
def get_items_json():
  return jsonify(database)


if __name__ == "__main__":
  app.run(debug=True)
