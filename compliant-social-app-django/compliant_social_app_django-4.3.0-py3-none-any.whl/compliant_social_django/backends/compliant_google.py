from social_core.backends.google import GoogleOAuth2
from ..storage import AuditLogger
from ..decorators import create_audit_logs


@create_audit_logs(AuditLogger)
class CompliantGoogleOAuth2(GoogleOAuth2):
    pass
