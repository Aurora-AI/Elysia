import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
import os


def init_error_tracking():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[FastApiIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv("ENVIRONMENT", "development"),
    )
