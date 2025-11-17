# backend/app.py
import os
import logging
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from gemini_service import GeminiHealthService

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determine project root and frontend path
ROOT = Path(__file__).resolve().parents[1]  # project root
FRONTEND_DIR = ROOT / "frontend"

# Create Flask app and serve frontend static files
app = Flask(
    __name__,
    static_folder=str(FRONTEND_DIR),
    static_url_path=""
)
CORS(app)

# Load config (doesn't raise here; we'll handle missing key gracefully)
try:
    Config.validate()  # this will raise if you intentionally want strict validation
    gemini_service = GeminiHealthService()
    logger.info("Gemini service initialized successfully.")
except Exception as e:
    # Do NOT crash the server — allow frontend to load and provide a fallback.
    logger.warning(f"Gemini service not initialized: {e}")
    gemini_service = None

@app.route("/", methods=["GET"])
def index():
    """
    Serve the frontend index.html
    Accessing http://localhost:5000/ will return frontend/index.html
    """
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return send_from_directory(str(FRONTEND_DIR), "index.html")
    return jsonify({
        "success": False,
        "error": "Frontend not found. Make sure the frontend directory exists."
    }), 500

@app.route("/<path:static_path>")
def serve_static(static_path):
    """
    Serve static assets (css, js, images) from the frontend folder.
    """
    file_path = FRONTEND_DIR / static_path
    if file_path.exists():
        return send_from_directory(str(FRONTEND_DIR), static_path)
    return ("", 404)

@app.route('/api/school-info', methods=['GET'])
def get_school_info():
    return jsonify({
        'success': True,
        'school': Config.SCHOOL_INFO
    })

@app.route('/api/health-report', methods=['POST'])
def generate_health_report():
    """
    Expects JSON:
    {
        "gender": "male/female/other",
        "age": 10,
        "height": 140,
        "weight": 35,
        "language": "english"/"gujarati"
    }
    """
    try:
        data = request.get_json(force=True)

        # Basic validation
        required = ['gender', 'age', 'height', 'weight']
        missing = [r for r in required if r not in data]
        if missing:
            return jsonify({'success': False, 'error': f'Missing fields: {missing}'}), 400

        gender = str(data.get('gender')).lower()
        age = int(data.get('age'))
        height = float(data.get('height'))
        weight = float(data.get('weight'))
        language = data.get('language', 'english').lower()

        # Range checks
        if not (1 <= age <= 100):
            return jsonify({'success': False, 'error': 'Age must be 1-100'}), 400
        if not (30 <= height <= 250):
            return jsonify({'success': False, 'error': 'Height must be 30-250 cm'}), 400
        if not (5 <= weight <= 200):
            return jsonify({'success': False, 'error': 'Weight must be 5-200 kg'}), 400
        if gender not in ['male', 'female', 'other']:
            return jsonify({'success': False, 'error': 'Gender must be male/female/other'}), 400

        if gemini_service:
            result = gemini_service.generate_health_report(
                gender=gender, age=age, height=height, weight=weight, language=language
            )
            return jsonify(result), 200 if result.get('success', False) else 500
        else:
            # Fallback generator when Gemini isn't configured — useful for local testing.
            from gemini_service import GeminiHealthService as LocalService
            local = LocalService()
            # local.generate_health_report uses internal prompt -> but since Gemini may fail inside it,
            # we will build a simple local structured response:
            bmi = local.calculate_bmi(weight, height)
            bmi_category = local.get_bmi_category(bmi)
            health_score = local.calculate_health_score(age, bmi)

            # Simple static recommendations for dev/testing
            recommendations = (
                f"DEV FALLBACK REPORT\n\n"
                f"- BMI: {bmi} ({bmi_category})\n"
                f"- Health score: {health_score}/100\n\n"
                f"Vegetarian diet (sample):\n"
                f"Breakfast: Poha with peanuts OR vegetable upma\n"
                f"Lunch: Roti, dal, vegetable curry, curd\n"
                f"Dinner: Khichdi OR vegetable pulao with salad\n\n"
                f"Exercise (kid-friendly):\n"
                f"- Skipping/jumping jacks: 10-15 min daily\n"
                f"- Playful running games: 20 min\n"
                f"- Ball catching: 10 min\n\n"
                f"Yoga (simple):\n"
                f"- Tadasana (Mountain) - 30s\n"
                f"- Vrikshasana (Tree) - 20s each side\n"
            )

            return jsonify({
                'success': True,
                'health_score': health_score,
                'bmi': round(bmi, 2),
                'bmi_category': bmi_category,
                'recommendations': recommendations,
                'user_data': {'gender': gender, 'age': age, 'height': height, 'weight': weight}
            }), 200

    except Exception as exc:
        logger.exception("Error generating health report")
        return jsonify({'success': False, 'error': str(exc)}), 500


if __name__ == "__main__":
    # Start server from project root with: python backend/app.py
    HOST = Config.HOST
    PORT = int(os.environ.get("PORT", Config.PORT))
    DEBUG = Config.DEBUG
    logger.info(f"Starting server at http://{HOST}:{PORT} (debug={DEBUG})")
    app.run(host=HOST, port=PORT, debug=DEBUG)
