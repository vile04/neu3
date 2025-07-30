from app import db
from datetime import datetime
from sqlalchemy import JSON
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    analyses = db.relationship("Analysis", backref=\'user\', lazy=True, cascade=\'all, delete-orphan\')

class Analysis(db.Model):
    __tablename__ = 'analyses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey(\'users.id\'), nullable=False)

    # Input data
    product_name = db.Column(db.String(200), nullable=False)
    product_description = db.Column(db.Text)
    target_market = db.Column(db.String(200))
    price_range = db.Column(db.String(100))
    competition_keywords = db.Column(db.Text)

    # Analysis results
    market_research_data = db.Column(JSON)
    avatar_analysis = db.Column(JSON)
    mental_drivers = db.Column(JSON)
    objection_analysis = db.Column(JSON)
    provi_system = db.Column(JSON)
    prepitch_architecture = db.Column(JSON)

    # Report data
    final_report = db.Column(db.Text)
    report_word_count = db.Column(db.Integer, default=0)
    pdf_path = db.Column(db.String(500))

    # Status tracking
    status = db.Column(db.String(50), default=\'pending\')
    progress = db.Column(db.Integer, default=0)
    current_step = db.Column(db.String(200))
    estimated_completion = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Error handling
    error_message = db.Column(db.Text)

class SearchResult(db.Model):
    __tablename__ = \'search_results\'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = db.Column(db.String(36), db.ForeignKey(\'analyses.id\'), nullable=False)

    url = db.Column(db.String(1000), nullable=False)
    title = db.Column(db.String(500))
    content = db.Column(db.Text)
    source_type = db.Column(db.String(100))  # google, serper, jina, etc.
    relevance_score = db.Column(db.Float, default=0.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIAnalysis(db.Model):
    __tablename__ = \'ai_analyses\'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = db.Column(db.String(36), db.ForeignKey(\'analyses.id\'), nullable=False)

    ai_provider = db.Column(db.String(50)) # openai, gemini, huggingface
    analysis_type = db.Column(db.String(100), nullable=False) # avatar, drivers, objections, etc.
    prompt_used = db.Column(db.Text)
    response_data = db.Column(JSON)
    tokens_used = db.Column(db.Integer)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MentalDriver(db.Model):
    __tablename__ = \'mental_drivers\'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = db.Column(db.String(36), db.ForeignKey(\'analyses.id\'), nullable=False)

    driver_name = db.Column(db.String(200))
    driver_type = db.Column(db.String(100)) # emotional, rational, hidden
    trigger_emotion = db.Column(db.String(100))
    installation_moment = db.Column(db.String(200))
    activation_script = db.Column(db.Text)
    anchor_phrases = db.Column(db.Text)
    logical_proof = db.Column(db.Text)
    priority_level = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ObjectionMapping(db.Model):
    __tablename__ = \'objection_mappings\'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = db.Column(db.String(36), db.ForeignKey(\'analyses.id\'), nullable=False)

    objection_type = db.Column(db.String(100), nullable=False) # time, money, trust, hidden
    objection_text = db.Column(db.Text)
    psychological_root = db.Column(db.Text)
    counter_strategy = db.Column(db.Text)
    neutralization_technique = db.Column(db.String(200))
    proof_elements = db.Column(JSON)
    intensity_level = db.Column(db.Integer, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProviElement(db.Model):
    __tablename__ = \'provi_elements\'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = db.Column(db.String(36), db.ForeignKey(\'analyses.id\'), nullable=False)

    provi_name = db.Column(db.String(200), nullable=False)
    concept_target = db.Column(db.String(200))
    category = db.Column(db.String(100)) # urgency, belief, objection, transformation, method
    priority = db.Column(db.String(50)) # critical, high, medium
    ideal_moment = db.Column(db.String(200))

    psychological_objective = db.Column(db.Text)
    experiment_description = db.Column(db.Text)
    perfect_analogy = db.Column(db.Text)
    complete_script = db.Column(db.Text)
    materials_needed = db.Column(JSON)
    variations = db.Column(JSON)
    risk_management = db.Column(JSON)
    impact_phrases = db.Column(JSON)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


