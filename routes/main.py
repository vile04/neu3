from flask import Blueprint, render_template, request, jsonify, session
from models import User, Analysis
from app import db
import uuid

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/analysis/<analysis_id>')
def analysis_page(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    return render_template('analysis.html', analysis=analysis)

@main_bp.route('/report/<analysis_id>')
def report_page(analysis_id):
    analysis = Analysis.query.get_or_404(analysis_id)
    return render_template('report.html', analysis=analysis)

@main_bp.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        username = data.get('username', f'user_{uuid.uuid4().hex[:8]}')
        email = data.get('email', f'{username}@example.com')
        
        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            session['user_id'] = existing_user.id
            return jsonify({'success': True, 'user_id': existing_user.id})
        
        # Create new user
        user = User()
        user.username = username
        user.email = email
        db.session.add(user)
        db.session.commit()
        
        session['user_id'] = user.id
        return jsonify({'success': True, 'user_id': user.id})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
