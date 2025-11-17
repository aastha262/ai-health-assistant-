import google.generativeai as genai
from config import Config

class GeminiHealthService:
    """Service class to interact with Gemini API for health recommendations"""
    
    def __init__(self):
        """Initialize Gemini API with configuration"""
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def calculate_bmi(self, weight_kg, height_cm):
        """Calculate BMI from weight and height"""
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)
        return round(bmi, 2)
    
    def get_bmi_category(self, bmi):
        """Categorize BMI into health categories"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def calculate_health_score(self, age, bmi):
        """Calculate health score based on age and BMI"""
        base_score = 100
        
        # BMI scoring
        if 18.5 <= bmi < 25:
            bmi_score = 0  # Ideal BMI
        elif 17 <= bmi < 18.5 or 25 <= bmi < 27:
            bmi_score = -10  # Slightly off
        elif 16 <= bmi < 17 or 27 <= bmi < 30:
            bmi_score = -20  # Concerning
        else:
            bmi_score = -30  # Very concerning
        
        # Age-based adjustments
        if age < 5 or age > 80:
            age_adjustment = -5
        else:
            age_adjustment = 0
        
        final_score = base_score + bmi_score + age_adjustment
        return max(40, min(100, final_score))  # Keep between 40-100
    
    def generate_health_report(self, gender, age, height, weight, language='english'):
        """Generate comprehensive health report using Gemini API"""
        
        try:
            # Calculate metrics
            bmi = self.calculate_bmi(weight, height)
            bmi_category = self.get_bmi_category(bmi)
            health_score = self.calculate_health_score(age, bmi)
            
            # Language-specific prompts
            if language.lower() == 'gujarati':
                prompt = self._create_gujarati_prompt(gender, age, height, weight, bmi, bmi_category)
            else:
                prompt = self._create_english_prompt(gender, age, height, weight, bmi, bmi_category)
            
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Structure the response
            result = {
                'success': True,
                'health_score': health_score,
                'bmi': bmi,
                'bmi_category': bmi_category,
                'recommendations': response.text,
                'user_data': {
                    'gender': gender,
                    'age': age,
                    'height': height,
                    'weight': weight
                }
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to generate health report. Please try again.'
            }
    
    def _create_english_prompt(self, gender, age, height, weight, bmi, bmi_category):
        """Create English prompt for Gemini"""
        return f"""
You are a friendly health advisor for school children. Generate a simple, encouraging health report.

USER PROFILE:
- Gender: {gender}
- Age: {age} years
- Height: {height} cm
- Weight: {weight} kg
- BMI: {bmi} ({bmi_category})

Please provide:

1. **VEGETARIAN DIET PLAN** (Kid-friendly, easy to understand):
   - with protein, fiber, calcium and vitamins 
   - Healthy snacks
   
2. **EXERCISE RECOMMENDATIONS** (Age-appropriate, fun activities):
   - 3-4 exercises suitable for age {age}
   - Duration and frequency for each
   - Make them sound fun and achievable

3. **YOGA POSES** (Simple, safe for age {age}):
   - 3-4 basic yoga poses
   - Benefits of each pose

Keep the language simple, friendly, and encouraging for children. Use emojis to make it fun! 🌟
Focus on vegetarian foods available in India. Make exercises sound like games or fun activities.
"""
    
    def _create_gujarati_prompt(self, gender, age, height, weight, bmi, bmi_category):
        """Create Gujarati prompt for Gemini"""
        return f"""
તમે શાળાના બાળકો માટે મિત્રતાપૂર્ણ આરોગ્ય સલાહકાર છો. સરળ અને પ્રોત્સાહક આરોગ્ય રિપોર્ટ બનાવો.

વપરાશકર્તા પ્રોફાઇલ:
- લિંગ: {gender}
- ઉંમર: {age} વર્ષ
- ઊંચાઈ: {height} સે.મી.
- વજન: {weight} કિ.ગ્રા.
- BMI: {bmi} ({bmi_category})

કૃપા કરીને આપો:

1. **શાકાહારી આહાર યોજના** (બાળકો માટે સરળ):
   - નાસ્તાના સૂચનો (2-3 વિકલ્પો)
   - બપોરના સૂચનો (2-3 વિકલ્પો)
   - રાત્રિના સૂચનો (2-3 વિકલ્પો)
   - તંદુરસ્ત નાસ્તો

2. **કસરતની ભલામણો** (ઉંમર મુજબ, મજાદાર પ્રવૃત્તિઓ):
   - {age} વર્ષની ઉંમર માટે 3-4 કસરતો
   - દરેક માટે સમય અને વારંવારતા
   - તેમને મજાદાર બનાવો

3. **યોગાસન** ({age} વર્ષ માટે સરળ):
   - 3-4 મૂળભૂત યોગાસન
   - દરેક આસનના ફાયદા
   - દરેક કેટલો સમય કરવો

ભાષા સરળ, મિત્રતાપૂર્ણ અને બાળકો માટે પ્રોત્સાહક રાખો. મજા માટે ઇમોજીનો ઉપયોગ કરો! 🌟
ગુજરાતમાં ઉપલબ્ધ શાકાહારી ખોરાક પર ધ્યાન કેન્દ્રિત કરો.
"""