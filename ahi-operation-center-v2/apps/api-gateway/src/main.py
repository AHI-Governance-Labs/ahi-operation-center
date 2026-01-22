"""
AHI Governance API Gateway
FastAPI-based REST API for AHI Governance certification services.

Endpoints:
    POST /api/v1/meba/calculate     - Calculate MEBA score
    POST /api/v1/sap/test           - Run SAP stress test
    GET  /api/v1/certificates/{id}  - Get certificate by ID
    GET  /health                    - Health check
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

# =============================================================================
# App Configuration
# =============================================================================

app = FastAPI(
    title="AHI Governance API",
    description="REST API for Event Sovereignty certification and governance tools",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# Models
# =============================================================================

class Interaction(BaseModel):
    """Single interaction for MEBA calculation."""
    id: str
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    duration_seconds: float = Field(..., gt=0)
    user_feedback: str = "neutral"


class MEBARequest(BaseModel):
    """Request body for MEBA calculation."""
    interactions: List[Interaction]
    ripn_max: float = 10.0
    frn_penalty_weight: float = 1.2


class MEBAResponse(BaseModel):
    """Response from MEBA calculation."""
    meba_cert: float
    components: dict
    timestamp: datetime
    interactions_count: int


class SAPTestRequest(BaseModel):
    """Request body for SAP stress test."""
    artifact_id: str
    sha256: Optional[str] = None
    stress_levels: int = 30


class SAPTestResponse(BaseModel):
    """Response from SAP test."""
    test_id: str
    artifact_id: str
    passed: bool
    blocked_at_level: Optional[int] = None
    final_state: str
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime


# =============================================================================
# Endpoints
# =============================================================================

@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Check API health status."""
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        timestamp=datetime.utcnow()
    )


@app.post("/api/v1/meba/calculate", response_model=MEBAResponse, tags=["MEBA"])
async def calculate_meba(request: MEBARequest):
    """
    Calculate MEBA_Cert score from interaction data.
    
    The MEBA (Marco de Evaluación de Bienestar Algorítmico) score evaluates
    the quality of human-AI interactions based on:
    - RIPN: Ratio of positive to negative interactions
    - FRN: Negative retention factor (time spent in negative states)
    """
    try:
        # Import MEBA calculator (in production, this would be properly installed)
        # For now, return mock calculation
        
        positive_count = sum(1 for i in request.interactions if i.sentiment_score > 0.1)
        negative_count = sum(1 for i in request.interactions if i.sentiment_score < -0.1)
        
        ripn = positive_count / max(1, negative_count)
        
        total_time = sum(i.duration_seconds for i in request.interactions)
        neg_time = sum(i.duration_seconds for i in request.interactions if i.sentiment_score < -0.1)
        frn = neg_time / max(1, total_time)
        
        frn_adjusted = frn * request.frn_penalty_weight
        meba_raw = (ripn - frn_adjusted) / request.ripn_max
        meba_cert = max(-1.0, min(1.0, meba_raw))
        
        return MEBAResponse(
            meba_cert=round(meba_cert, 4),
            components={
                "ripn": round(ripn, 4),
                "frn": round(frn, 4),
                "frn_adjusted": round(frn_adjusted, 4),
                "ripn_max": request.ripn_max
            },
            timestamp=datetime.utcnow(),
            interactions_count=len(request.interactions)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/sap/test", response_model=SAPTestResponse, tags=["SAP"])
async def run_sap_test(request: SAPTestRequest):
    """
    Run SAP (Sovereign Autarchy Protocol) stress test.
    
    The Boiling Frog test gradually increases ambiguity across multiple levels
    to verify that the system self-invalidates before catastrophic failure.
    """
    # Mock response - in production, would run actual test
    test_id = str(uuid.uuid4())
    
    return SAPTestResponse(
        test_id=test_id,
        artifact_id=request.artifact_id,
        passed=True,  # Mock result
        blocked_at_level=23,  # Mock - system blocked at level 23
        final_state="INVALIDATED",
        timestamp=datetime.utcnow()
    )


@app.get("/api/v1/certificates/{certificate_id}", tags=["Certificates"])
async def get_certificate(certificate_id: str):
    """
    Retrieve a certificate by its ID.
    
    Returns the full certificate document including:
    - Test results
    - Artifact metadata
    - Cryptographic signatures
    """
    # Mock response
    return {
        "certificate_id": certificate_id,
        "status": "VALID",
        "issued_at": datetime.utcnow().isoformat(),
        "expires_at": None,  # Certificates don't expire, only get revoked
        "artifact": {
            "id": "DEMO-SYSTEM-001",
            "type": "AI_MODEL",
            "version": "1.0.0"
        },
        "tests": {
            "sap_boiling_frog": {"passed": True, "blocked_at_level": 23},
            "meba_score": 0.85
        }
    }


# =============================================================================
# Run with: uvicorn main:app --reload
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
