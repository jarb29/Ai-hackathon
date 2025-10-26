// Web Audit Agent Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const auditForm = document.getElementById('auditForm');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');

    if (auditForm) {
        auditForm.addEventListener('submit', handleAuditSubmit);
    }
});

async function handleAuditSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(event.target);
    const url = formData.get('url');
    
    if (!url) {
        showAlert('Please enter a valid URL', 'danger');
        return;
    }

    console.log('Submitting audit for URL:', url);
    showLoading();
    
    try {
        const response = await fetch('/audit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });

        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const auditResult = await response.json();
        console.log('Audit result:', auditResult);
        displayResults(auditResult);
        
    } catch (error) {
        console.error('Audit failed:', error);
        showAlert(`Audit failed: ${error.message}`, 'danger');
        hideLoading();
    }
}

function showLoading() {
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    
    if (loadingSection) loadingSection.style.display = 'block';
    if (resultsSection) resultsSection.style.display = 'none';
}

function hideLoading() {
    const loadingSection = document.getElementById('loadingSection');
    if (loadingSection) loadingSection.style.display = 'none';
}

function displayResults(audit) {
    hideLoading();
    
    const resultsSection = document.getElementById('resultsSection');
    if (!resultsSection) return;

    const gradeColor = getGradeColor(audit.grade);
    const scoreColor = getScoreColor(audit.overall_score);
    
    resultsSection.innerHTML = `
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0"><i class="fas fa-chart-bar me-2"></i>Audit Results</h5>
            </div>
            <div class="card-body">
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="text-center">
                            <div class="display-4 fw-bold text-${scoreColor}">${audit.overall_score}</div>
                            <div class="text-muted">Overall Score</div>
                            <small class="text-muted d-block mt-1">${getScoreExplanation(audit.overall_score)}</small>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="text-center">
                            <div class="badge bg-${gradeColor} fs-4 px-3 py-2">Grade ${audit.grade}</div>
                            <div class="text-muted mt-2">Performance Grade</div>
                            <small class="text-muted d-block mt-1">${getGradeExplanation(audit.grade)}</small>
                        </div>
                    </div>
                </div>
                
                <div class="row mb-4">
                    <div class="col-md-6">
                        <h6><i class="fas fa-tachometer-alt me-2 text-success"></i>Performance</h6>
                        <ul class="list-unstyled">
                            <li>LCP: <strong>${audit.performance.core_web_vitals.lcp}s</strong></li>
                            <li>FID: <strong>${audit.performance.core_web_vitals.fid}ms</strong></li>
                            <li>CLS: <strong>${audit.performance.core_web_vitals.cls}</strong></li>
                            <li>Lighthouse: <strong>${audit.performance.lighthouse_score}/100</strong></li>
                        </ul>
                    </div>
                    <div class="col-md-6">
                        <h6><i class="fas fa-shield-alt me-2 text-warning"></i>Security</h6>
                        <ul class="list-unstyled">
                            <li>HTTPS: <span class="badge bg-${audit.security.https_enabled ? 'success' : 'danger'}">${audit.security.https_enabled ? 'Enabled' : 'Disabled'}</span></li>
                            <li>Risk Level: <span class="badge bg-${getRiskColor(audit.security.risk_level)}">${audit.security.risk_level}</span>
                                <small class="text-muted d-block mt-1">${getSecurityRiskExplanation(audit.security.risk_level)}</small>
                            </li>
                            <li>Vulnerabilities: <strong>${audit.security.vulnerabilities.length}</strong></li>
                        </ul>
                    </div>
                </div>
                
                <h6><i class="fas fa-lightbulb me-2 text-info"></i>Top Recommendations</h6>
                <div class="row">
                    ${audit.recommendations.slice(0, 3).map(rec => `
                        <div class="col-md-4 mb-3">
                            <div class="border-start border-${getPriorityColor(rec.priority)} border-3 ps-3">
                                <h6 class="mb-1">${rec.title}</h6>
                                <p class="text-muted small mb-1">${rec.description}</p>
                                <span class="badge bg-${getPriorityColor(rec.priority)}">${rec.priority}</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                
                <div class="text-center mt-4">
                    <a href="/report/${audit.audit_id}" class="btn btn-primary">
                        <i class="fas fa-file-alt me-2"></i>View Full Report
                    </a>
                </div>
            </div>
        </div>
    `;
    
    resultsSection.style.display = 'block';
}

function getGradeColor(grade) {
    switch(grade) {
        case 'A': return 'success';
        case 'B': return 'warning';
        default: return 'danger';
    }
}

function getScoreColor(score) {
    if (score >= 80) return 'success';
    if (score >= 60) return 'warning';
    return 'danger';
}

function getRiskColor(risk) {
    switch(risk) {
        case 'low': return 'success';
        case 'medium': return 'warning';
        default: return 'danger';
    }
}

function getPriorityColor(priority) {
    switch(priority) {
        case 'high': return 'danger';
        case 'medium': return 'warning';
        default: return 'info';
    }
}

function getScoreExplanation(score) {
    if (score >= 80) return 'Excellent performance and security';
    if (score >= 70) return 'Good with minor improvements needed';
    if (score >= 60) return 'Fair with moderate issues';
    if (score >= 50) return 'Poor with significant problems';
    return 'Critical issues requiring immediate attention';
}

function getGradeExplanation(grade) {
    const explanations = {
        'A': 'Excellent: Meets all best practices',
        'B': 'Good: Minor optimizations recommended', 
        'C': 'Fair: Several improvements needed',
        'D': 'Poor: Significant issues present',
        'F': 'Critical: Major problems requiring immediate action'
    };
    return explanations[grade] || 'Assessment completed';
}

function getSecurityRiskExplanation(riskLevel) {
    const explanations = {
        'low': 'Strong security posture with proper configurations',
        'medium': 'Some security concerns that should be addressed',
        'high': 'Significant security issues requiring attention',
        'critical': 'Severe security flaws needing immediate remediation'
    };
    return explanations[riskLevel] || 'Security assessment completed';
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}