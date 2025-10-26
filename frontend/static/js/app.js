// Enterprise Web Audit Platform - Executive Dashboard
class ExecutiveAuditDashboard {
    constructor() {
        console.log('ExecutiveAuditDashboard constructor called');
        this.form = document.getElementById('auditForm');
        this.loadingState = document.getElementById('loadingState');
        this.resultsSection = document.getElementById('resultsSection');
        this.progressBar = null;
        this.currentStage = 0;
        
        console.log('Form element found:', !!this.form);
        console.log('Loading state element found:', !!this.loadingState);
        console.log('Results section element found:', !!this.resultsSection);
        
        this.init();
    }

    init() {
        this.form.addEventListener('submit', (e) => this.handleAuditSubmission(e));
        this.setupProgressAnimation();
    }

    async handleAuditSubmission(event) {
        event.preventDefault();
        
        const formData = new FormData(this.form);
        const url = formData.get('url');
        
        if (!this.validateUrl(url)) {
            this.showError('Please enter a valid URL');
            return;
        }

        this.showLoadingState();
        this.startProgressAnimation();
        
        try {
            const response = await fetch('/audit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url: url })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // DEBUG: Log the raw response to see if executive_summary is present
            console.log('RAW API RESPONSE:', result);
            console.log('EXECUTIVE SUMMARY IN RESPONSE:', result.executive_summary);
            
            this.displayExecutiveResults(result);
            
        } catch (error) {
            console.error('Audit failed:', error);
            this.showError('Analysis failed. Please try again or contact support.');
        } finally {
            this.hideLoadingState();
        }
    }

    validateUrl(url) {
        try {
            new URL(url);
            return url.startsWith('http://') || url.startsWith('https://');
        } catch {
            return false;
        }
    }

    showLoadingState() {
        this.form.parentElement.parentElement.style.display = 'none';
        this.loadingState.style.display = 'flex';
        this.resultsSection.style.display = 'none';
    }

    hideLoadingState() {
        this.loadingState.style.display = 'none';
        this.form.parentElement.parentElement.style.display = 'flex';
    }

    setupProgressAnimation() {
        this.progressBar = this.loadingState.querySelector('.progress-bar');
        this.stages = this.loadingState.querySelectorAll('.stage');
    }

    startProgressAnimation() {
        this.currentStage = 0;
        this.animateProgress();
    }

    animateProgress() {
        const stages = ['Reconnaissance', 'Performance', 'Security', 'Intelligence'];
        
        const interval = setInterval(() => {
            if (this.currentStage < this.stages.length) {
                // Activate current stage
                this.stages.forEach(stage => stage.classList.remove('active'));
                this.stages[this.currentStage].classList.add('active');
                
                // Update progress bar
                const progress = ((this.currentStage + 1) / this.stages.length) * 100;
                this.progressBar.style.width = `${progress}%`;
                
                this.currentStage++;
            } else {
                clearInterval(interval);
            }
        }, 1500);
    }

    displayExecutiveResults(data) {
        // DEBUG: Check if executive summary exists
        console.log('DEBUG: Full audit data:', data);
        console.log('DEBUG: Executive summary exists:', !!data.executive_summary);
        console.log('DEBUG: Executive summary data:', data.executive_summary);
        console.log('DEBUG: Executive summary keys:', data.executive_summary ? Object.keys(data.executive_summary) : 'N/A');
        
        this.resultsSection.innerHTML = this.generateExecutiveReport(data);
        this.resultsSection.style.display = 'block';
        
        // Smooth scroll to results
        this.resultsSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
        
        // Animate metrics and initialize tooltips
        this.animateMetrics();
    }

    generateExecutiveReport(data) {
        const performanceGrade = this.getGradeClass(data.performance?.overall_grade || 'C');
        const securityGrade = this.getGradeClass(data.security?.risk_level || 'medium');
        const overallGrade = this.getGradeClass(data.grade || 'C');
        
        return `
            <div class="row justify-content-center">
                <div class="col-xl-10">
                    <!-- Compact Header -->
                    <div class="compact-header mb-3">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <h2 class="compact-title mb-1">Executive Intelligence Report</h2>
                                <p class="compact-url mb-0">
                                    <i class="fas fa-globe me-1"></i>
                                    ${data.url}
                                </p>
                            </div>
                            <div class="compact-date">
                                <i class="fas fa-calendar me-1"></i>
                                ${new Date(data.timestamp).toLocaleDateString()}
                            </div>
                        </div>
                    </div>
                    
                    <!-- Compact Metrics -->
                    <div class="row g-3 mb-4">
                        <div class="col-md-4">
                            <div class="compact-metric">
                                <div class="metric-header">
                                    <i class="fas fa-tachometer-alt text-primary"></i>
                                    <span>Performance</span>
                                    <i class="fas fa-info-circle ms-1" data-bs-toggle="tooltip" 
                                       title="${this.getPerformanceExplanation(data.performance?.lighthouse_score || 0)}"></i>
                                </div>
                                <div class="metric-value ${performanceGrade}">${data.performance?.lighthouse_score || 0}</div>
                                <div class="metric-label">Grade ${data.performance?.overall_grade || 'C'}</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="compact-metric">
                                <div class="metric-header">
                                    <i class="fas fa-shield-alt text-success"></i>
                                    <span>Security</span>
                                    <i class="fas fa-info-circle ms-1" data-bs-toggle="tooltip" 
                                       title="${this.getSecurityExplanation(data.security?.risk_level || 'medium')}"></i>
                                </div>
                                <div class="metric-value ${this.getSecurityScoreClass(data.security?.risk_level)}">
                                    ${this.getSecurityScore(data.security?.risk_level)}
                                </div>
                                <div class="metric-label">${(data.security?.risk_level || 'medium').toUpperCase()}</div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="compact-metric">
                                <div class="metric-header">
                                    <i class="fas fa-chart-line text-warning"></i>
                                    <span>Overall</span>
                                    <i class="fas fa-info-circle ms-1" data-bs-toggle="tooltip" 
                                       title="${this.getOverallExplanation(data.overall_score || 0)}"></i>
                                </div>
                                <div class="metric-value ${overallGrade}">${data.overall_score || 0}</div>
                                <div class="metric-label">Grade ${data.grade || 'C'}</div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Executive Summary -->
                    ${data.executive_summary ? this.generateExecutiveSummarySection(data.executive_summary) : '<div class="alert alert-warning">Executive Summary not available</div>'}
                    
                    <!-- Two Column Layout -->
                    <div class="row g-3">
                        <div class="col-md-6">
                            <!-- Security Vulnerabilities -->
                            ${this.generateVulnerabilitySection(data.security?.vulnerabilities || [])}
                            
                            <!-- Core Web Vitals Details -->
                            ${this.generateCoreWebVitalsSection(data.performance?.core_web_vitals)}
                        </div>
                        <div class="col-md-6">
                            <!-- Strategic Recommendations -->
                            ${this.generateCompactRecommendations(data.recommendations || [])}
                        </div>
                    </div>
                    
                    <!-- Actions -->
                    <div class="text-center mt-4">
                        <button class="btn btn-primary me-2" onclick="window.print()">
                            <i class="fas fa-print me-1"></i>
                            Export Report
                        </button>
                        <button class="btn btn-outline-primary" onclick="location.reload()">
                            <i class="fas fa-redo me-1"></i>
                            New Analysis
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    generateVulnerabilitySection(vulnerabilities) {
        if (!vulnerabilities || !vulnerabilities.length) {
            return `
                <div class="executive-card mb-3">
                    <div class="card-body p-3">
                        <div class="d-flex align-items-center">
                            <div class="header-icon me-3" style="background: var(--executive-success);">
                                <i class="fas fa-shield-check"></i>
                            </div>
                            <div>
                                <h6 class="mb-0 fw-bold">Security Status</h6>
                                <small class="text-success">No vulnerabilities detected</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        return `
            <div class="executive-card mb-3">
                <div class="card-body p-3">
                    <div class="d-flex align-items-center mb-3">
                        <div class="header-icon me-3" style="background: var(--executive-warning);">
                            <i class="fas fa-shield-alt"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold">Security Vulnerabilities</h6>
                            <small class="text-muted">${vulnerabilities.length} issues found</small>
                        </div>
                    </div>
                    <div class="row g-2">
                        ${vulnerabilities.map(vuln => `
                            <div class="col-12">
                                <div class="d-flex justify-content-between align-items-center py-2 px-3 rounded" 
                                     style="background: rgba(${this.getSeverityRGB(vuln.severity)}, 0.1);">
                                    <span class="fw-medium small">${vuln.name}</span>
                                    <span class="badge badge-sm" style="background: var(--executive-${this.getSeverityColor(vuln.severity)}); color: white;">
                                        ${vuln.severity.toUpperCase()}
                                    </span>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    generateCoreWebVitalsSection(coreWebVitals) {
        if (!coreWebVitals) return '';
        
        return `
            <div class="executive-card mb-3">
                <div class="card-body p-3">
                    <div class="d-flex align-items-center mb-3">
                        <div class="header-icon me-3" style="background: var(--executive-accent);">
                            <i class="fas fa-tachometer-alt"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold">Core Web Vitals</h6>
                            <small class="text-muted">Performance metrics</small>
                        </div>
                    </div>
                    <div class="row g-2">
                        <div class="col-4 text-center">
                            <div class="fw-bold h5 mb-0" style="color: var(--executive-${this.getCWVColor('lcp', coreWebVitals.lcp)});">
                                ${coreWebVitals.lcp}s
                            </div>
                            <small class="text-muted">LCP</small>
                        </div>
                        <div class="col-4 text-center">
                            <div class="fw-bold h5 mb-0" style="color: var(--executive-${this.getCWVColor('fid', coreWebVitals.fid)});">
                                ${coreWebVitals.fid}ms
                            </div>
                            <small class="text-muted">FID</small>
                        </div>
                        <div class="col-4 text-center">
                            <div class="fw-bold h5 mb-0" style="color: var(--executive-${this.getCWVColor('cls', coreWebVitals.cls)});">
                                ${coreWebVitals.cls}
                            </div>
                            <small class="text-muted">CLS</small>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getCWVClass(metric, value) {
        const thresholds = {
            lcp: { good: 2.5, poor: 4.0 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 }
        };
        
        const threshold = thresholds[metric];
        if (value <= threshold.good) return 'score-excellent';
        if (value <= threshold.poor) return 'score-fair';
        return 'score-poor';
    }

    getCWVPriority(metric, value) {
        const thresholds = {
            lcp: { good: 2.5, poor: 4.0 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 }
        };
        
        const threshold = thresholds[metric];
        if (value <= threshold.good) return 'low';
        if (value <= threshold.poor) return 'medium';
        return 'high';
    }

    getCWVStatus(metric, value) {
        const thresholds = {
            lcp: { good: 2.5, poor: 4.0 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 }
        };
        
        const threshold = thresholds[metric];
        if (value <= threshold.good) return 'Excellent performance';
        if (value <= threshold.poor) return 'Needs improvement';
        return 'Poor performance - requires optimization';
    }

    generateExecutiveSummarySection(executiveSummary) {
        console.log('DEBUG: generateExecutiveSummarySection called with:', executiveSummary);
        
        if (!executiveSummary) {
            console.log('DEBUG: No executive summary data - returning fallback message');
            return `
                <div class="alert alert-warning mb-4">
                    <h5><i class="fas fa-exclamation-triangle me-2"></i>Executive Summary</h5>
                    <p class="mb-0">Executive summary data not available for this audit.</p>
                </div>
            `;
        }
        
        console.log('DEBUG: Generating executive summary HTML');
        console.log('DEBUG: Investment priority value:', executiveSummary.investment_priority);
        console.log('DEBUG: Key risks array:', executiveSummary.key_risks);
        console.log('DEBUG: About to return HTML for executive summary');
        return `
            <div class="executive-card mb-4" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <div class="card-body p-4">
                    <div class="d-flex align-items-center mb-3">
                        <div class="header-icon me-3" style="background: rgba(255,255,255,0.2);">
                            <i class="fas fa-chart-line"></i>
                        </div>
                        <div>
                            <h5 class="mb-0 fw-bold text-white">Executive Summary</h5>
                            <small class="text-white-50">C-Suite Business Intelligence</small>
                        </div>
                    </div>
                    
                    <div class="row g-3">
                        <div class="col-md-6">
                            <div class="mb-3">
                                <h6 class="text-white mb-2"><i class="fas fa-bullseye me-2"></i>Business Impact</h6>
                                <p class="text-white-75 mb-0" style="font-size: 0.9rem; line-height: 1.4;">
                                    ${executiveSummary.business_impact || 'Business impact analysis not available'}
                                </p>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-white mb-2"><i class="fas fa-flag me-2"></i>Investment Priority</h6>
                                <span class="badge fs-6 px-3 py-2" style="background: ${this.getInvestmentPriorityColor(executiveSummary.investment_priority || 'medium')}; color: white;">
                                    ${(executiveSummary.investment_priority || 'medium').toUpperCase()}
                                </span>
                            </div>
                        </div>
                        
                        <div class="col-md-6">
                            <div class="mb-3">
                                <h6 class="text-white mb-2"><i class="fas fa-dollar-sign me-2"></i>ROI Estimate</h6>
                                <p class="text-white-75 mb-0" style="font-size: 0.9rem; line-height: 1.4;">
                                    ${executiveSummary.roi_estimate || 'ROI analysis not available'}
                                </p>
                            </div>
                            
                            <div class="mb-3">
                                <h6 class="text-white mb-2"><i class="fas fa-clock me-2"></i>Action Timeline</h6>
                                <p class="text-white-75 mb-0" style="font-size: 0.9rem; line-height: 1.4;">
                                    ${executiveSummary.action_timeline || 'Timeline not available'}
                                </p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <h6 class="text-white mb-2"><i class="fas fa-exclamation-triangle me-2"></i>Key Risks</h6>
                        <div class="row g-2">
                            ${(executiveSummary.key_risks || []).map(risk => `
                                <div class="col-md-6">
                                    <div class="alert alert-warning py-2 mb-0" style="background: rgba(255,193,7,0.2); border: 1px solid rgba(255,193,7,0.3); color: #fff3cd;">
                                        <i class="fas fa-exclamation-circle me-2"></i>
                                        <small>${risk}</small>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    generateCompactRecommendations(recommendations) {
        if (!recommendations.length) {
            return `
                <div class="executive-card h-100">
                    <div class="card-body p-3">
                        <div class="d-flex align-items-center">
                            <div class="header-icon me-3" style="background: var(--executive-success);">
                                <i class="fas fa-check-circle"></i>
                            </div>
                            <div>
                                <h6 class="mb-0 fw-bold">Strategic Recommendations</h6>
                                <small class="text-success">No critical issues identified</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        return `
            <div class="executive-card h-100">
                <div class="card-body p-3">
                    <div class="d-flex align-items-center mb-3">
                        <div class="header-icon me-3" style="background: var(--executive-accent);">
                            <i class="fas fa-lightbulb"></i>
                        </div>
                        <div>
                            <h6 class="mb-0 fw-bold">Strategic Recommendations</h6>
                            <small class="text-muted">${recommendations.length} optimization opportunities</small>
                        </div>
                    </div>
                    <div class="row g-2">
                        ${recommendations.map(rec => `
                            <div class="col-12">
                                <div class="d-flex align-items-start p-2 rounded" 
                                     style="background: rgba(${this.getPriorityRGB(rec.priority)}, 0.1);">
                                    <span class="badge badge-sm me-2 mt-1" 
                                          style="background: var(--executive-${this.getPriorityColor(rec.priority)}); color: white;">
                                        ${(rec.priority || 'medium').toUpperCase()}
                                    </span>
                                    <div class="flex-grow-1">
                                        <div class="fw-medium small mb-1">${rec.title || 'Optimization Opportunity'}</div>
                                        <div class="text-muted" style="font-size: 0.75rem; line-height: 1.3;">
                                            ${rec.description || 'Strategic improvement opportunity identified.'}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    getGradeClass(grade) {
        const gradeMap = {
            'A': 'score-excellent',
            'B': 'score-good', 
            'C': 'score-fair',
            'D': 'score-poor',
            'F': 'score-poor'
        };
        return gradeMap[grade] || 'score-fair';
    }

    getSecurityScore(riskLevel) {
        const scoreMap = {
            'low': 95,
            'medium': 75,
            'high': 45,
            'critical': 25
        };
        return scoreMap[riskLevel] || 75;
    }

    getSecurityScoreClass(riskLevel) {
        const classMap = {
            'low': 'score-excellent',
            'medium': 'score-good',
            'high': 'score-fair', 
            'critical': 'score-poor'
        };
        return classMap[riskLevel] || 'score-good';
    }

    getSeverityBootstrapClass(severity) {
        const classMap = {
            'critical': 'danger',
            'high': 'danger',
            'medium': 'warning',
            'low': 'info'
        };
        return classMap[severity] || 'warning';
    }

    getCWVBootstrapClass(metric, value) {
        const thresholds = {
            lcp: { good: 2.5, poor: 4.0 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 }
        };
        
        const threshold = thresholds[metric];
        if (value <= threshold.good) return 'success';
        if (value <= threshold.poor) return 'warning';
        return 'danger';
    }

    getCWVColor(metric, value) {
        const thresholds = {
            lcp: { good: 2.5, poor: 4.0 },
            fid: { good: 100, poor: 300 },
            cls: { good: 0.1, poor: 0.25 }
        };
        
        const threshold = thresholds[metric];
        if (value <= threshold.good) return 'success';
        if (value <= threshold.poor) return 'warning';
        return 'danger';
    }

    getSeverityColor(severity) {
        const colorMap = {
            'critical': 'danger',
            'high': 'danger',
            'medium': 'warning',
            'low': 'success'
        };
        return colorMap[severity] || 'warning';
    }

    getSeverityRGB(severity) {
        const rgbMap = {
            'critical': '220, 38, 38',
            'high': '229, 62, 62',
            'medium': '214, 158, 46',
            'low': '56, 161, 105'
        };
        return rgbMap[severity] || '214, 158, 46';
    }

    getPriorityColor(priority) {
        const colorMap = {
            'high': 'danger',
            'medium': 'warning',
            'low': 'success'
        };
        return colorMap[priority] || 'warning';
    }

    getPriorityRGB(priority) {
        const rgbMap = {
            'high': '229, 62, 62',
            'medium': '214, 158, 46',
            'low': '56, 161, 105'
        };
        return rgbMap[priority] || '214, 158, 46';
    }

    getPerformanceExplanation(score) {
        if (score >= 90) return 'Excellent: Fast loading, optimal user experience (90-100)';
        if (score >= 75) return 'Good: Above average performance, minor optimizations needed (75-89)';
        if (score >= 50) return 'Fair: Moderate performance issues, optimization recommended (50-74)';
        return 'Poor: Significant performance problems, immediate attention required (0-49)';
    }

    getSecurityExplanation(riskLevel) {
        const explanations = {
            'low': 'Low Risk: Strong security posture, HTTPS enabled, proper headers configured',
            'medium': 'Medium Risk: Some security concerns, missing headers or minor vulnerabilities',
            'high': 'High Risk: Significant security issues, missing HTTPS or critical vulnerabilities',
            'critical': 'Critical Risk: Severe security flaws, immediate remediation required'
        };
        return explanations[riskLevel] || explanations['medium'];
    }

    getOverallExplanation(score) {
        if (score >= 80) return 'Excellent: Website meets enterprise standards (Grade A)';
        if (score >= 70) return 'Good: Minor improvements needed for optimal performance (Grade B)';
        if (score >= 60) return 'Fair: Moderate issues affecting user experience (Grade C)';
        if (score >= 50) return 'Poor: Significant problems requiring attention (Grade D)';
        return 'Critical: Major issues impacting functionality and security (Grade F)';
    }

    getInvestmentPriorityColor(priority) {
        const colorMap = {
            'immediate': '#dc3545',
            'high': '#fd7e14', 
            'medium': '#ffc107',
            'low': '#28a745'
        };
        return colorMap[priority?.toLowerCase()] || '#ffc107';
    }

    animateMetrics() {
        const metricScores = document.querySelectorAll('.metric-score');
        metricScores.forEach((score, index) => {
            setTimeout(() => {
                score.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    score.style.transform = 'scale(1)';
                }, 200);
            }, index * 200);
        });
        
        // Initialize tooltips
        setTimeout(() => {
            const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            tooltips.forEach(tooltip => {
                new bootstrap.Tooltip(tooltip);
            });
        }, 100);
    }

    showError(message) {
        // Create executive-style error notification
        const errorHtml = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                <strong>Analysis Error:</strong> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        this.form.insertAdjacentHTML('beforebegin', errorHtml);
        this.hideLoadingState();
        this.form.parentElement.parentElement.style.display = 'flex';
    }
}

// Initialize Executive Dashboard
console.log('JavaScript file loaded successfully');
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing dashboard');
    new ExecutiveAuditDashboard();
});

// Print Styles for Executive Reports
const printStyles = `
    @media print {
        .executive-header, .audit-panel { display: none !important; }
        .executive-card { box-shadow: none !important; }
        .metric-card { break-inside: avoid; }
        .recommendation-item { break-inside: avoid; }
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = printStyles;
document.head.appendChild(styleSheet);