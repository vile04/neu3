"""
Gerador de PDF para relatórios de análise psicológica
Cria documentos profissionais com formatação avançada
"""
import logging
import os
from typing import Dict, Any, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    Gerador de PDF com formatação profissional
    Converte análises em documentos presentation-ready
    """
    
    def __init__(self):
        self.output_dir = "reports"
        self.ensure_output_directory()
        
    def ensure_output_directory(self):
        """Garante que o diretório de relatórios existe"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_comprehensive_report(self, analysis_data: Dict[str, Any], 
                                    filename: str) -> str:
        """
        Gera PDF completo da análise psicológica
        """
        try:
            from reportlab.lib.pagesizes import A4, letter
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
            from reportlab.platypus import Table, TableStyle, Image
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
            
            # Caminho completo do arquivo
            filepath = os.path.join(self.output_dir, filename)
            
            # Criar documento
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Estilos
            styles = getSampleStyleSheet()
            story = []
            
            # Estilo customizado para título
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=TA_CENTER,
                textColor=colors.HexColor('#2C3E50')
            )
            
            # Estilo para subtítulos
            subtitle_style = ParagraphStyle(
                'CustomSubtitle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                textColor=colors.HexColor('#34495E')
            )
            
            # Estilo para corpo do texto
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                leftIndent=20,
                rightIndent=20
            )
            
            # Capa
            story.append(Paragraph("ANÁLISE PSICOLÓGICA DE MERCADO", title_style))
            story.append(Spacer(1, 20))
            
            # Informações do produto
            product_info = analysis_data.get('metadata', {}).get('product_info', {})
            if product_info:
                story.append(Paragraph(f"<b>Produto:</b> {product_info.get('name', 'N/A')}", body_style))
                story.append(Paragraph(f"<b>Categoria:</b> {product_info.get('category', 'N/A')}", body_style))
            
            story.append(Spacer(1, 20))
            story.append(Paragraph(f"<b>Data de Geração:</b> {datetime.now().strftime('%d/%m/%Y às %H:%M')}", body_style))
            story.append(PageBreak())
            
            # Índice
            story.append(Paragraph("ÍNDICE", title_style))
            story.append(Spacer(1, 20))
            
            index_items = [
                "1. Resumo Executivo",
                "2. Perfil do Avatar Psicológico", 
                "3. Drivers Mentais Identificados",
                "4. Análise de Objeções",
                "5. Análise da Concorrência",
                "6. Estratégias de Marketing",
                "7. Dados de Mercado",
                "8. Recomendações de Implementação",
                "9. Métricas de Acompanhamento"
            ]
            
            for item in index_items:
                story.append(Paragraph(item, body_style))
                story.append(Spacer(1, 6))
            
            story.append(PageBreak())
            
            # Conteúdo principal
            sections = [
                ("Resumo Executivo", analysis_data.get('executive_summary', '')),
                ("Perfil do Avatar Psicológico", analysis_data.get('avatar_psicologico', {})),
                ("Drivers Mentais Identificados", analysis_data.get('drivers_mentais', {})),
                ("Análise de Objeções", analysis_data.get('analise_objecoes', {})),
                ("Análise da Concorrência", analysis_data.get('analise_concorrencia', {})),
                ("Estratégias de Marketing", analysis_data.get('estrategias_marketing', {})),
                ("Dados de Mercado", analysis_data.get('dados_mercado', {})),
                ("Recomendações de Implementação", analysis_data.get('recomendacoes_implementacao', {})),
                ("Métricas de Acompanhamento", analysis_data.get('metricas_acompanhamento', {}))
            ]
            
            for section_title, section_data in sections:
                story.append(Paragraph(section_title, subtitle_style))
                story.append(Spacer(1, 12))
                
                # Processar conteúdo da seção
                content = self._extract_section_content(section_data)
                if content:
                    # Quebrar conteúdo em parágrafos
                    paragraphs = content.split('\n\n')
                    for para in paragraphs:
                        if para.strip():
                            story.append(Paragraph(para.strip(), body_style))
                            story.append(Spacer(1, 6))
                else:
                    story.append(Paragraph("Conteúdo não disponível para esta seção.", body_style))
                
                story.append(Spacer(1, 20))
            
            # Rodapé com informações técnicas
            story.append(PageBreak())
            story.append(Paragraph("INFORMAÇÕES TÉCNICAS", subtitle_style))
            
            metadata = analysis_data.get('metadata', {})
            if metadata:
                story.append(Paragraph(f"<b>Sistema:</b> PsychAnalytica v3.0", body_style))
                story.append(Paragraph(f"<b>Modo de Operação:</b> {metadata.get('system_mode', 'Standard')}", body_style))
                
                services_used = metadata.get('services_used', [])
                if services_used:
                    story.append(Paragraph(f"<b>Serviços Utilizados:</b> {', '.join(services_used)}", body_style))
            
            # Gerar PDF
            doc.build(story)
            
            logger.info(f"PDF gerado com sucesso: {filepath}")
            return filepath
            
        except ImportError:
            logger.warning("ReportLab não instalado, gerando relatório texto")
            return self._generate_text_report(analysis_data, filename)
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            return self._generate_text_report(analysis_data, filename)
    
    def _extract_section_content(self, section_data: Any) -> str:
        """Extrai conteúdo textual de uma seção"""
        if isinstance(section_data, str):
            return section_data
        elif isinstance(section_data, dict):
            content_parts = []
            for key, value in section_data.items():
                if key == 'content':
                    content_parts.append(str(value))
                elif isinstance(value, str) and len(value) > 50:
                    content_parts.append(f"**{key.replace('_', ' ').title()}:**\n{value}")
            return '\n\n'.join(content_parts)
        else:
            return str(section_data)
    
    def _generate_text_report(self, analysis_data: Dict[str, Any], filename: str) -> str:
        """Gera relatório em texto quando PDF não é possível"""
        try:
            text_filename = filename.replace('.pdf', '.txt')
            filepath = os.path.join(self.output_dir, text_filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("ANÁLISE PSICOLÓGICA DE MERCADO\n")
                f.write("=" * 80 + "\n\n")
                
                # Informações do produto
                product_info = analysis_data.get('metadata', {}).get('product_info', {})
                if product_info:
                    f.write(f"Produto: {product_info.get('name', 'N/A')}\n")
                    f.write(f"Categoria: {product_info.get('category', 'N/A')}\n\n")
                
                f.write(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y às %H:%M')}\n\n")
                
                # Seções
                sections = [
                    ("RESUMO EXECUTIVO", analysis_data.get('executive_summary', '')),
                    ("PERFIL DO AVATAR PSICOLÓGICO", analysis_data.get('avatar_psicologico', {})),
                    ("DRIVERS MENTAIS IDENTIFICADOS", analysis_data.get('drivers_mentais', {})),
                    ("ANÁLISE DE OBJEÇÕES", analysis_data.get('analise_objecoes', {})),
                    ("ANÁLISE DA CONCORRÊNCIA", analysis_data.get('analise_concorrencia', {})),
                    ("ESTRATÉGIAS DE MARKETING", analysis_data.get('estrategias_marketing', {})),
                    ("DADOS DE MERCADO", analysis_data.get('dados_mercado', {})),
                    ("RECOMENDAÇÕES DE IMPLEMENTAÇÃO", analysis_data.get('recomendacoes_implementacao', {})),
                    ("MÉTRICAS DE ACOMPANHAMENTO", analysis_data.get('metricas_acompanhamento', {}))
                ]
                
                for section_title, section_data in sections:
                    f.write("-" * 60 + "\n")
                    f.write(f"{section_title}\n")
                    f.write("-" * 60 + "\n\n")
                    
                    content = self._extract_section_content(section_data)
                    if content:
                        f.write(content + "\n\n")
                    else:
                        f.write("Conteúdo não disponível para esta seção.\n\n")
                
                f.write("=" * 80 + "\n")
                f.write("Relatório gerado pelo PsychAnalytica v3.0\n")
                f.write("=" * 80 + "\n")
            
            logger.info(f"Relatório texto gerado: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório texto: {e}")
            return ""