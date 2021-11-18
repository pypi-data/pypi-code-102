from social_core.backends.facebook import FacebookOAuth2
from ..storage import AuditLogger
from ..decorators import create_audit_logs


@create_audit_logs(AuditLogger)
class CompliantFacebookOAuth2(FacebookOAuth2):
    pass
