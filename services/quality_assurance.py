"""
Sistema de Garantia de Qualidade (Quality Assurance)
Garante que todos os processos sejam executados com perfeição
E que relatórios tenham mínimo de 25.000 caracteres com dados reais
"""
import logging
import time
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)

@dataclass
class QualityMetrics:
    """Métricas de qualidade para validação"""
    min_report_length: int = 25000
    min_sections: int = 8
    min_analysis_depth: int = 1000  # caracteres por seção crítica
    required_components: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.required_components is None:
            self.required_components = [
                'avatar_psicologico',
                'drivers_mentais', 
                'analise_objecoes',
                'estrategias_marketing',
                'analise_concorrencia',
                'dados_mercado',
                'recomendacoes_acao',
                'metricas_sucesso'
            ]

@dataclass
class QualityResult:
    """Resultado da validação de qualidade"""
    is_valid: bool
    score: float
    issues: List[str]
    metrics: Dict[str, Any]
    improvement_suggestions: List[str]

class QualityAssuranceSystem:
    """
    Sistema de Garantia de Qualidade que assegura execução perfeita
    ZERO tolerância para dados simulados ou relatórios incompletos
    """
    
    def __init__(self):
        self.metrics = QualityMetrics()
        self.validation_rules = self._setup_validation_rules()
        self.content_validators = self._setup_content_validators()
        
    def _setup_validation_rules(self) -> Dict[str, Any]:
        """Define regras rigorosas de validação"""
        return {
            'length_validation': {
                'min_total_length': 25000,
                'min_section_length': 800,
                'min_paragraph_length': 150
            },
            'content_validation': {
                'forbidden_patterns': [
                    r'\[.*?\]',  # placeholders em colchetes
                    r'lorem ipsum',
                    r'exemplo.*genérico',
                    r'simulado',
                    r'mocado',
                    r'placeholder',
                    r'your.*here',
                    r'insert.*content',
                    r'add.*information',
                    r'replace.*with',
                    r'coming soon',
                    r'to be added',
                    r'xxx+',
                    r'pending',
                    r'tbd',
                    r'todo'
                ],
                'required_patterns': [
                    r'\d+%',  # percentuais
                    r'R\$\s*\d+',  # valores monetários
                    r'\d{4}',  # anos
                    r'pesquisa.*mostrou?',  # referências a pesquisas
                    r'dados.*indicam',  # referências a dados
                    r'análise.*revela'  # referências a análises
                ]
            },
            'structure_validation': {
                'required_sections': [
                    'perfil.*avatar',
                    'drivers.*mentais',
                    'análise.*objeções',
                    'estratégias.*marketing',
                    'concorrência',
                    'mercado',
                    'recomendações',
                    'métricas'
                ],
                'min_subsections_per_section': 3
            }
        }
    
    def _setup_content_validators(self) -> Dict[str, Any]:
        """Configura validadores específicos de conteúdo"""
        return {
            'psychology_analysis': self._validate_psychology_analysis,
            'market_data': self._validate_market_data,
            'competitor_analysis': self._validate_competitor_analysis,
            'strategy_recommendations': self._validate_strategy_recommendations
        }
    
    def validate_complete_report(self, report_data: Dict[str, Any]) -> QualityResult:
        """
        Validação completa e rigorosa do relatório
        Garante qualidade mínima de 25.000 caracteres com dados reais
        """
        logger.info("Iniciando validação rigorosa de qualidade")
        
        issues = []
        metrics = {}
        improvement_suggestions = []
        total_score = 0.0
        max_score = 100.0
        
        # 1. Validação de Comprimento (20 pontos)
        length_score, length_issues, length_metrics = self._validate_length(report_data)
        total_score += length_score
        issues.extend(length_issues)
        metrics.update(length_metrics)
        
        # 2. Validação de Conteúdo Real (30 pontos)
        content_score, content_issues, content_suggestions = self._validate_real_content(report_data)
        total_score += content_score
        issues.extend(content_issues)
        improvement_suggestions.extend(content_suggestions)
        
        # 3. Validação de Estrutura (20 pontos)
        structure_score, structure_issues = self._validate_structure(report_data)
        total_score += structure_score
        issues.extend(structure_issues)
        
        # 4. Validação de Componentes Obrigatórios (20 pontos)
        components_score, components_issues = self._validate_required_components(report_data)
        total_score += components_score
        issues.extend(components_issues)
        
        # 5. Validação de Profundidade Analítica (10 pontos)
        depth_score, depth_issues = self._validate_analysis_depth(report_data)
        total_score += depth_score
        issues.extend(depth_issues)
        
        final_score = (total_score / max_score) * 100
        is_valid = final_score >= 85.0 and len(issues) == 0
        
        # Adicionar sugestões baseadas na pontuação
        if final_score < 85:
            improvement_suggestions.append("Relatório não atinge qualidade mínima de 85%")
        if final_score < 70:
            improvement_suggestions.append("Revisão completa necessária - qualidade muito baixa")
        
        logger.info(f"Validação concluída - Score: {final_score:.1f}%, Válido: {is_valid}")
        
        return QualityResult(
            is_valid=is_valid,
            score=final_score,
            issues=issues,
            metrics=metrics,
            improvement_suggestions=improvement_suggestions
        )
    
    def _validate_length(self, report_data: Dict[str, Any]) -> Tuple[float, List[str], Dict[str, Any]]:
        """Validação rigorosa de comprimento (20 pontos máximo)"""
        issues = []
        metrics = {}
        score = 0.0
        
        # Extrair todo o texto do relatório
        full_text = self._extract_all_text(report_data)
        total_length = len(full_text)
        
        metrics['total_characters'] = total_length
        metrics['total_words'] = len(full_text.split())
        
        # Verificar comprimento mínimo absoluto
        if total_length >= self.metrics.min_report_length:
            score += 15.0  # 15 pontos por atingir o mínimo
            logger.info(f"✓ Comprimento adequado: {total_length:,} caracteres")
        else:
            deficit = self.metrics.min_report_length - total_length
            issues.append(f"Relatório muito curto: {total_length:,} caracteres (faltam {deficit:,})")
            score += max(0, (total_length / self.metrics.min_report_length) * 15.0)
        
        # Verificar distribuição por seções
        sections = report_data.get('sections', {})
        if sections:
            section_lengths = {}
            for section_name, section_content in sections.items():
                section_text = str(section_content)
                section_length = len(section_text)
                section_lengths[section_name] = section_length
                
                if section_length < 800:  # mínimo por seção
                    issues.append(f"Seção '{section_name}' muito curta: {section_length} caracteres")
            
            metrics['section_lengths'] = section_lengths
            
            # Bonificar distribuição equilibrada
            if len([l for l in section_lengths.values() if l >= 800]) >= 6:
                score += 5.0  # 5 pontos bonus por distribuição
        
        return score, issues, metrics
    
    def _validate_real_content(self, report_data: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Validação rigorosa de conteúdo real (30 pontos máximo)"""
        issues = []
        suggestions = []
        score = 0.0
        
        full_text = self._extract_all_text(report_data).lower()
        
        # 1. Verificar padrões proibidos (indicadores de conteúdo falso)
        forbidden_found = 0
        for pattern in self.validation_rules['content_validation']['forbidden_patterns']:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            if matches:
                forbidden_found += len(matches)
                issues.append(f"Conteúdo simulado detectado: '{matches[0]}' (padrão: {pattern})")
        
        if forbidden_found == 0:
            score += 15.0  # 15 pontos por não ter conteúdo simulado
        else:
            penalty = min(15.0, forbidden_found * 2.0)
            score += max(0, 15.0 - penalty)
            suggestions.append("Remover todo conteúdo simulado, mocado ou placeholder")
        
        # 2. Verificar padrões obrigatórios (indicadores de dados reais)
        required_found = 0
        for pattern in self.validation_rules['content_validation']['required_patterns']:
            matches = re.findall(pattern, full_text, re.IGNORECASE)
            required_found += len(matches)
        
        if required_found >= 10:  # pelo menos 10 indicadores de dados reais
            score += 15.0
        else:
            score += (required_found / 10) * 15.0
            suggestions.append("Adicionar mais dados específicos (percentuais, valores, datas)")
        
        # 3. Verificar qualidade de citações e referências
        citation_patterns = [
            r'segundo.*pesquisa',
            r'estudo.*mostrou',
            r'dados.*ibge',
            r'relatório.*mostra',
            r'fonte:',
            r'baseado.*em'
        ]
        
        citations_found = 0
        for pattern in citation_patterns:
            citations_found += len(re.findall(pattern, full_text, re.IGNORECASE))
        
        if citations_found >= 5:
            # Pontuação bonus por citações
            score += min(5.0, citations_found)
        else:
            suggestions.append("Adicionar mais referências e citações de fontes confiáveis")
        
        return min(30.0, score), issues, suggestions
    
    def _validate_structure(self, report_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Validação de estrutura do relatório (20 pontos máximo)"""
        issues = []
        score = 0.0
        
        sections = report_data.get('sections', {})
        if not sections:
            issues.append("Relatório sem estrutura de seções definida")
            return 0.0, issues
        
        # Verificar seções obrigatórias
        required_sections = self.validation_rules['structure_validation']['required_sections']
        found_sections = 0
        
        for required_pattern in required_sections:
            section_found = False
            for section_name in sections.keys():
                if re.search(required_pattern, section_name.lower()):
                    section_found = True
                    break
            
            if section_found:
                found_sections += 1
            else:
                issues.append(f"Seção obrigatória ausente: {required_pattern}")
        
        # Pontuação por seções encontradas
        section_score = (found_sections / len(required_sections)) * 15.0
        score += section_score
        
        # Verificar subseções
        total_subsections = 0
        for section_name, section_content in sections.items():
            if isinstance(section_content, dict):
                subsections = len(section_content.keys())
                total_subsections += subsections
                
                if subsections < 3:
                    issues.append(f"Seção '{section_name}' tem poucas subseções: {subsections}")
        
        if total_subsections >= 20:  # pelo menos 20 subseções no total
            score += 5.0
        else:
            score += (total_subsections / 20) * 5.0
        
        return score, issues
    
    def _validate_required_components(self, report_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Validação de componentes obrigatórios (20 pontos máximo)"""
        issues = []
        score = 0.0
        
        full_text = self._extract_all_text(report_data).lower()
        
        components_found = 0
        for component in self.metrics.required_components:
            # Buscar por padrões relacionados ao componente
            component_patterns = {
                'avatar_psicologico': [r'avatar.*psicológico', r'perfil.*demográfico', r'persona'],
                'drivers_mentais': [r'drivers.*mentais', r'gatilhos.*psicológicos', r'motivadores'],
                'analise_objecoes': [r'análise.*objeções', r'objeções.*cliente', r'resistências'],
                'estrategias_marketing': [r'estratégias.*marketing', r'plano.*marketing', r'táticas'],
                'analise_concorrencia': [r'análise.*concorrência', r'concorrentes', r'competidores'],
                'dados_mercado': [r'dados.*mercado', r'mercado.*alvo', r'segmentação'],
                'recomendacoes_acao': [r'recomendações', r'plano.*ação', r'próximos.*passos'],
                'metricas_sucesso': [r'métricas.*sucesso', r'indicadores', r'kpis']
            }
            
            patterns = component_patterns.get(component, [component.replace('_', '.*')])
            component_found = False
            
            for pattern in patterns:
                if re.search(pattern, full_text):
                    component_found = True
                    break
            
            if component_found:
                components_found += 1
            else:
                issues.append(f"Componente obrigatório ausente: {component}")
        
        # Pontuação proporcional aos componentes encontrados
        score = (components_found / len(self.metrics.required_components)) * 20.0
        
        return score, issues
    
    def _validate_analysis_depth(self, report_data: Dict[str, Any]) -> Tuple[float, List[str]]:
        """Validação de profundidade analítica (10 pontos máximo)"""
        issues = []
        score = 0.0
        
        # Verificar indicadores de análise profunda
        depth_indicators = [
            r'porque.*comportamento',
            r'psicologia.*consumidor',
            r'motivação.*compra',
            r'processo.*decisão',
            r'influência.*social',
            r'aspectos.*emocionais',
            r'padrões.*comportamento',
            r'drivers.*inconscientes'
        ]
        
        full_text = self._extract_all_text(report_data).lower()
        depth_score = 0
        
        for indicator in depth_indicators:
            matches = len(re.findall(indicator, full_text))
            depth_score += matches
        
        if depth_score >= 15:  # pelo menos 15 indicadores de profundidade
            score = 10.0
        else:
            score = (depth_score / 15) * 10.0
            if depth_score < 8:
                issues.append("Análise psicológica muito superficial - necessária maior profundidade")
        
        return score, issues
    
    def _validate_psychology_analysis(self, content: str) -> bool:
        """Valida se a análise psicológica é robusta"""
        psychology_terms = [
            'comportamento', 'motivação', 'psicologia', 'emocional',
            'cognição', 'percepção', 'atitude', 'personalidade'
        ]
        
        content_lower = content.lower()
        found_terms = sum(1 for term in psychology_terms if term in content_lower)
        
        return found_terms >= 5 and len(content) >= 1000
    
    def _validate_market_data(self, content: str) -> bool:
        """Valida se os dados de mercado são específicos"""
        data_indicators = [
            r'\d+%', r'R\$\s*\d+', r'\d{4}', r'milhões?', r'bilhões?',
            r'crescimento.*\d+', r'mercado.*\d+', r'segmento.*\d+'
        ]
        
        indicators_found = 0
        for pattern in data_indicators:
            indicators_found += len(re.findall(pattern, content))
        
        return indicators_found >= 8 and len(content) >= 800
    
    def _validate_competitor_analysis(self, content: str) -> bool:
        """Valida se a análise de concorrência é específica"""
        competitor_indicators = [
            'empresa', 'concorrente', 'competidor', 'líder.*mercado',
            'participação.*mercado', 'estratégia.*competitiva'
        ]
        
        content_lower = content.lower()
        found_indicators = sum(1 for indicator in competitor_indicators if indicator in content_lower)
        
        return found_indicators >= 4 and len(content) >= 600
    
    def _validate_strategy_recommendations(self, content: str) -> bool:
        """Valida se as recomendações são acionáveis"""
        action_terms = [
            'implementar', 'executar', 'desenvolver', 'criar', 'lançar',
            'estabelecer', 'construir', 'otimizar', 'melhorar'
        ]
        
        content_lower = content.lower()
        action_count = sum(1 for term in action_terms if term in content_lower)
        
        return action_count >= 6 and len(content) >= 800
    
    def _extract_all_text(self, data: Any) -> str:
        """Extrai todo o texto de uma estrutura de dados"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            text_parts = []
            for value in data.values():
                text_parts.append(self._extract_all_text(value))
            return ' '.join(text_parts)
        elif isinstance(data, list):
            text_parts = []
            for item in data:
                text_parts.append(self._extract_all_text(item))
            return ' '.join(text_parts)
        else:
            return str(data)
    
    def suggest_improvements(self, report_data: Dict[str, Any]) -> List[str]:
        """Sugere melhorias específicas para atingir qualidade mínima"""
        quality_result = self.validate_complete_report(report_data)
        
        suggestions = quality_result.improvement_suggestions.copy()
        
        # Sugestões específicas baseadas nas métricas
        total_length = quality_result.metrics.get('total_characters', 0)
        if total_length < 25000:
            deficit = 25000 - total_length
            suggestions.append(f"Expandir conteúdo em {deficit:,} caracteres")
            suggestions.append("Adicionar mais análises detalhadas em cada seção")
            suggestions.append("Incluir exemplos específicos e casos de uso")
        
        if quality_result.score < 85:
            suggestions.append("Foco em dados reais e análises específicas")
            suggestions.append("Remover qualquer conteúdo genérico ou simulado")
            suggestions.append("Aprofundar análise psicológica dos consumidores")
        
        return suggestions
    
    def create_quality_report(self, validation_result: QualityResult) -> Dict[str, Any]:
        """Cria relatório detalhado de qualidade"""
        return {
            'timestamp': time.time(),
            'overall_score': validation_result.score,
            'is_approved': validation_result.is_valid,
            'quality_grade': self._calculate_grade(validation_result.score),
            'issues_found': len(validation_result.issues),
            'critical_issues': validation_result.issues,
            'improvement_suggestions': validation_result.improvement_suggestions,
            'metrics': validation_result.metrics,
            'next_steps': self._generate_next_steps(validation_result)
        }
    
    def _calculate_grade(self, score: float) -> str:
        """Calcula nota baseada na pontuação"""
        if score >= 95:
            return 'A+'
        elif score >= 90:
            return 'A'
        elif score >= 85:
            return 'B+'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'
    
    def _generate_next_steps(self, validation_result: QualityResult) -> List[str]:
        """Gera próximos passos baseados na validação"""
        if validation_result.is_valid:
            return ["Relatório aprovado para entrega", "Realizar revisão final opcional"]
        
        steps = []
        if validation_result.score < 70:
            steps.append("Revisão completa necessária")
            steps.append("Regenerar seções com baixa qualidade")
        elif validation_result.score < 85:
            steps.append("Melhorar seções específicas")
            steps.append("Adicionar mais dados e análises")
        
        steps.extend(validation_result.improvement_suggestions[:3])  # Top 3 sugestões
        
        return steps