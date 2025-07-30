from flask import Blueprint, request, jsonify, session, send_file
from models import Analysis, User
from app import db
# from app import socketio  # Temporarily disabled
from services.simple_backup_manager import SimpleBackupManager
from services.pdf_generator import PDFGenerator
import threading
import uuid
from datetime import datetime, timedelta

analysis_bp = Blueprint('analysis', __name__)

@analysis_bp.route('/start_analysis', methods=['POST'])
def start_analysis():
    try:
        data = request.get_json()
        user_id = session.get('user_id')

        if not user_id:
            return jsonify({'success': False, 'error': 'User not authenticated'}), 401

        # Create analysis record
        analysis = Analysis()
        analysis.user_id = user_id
        analysis.product_name = data.get('product_name')
        analysis.product_description = data.get('product_description', '')
        analysis.target_market = data.get('target_market')
        analysis.competition_keywords = data.get('competition_keywords', [])
        analysis.status = 'processing'
        analysis.current_step = 'Initializing analysis...'
        analysis.estimated_completion = datetime.utcnow() + timedelta(minutes=45)

        db.session.add(analysis)
        db.session.commit()

        # Start analysis in background thread
        thread = threading.Thread(
            target=run_complete_analysis,
            args=(analysis.id, data)
        )
        thread.daemon = True
        thread.start()

        return jsonify({
            'success': True,
            'analysis_id': analysis.id,
            'estimated_completion': analysis.estimated_completion.isoformat()
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analysis_bp.route('/analysis_status/<analysis_id>')
def get_analysis_status(analysis_id):
    try:
        analysis = Analysis.query.get_or_404(analysis_id)
        return jsonify({
            'status': analysis.status,
            'progress': analysis.progress,
            'current_step': analysis.current_step,
            'estimated_completion': analysis.estimated_completion.isoformat() if analysis.estimated_completion else None,
            'error_message': analysis.error_message,
            'completed_at': analysis.completed_at.isoformat() if analysis.completed_at else None
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@analysis_bp.route('/download_report/<analysis_id>')
def download_report(analysis_id):
    try:
        analysis = Analysis.query.get_or_404(analysis_id)

        if not analysis.pdf_path or analysis.status != 'completed':
            return jsonify({'error': 'Report not ready'}), 400

        return send_file(
            analysis.pdf_path,
            as_attachment=True,
            download_name=f'psychological_analysis_{analysis.product_name}_{analysis.analysis_id[:8]}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_complete_analysis(analysis_id, input_data):
    """Run the complete analysis pipeline in background"""
    analysis = None
    try:
        analysis = Analysis.query.get(analysis_id)
        if not analysis:
            raise ValueError(f"Analysis {analysis_id} not found")

        # Usar sistema de backup simplificado
        backup_manager = SimpleBackupManager()

        # Update progress function
        def update_progress(step, progress, message):
            if analysis:
                analysis.progress = progress
                analysis.current_step = message
                db.session.commit()
                # socketio.emit('analysis_progress', {  # Temporarily disabled
                #     'analysis_id': analysis_id,
                #     'progress': progress,
                #     'current_step': step,
                #     'message': message
                # })

        # Executar análise completa com sistema de backup
        update_progress('analysis_start', 10, 'Iniciando análise com sistema de backup automático...')
        # Simulate a long-running analysis process
        # time.sleep(5)

        # Preparar dados para análise
        product_name = input_data.get('product_name', '')
        product_description = input_data.get('product_description', '')
        target_market = input_data.get('target_market', '')
        competition_keywords = input_data.get('competition_keywords', [])

        update_progress('data_collection', 30, 'Coletando dados de mercado com backups automáticos...')

        # Executar análise completa
        result = backup_manager.execute_analysis(
            product_name=product_name,
            product_description=product_description,
            target_market=target_market,
            competition_keywords=competition_keywords
        )

        update_progress('analysis_processing', 60, 'Processando análise psicológica...')

        if result['success']:
            # Salvar resultados
            analysis.results = result['report']
            analysis.quality_score = result['quality_score']
            analysis.execution_time = result['execution_time']
            analysis.metadata = {
                'services_used': result['services_used'],
                'report_stats': result['report_stats'],
                'warnings': result.get('warnings', [])
            }

            update_progress('report_generation', 80, 'Gerando relatório final...')

            # Gerar PDF se possível
            try:
                from services.pdf_generator import PDFGenerator
                pdf_generator = PDFGenerator()
                pdf_path = pdf_generator.generate_comprehensive_report(
                    analysis.results,
                    f"psychological_analysis_{analysis.id}.pdf"
                )
                analysis.pdf_path = pdf_path
            except Exception as e:
                # PDF generation is not critical
                import logging
                logging.warning(f"Erro ao gerar PDF: {e}")

        else:
            # Erro na análise
            raise Exception(result.get("error", "Erro desconhecido na análise"))

            # Finalizar análise
            analysis.status = 'completed'
            analysis.progress = 100
            analysis.completed_at = datetime.utcnow()
            analysis.current_step = f'Análise concluída! Qualidade: {result["quality_score"]:.1f}%'
            db.session.commit()

            update_progress('completed', 100, f'Análise concluída com sucesso! Qualidade: {result["quality_score"]:.1f}%')

        else:
            # Erro na análise
            raise Exception(result.get('error', 'Erro desconhecido na análise'))

    except Exception as e:
        if analysis:
            analysis.status = 'error'
            analysis.error_message = str(e)
            db.session.commit()
            # socketio.emit('analysis_error', {  # Temporarily disabled
            #     'analysis_id': analysis_id,
            #     'error': str(e)
            # })




