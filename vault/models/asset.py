import uuid
from datetime import datetime, timezone
from extensions import db


class Asset(db.Model):
    __tablename__ = "asset"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    application_id = db.Column(db.String(36), db.ForeignKey("application.id"), nullable=False, index=True)

    name = db.Column(db.String(150), nullable=False)
    identifier = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False, index=True)
    status = db.Column(db.String(30), nullable=False, default="active", index=True)
    description = db.Column(db.Text)

    original_filename = db.Column(db.String(255))
    mime_type = db.Column(db.String(150))
    size_bytes = db.Column(db.BigInteger)
    storage_provider = db.Column(db.String(50))
    storage_key = db.Column(db.Text)
    checksum_sha256 = db.Column(db.String(64), index=True)

    analysis_status = db.Column(db.String(30), nullable=False, default="pending", index=True)
    analysis_metadata = db.Column(db.JSON)
    last_analyzed_at = db.Column(db.DateTime(timezone=True))

    metadata_ = db.Column("metadata", db.JSON)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    application = db.relationship("Application", back_populates="assets")
    events = db.relationship("Event", back_populates="asset")
    vulnerabilities = db.relationship("Vulnerability", back_populates="asset")
    alerts = db.relationship("Alert", back_populates="asset")
    audit_logs = db.relationship("AuditLog", back_populates="asset")

    __table_args__ = (
        db.UniqueConstraint("application_id", "identifier", name="uq_asset_application_identifier"),
    )
