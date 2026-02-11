from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import datetime, uuid

Base = declarative_base()

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_storage_key = Column(String, unique=True, nullable=False)
    filename = Column(String, nullable=False)
    mime_type = Column(String, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    etag = Column(String, nullable=False)
    current_version_id = Column(UUID(as_uuid=True), nullable=True)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class AssetVersion(Base):
    __tablename__ = 'asset_versions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id'))
    object_storage_key = Column(String, unique=True, nullable=False)
    etag = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AccessToken(Base):
    __tablename__ = 'access_tokens'
    token = Column(String, primary_key=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey('assets.id'))
    expires_at = Column(DateTime, nullable=False)