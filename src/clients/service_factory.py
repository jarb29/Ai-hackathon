from business.audit_logic import AuditService


def get_audit_service() -> AuditService:
    """Factory function to create AuditService instance"""
    return AuditService()