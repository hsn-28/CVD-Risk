"""
Configuration settings for CVD prediction backend
"""

from pathlib import Path
import os


class Settings:
    """Application settings"""

    # Project paths - check if /app exists (Docker) or use local path
    if Path("/app").exists():
        PROJECT_ROOT = Path("/app")
    else:
        PROJECT_ROOT = Path(__file__).parent.parent.parent
    BACKEND_ROOT = PROJECT_ROOT / "backend"
    WEIGHTS_DIR = Path(os.getenv("WEIGHTS_DIR", PROJECT_ROOT / "weights"))
    LEGACY_WEIGHTS_DIR = PROJECT_ROOT / "pth"

    # Model checkpoint paths
    HTN_CHECKPOINT = WEIGHTS_DIR / "hypertension.pt"
    CIMT_CHECKPOINT = WEIGHTS_DIR / "cimt_reg.pth"
    VESSEL_CHECKPOINT = WEIGHTS_DIR / "vessel.pth"
    FUSION_CHECKPOINT = WEIGHTS_DIR / "fusion_cvd_notskewed.pth"

    # Normalization statistics
    NORMALIZATION_STATS_PATH = BACKEND_ROOT / "normalization_stats.pkl"

    # Device
    DEVICE = os.getenv("DEVICE", "cuda")  # or "cpu"

    # Runtime flags
    USE_DUMMY_MODEL = os.getenv("USE_DUMMY_MODEL", "0") == "1"
    ENABLE_METRICS = os.getenv("ENABLE_METRICS", "0") == "1"
    MODEL_VERSION = os.getenv("MODEL_VERSION", "demo")

    # API settings
    API_TITLE = "CVD Risk Prediction API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "Cardiovascular disease risk prediction from retinal fundus images"

    # Image settings
    MAX_IMAGE_SIZE_MB = 10
    ALLOWED_IMAGE_FORMATS = {'png', 'jpg', 'jpeg'}

    # Feature dimensions
    HTN_FEATURES = 1025
    CIMT_FEATURES = 129
    VESSEL_FEATURES = 271
    FUSION_FEATURES = 1425

    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    def resolve_model_paths(self):
        """Resolve model paths with legacy fallback."""

        required_paths = {
            'HTN': self.HTN_CHECKPOINT,
            'CIMT': self.CIMT_CHECKPOINT,
            'Vessel': self.VESSEL_CHECKPOINT,
            'Fusion': self.FUSION_CHECKPOINT,
        }

        resolved = {}
        for name, path in required_paths.items():
            if path.exists():
                resolved[name] = path
                continue
            legacy_path = self.LEGACY_WEIGHTS_DIR / path.name
            resolved[name] = legacy_path if legacy_path.exists() else path

        return resolved

    def validate_model_paths(self):
        """Validate that all required model files exist"""

        required_paths = self.resolve_model_paths()
        missing = []
        for name, path in required_paths.items():
            if not path.exists():
                missing.append(f"{name}: {path}")

        if missing:
            msg = (
                "Missing model files:\n"
                + "\n".join(missing)
                + "\n\nRun: python scripts/check_weights.py"
            )
            raise FileNotFoundError(msg)

    def __repr__(self):
        return (
            f"Settings(\n"
            f"  HTN: {self.HTN_CHECKPOINT}\n"
            f"  CIMT: {self.CIMT_CHECKPOINT}\n"
            f"  Vessel: {self.VESSEL_CHECKPOINT}\n"
            f"  Fusion: {self.FUSION_CHECKPOINT}\n"
            f"  Stats: {self.NORMALIZATION_STATS_PATH}\n"
            f"  Device: {self.DEVICE}\n"
            f")"
        )


# Global settings instance
settings = Settings()
