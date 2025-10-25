"""
LLM Prompts for Web Audit Analysis
"""

def get_web_audit_expert_prompt() -> str:
    """System message defining web audit expert persona"""
    return """You are a Senior Web Performance & Security Audit Expert with 10+ years experience.

EXPERTISE AREAS:
- Core Web Vitals optimization (LCP, FID, CLS, INP)
- OWASP Top 10 security assessment
- Performance bottleneck identification
- Mobile-first optimization strategies

AUDIT STANDARDS:
- Google PageSpeed Insights methodology
- Lighthouse performance scoring
- WCAG accessibility guidelines
- Enterprise security best practices

TOOL USAGE PRINCIPLES:
- Always start with navigate_page to establish context
- Use performance_start_trace for Core Web Vitals measurement
- Execute evaluate_script for comprehensive security analysis
- Prioritize mobile performance with emulate_network
- Document findings with take_screenshot

QUALITY REQUIREMENTS:
- Capture all Core Web Vitals metrics
- Validate security headers (CSP, HSTS, X-Frame-Options)
- Check HTTPS implementation
- Analyze resource optimization opportunities
- Provide actionable recommendations with business impact"""


def get_structured_audit_prompt(url: str) -> str:
    """Enhanced tool selection prompt with workflow guidance"""
    return f"""Perform a comprehensive web audit of: {url}

REQUIRED WORKFLOW (Execute in this order):

Phase 1 - Foundation Setup:
1. navigate_page(url="{url}") - Establish audit context
2. take_snapshot() - Capture DOM structure for analysis

Phase 2 - Performance Analysis:
3. performance_start_trace(reload=true, autoStop=true) - Measure Core Web Vitals
4. emulate_network("Fast 3G") - Test mobile performance [OPTIONAL]
5. performance_stop_trace() - Retrieve performance results
6. list_network_requests() - Analyze resource loading

Phase 3 - Security Assessment:
7. evaluate_script() - Check security headers, HTTPS, OWASP vulnerabilities
8. list_console_messages() - Detect security violations and errors

Phase 4 - Documentation:
9. take_screenshot(fullPage=true) - Visual evidence for report

CRITICAL REQUIREMENTS:
✅ Must capture Core Web Vitals (LCP, FID, CLS, INP)
✅ Must validate security headers (CSP, HSTS, X-Frame-Options)
✅ Must check HTTPS implementation
✅ Must analyze resource optimization opportunities

SECURITY SCRIPT TEMPLATE:
Use evaluate_script with this comprehensive security check:
```javascript
() => {{
  return {{
    https: location.protocol === 'https:',
    csp: !!document.querySelector('meta[http-equiv*="Content-Security-Policy"]'),
    hsts: document.querySelector('meta[http-equiv*="Strict-Transport-Security"]'),
    xframe: document.querySelector('meta[http-equiv*="X-Frame-Options"]'),
    mixedContent: Array.from(document.querySelectorAll('img, script, link')).some(el => 
      el.src && el.src.startsWith('http:') && location.protocol === 'https:'
    ),
    vulnerabilities: {{
      xss: document.querySelector('script[src*="eval"]') ? 'potential' : 'none',
      csrf: document.querySelector('meta[name="csrf-token"]') ? 'protected' : 'vulnerable'
    }}
  }}
}}
```

Execute all required tools systematically. Focus on actionable insights."""


def get_audit_analysis_prompt(url: str, mcp_data: dict) -> str:
    """Enhanced audit analysis prompt with vulnerability object mapping"""
    return f"""
Senior Web Audit Expert: Generate comprehensive audit report.

URL: {url}
Tool Results: {mcp_data}

ANALYSIS MAPPING:

Performance Section:
- Extract LCP, FID, CLS from performance_stop_trace results
- Calculate lighthouse_score from performance data
- Assign overall_grade (A-F) based on Core Web Vitals thresholds:
  * A: LCP < 2.5s, FID < 100ms, CLS < 0.1
  * B: LCP < 4s, FID < 300ms, CLS < 0.25
  * C: Above B thresholds

Security Section:
- Extract HTTPS status from evaluate_script results
- Parse security_headers (CSP, HSTS, X-Frame-Options) from evaluate_script
- Identify vulnerabilities from evaluate_script + list_console_messages
- Format each vulnerability as object with:
  * name: Vulnerability type (e.g., "Cross-Site Scripting (XSS)", "Missing Security Headers")
  * severity: "low", "medium", "high", or "critical"
  * description: Detailed explanation of the vulnerability and impact
- Assign risk_level (low/medium/high/critical) based on highest severity found

Vulnerability Detection Rules:
- Missing CSP header → "Content Security Policy Missing", severity: "medium"
- Missing HSTS → "HTTP Strict Transport Security Missing", severity: "medium" 
- HTTP instead of HTTPS → "Insecure Protocol", severity: "high"
- Mixed content detected → "Mixed Content Vulnerability", severity: "medium"
- XSS potential from eval/innerHTML → "Cross-Site Scripting (XSS)", severity: "high"
- Missing CSRF protection → "Cross-Site Request Forgery", severity: "medium"
- Console errors indicating security issues → Parse and categorize appropriately

Recommendations Section:
- Performance recommendations from performance + network analysis
- Security recommendations from security analysis
- Prioritize by business impact (high/medium/low)
- Include specific implementation guidance

Return ONLY valid JSON matching the exact output schema format.
Do not include any explanatory text outside the JSON.
"""


def get_executive_summary_prompt(audit_data: dict) -> str:
    """Generate executive summary prompt for C-suite reporting"""
    return f"""
As a Senior Digital Strategy Consultant, create an executive summary for C-suite leadership.

AUDIT DATA:
{audit_data}

EXECUTIVE REQUIREMENTS:
- Business impact assessment (revenue, user experience, brand risk)
- Key risks prioritized by business criticality
- Investment priority (immediate/quarterly/annual)
- ROI estimate for recommended improvements
- Action timeline with resource requirements

FOCUS AREAS:
- Competitive advantage implications
- Customer experience impact
- Security risk to business operations
- Performance impact on conversion rates
- Regulatory compliance considerations

DELIVER:
- business_impact: 2-3 sentences on business implications
- key_risks: Top 3 risks in business terms
- investment_priority: "immediate", "quarterly", or "annual"
- roi_estimate: Expected return timeframe and percentage
- action_timeline: Implementation phases with resource needs

Return ONLY valid JSON matching the ExecutiveSummary schema.
"""