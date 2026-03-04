from __future__ import annotations

from datetime import date, datetime
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# -------------------------
# Helpers
# -------------------------
def _normalize_str(v: Optional[str]) -> Optional[str]:
    if v is None:
        return None
    v = v.strip()
    if v == "" or v == "-":
        return None
    return v


# -------------------------
# InputSchema (RAW)
# -------------------------
class InputSchema(BaseModel):
    """
    Representa UNA FILA del dataset original (antes de limpieza).
    Campos en formato ya estandarizado: lower + underscore.
    """

    model_config = ConfigDict(extra="ignore", str_strip_whitespace=True)

    athlete_id: str
    athlete_name: Optional[str] = None
    gender: Optional[Literal["Male", "Female"]] = None

    age: Optional[int] = Field(default=None, ge=0, le=120)
    date_of_birth: Optional[date] = None

    nationality: Optional[str] = None
    country_name: Optional[str] = None

    sport: Optional[str] = None
    event: Optional[str] = None
    games_type: Optional[Literal["Summer", "Winter"]] = None

    year: Optional[int] = Field(default=None, ge=1800, le=2100)
    host_city: Optional[str] = None
    team_or_individual: Optional[str] = None

    medal: Optional[str] = None

    result_value: Optional[float] = None
    result_unit: Optional[str] = None

    total_olympics_attended: Optional[int] = Field(default=None, ge=0, le=50)
    total_medals_won: Optional[int] = Field(default=None, ge=0, le=200)
    gold_medals: Optional[int] = Field(default=None, ge=0, le=200)
    silver_medals: Optional[int] = Field(default=None, ge=0, le=200)
    bronze_medals: Optional[int] = Field(default=None, ge=0, le=200)

    country_total_gold: Optional[int] = Field(default=None, ge=0)
    country_total_medals: Optional[int] = Field(default=None, ge=0)
    country_first_participation: Optional[int] = Field(default=None, ge=1800, le=2100)
    country_best_rank: Optional[int] = Field(default=None, ge=1)

    is_record_holder: Optional[str] = None
    coach_name: Optional[str] = None

    height_cm: Optional[float] = Field(default=None, ge=0, le=300)
    weight_kg: Optional[float] = Field(default=None, ge=0, le=500)

    notes: Optional[str] = None

    # --- Validators (input) ---
    @field_validator(
        "athlete_name",
        "nationality",
        "country_name",
        "sport",
        "event",
        "host_city",
        "team_or_individual",
        "medal",
        "result_unit",
        "is_record_holder",
        "coach_name",
        "notes",
        mode="before",
    )
    @classmethod
    def normalize_strings(cls, v):
        return _normalize_str(v)

    @field_validator("date_of_birth", mode="before")
    @classmethod
    def parse_date(cls, v):
        # acepta "YYYY-MM-DD" y datetime
        if v is None or v == "":
            return None
        if isinstance(v, date) and not isinstance(v, datetime):
            return v
        if isinstance(v, datetime):
            return v.date()
        if isinstance(v, str):
            try:
                return datetime.strptime(v.strip(), "%Y-%m-%d").date()
            except ValueError:
                return None
        return None


# -------------------------
# OutputSchema (CLEAN)
# -------------------------
class OutputSchema(InputSchema):
    """
    Fila ya limpia. Reutilizamos campos del InputSchema y añadimos `has_medal`.
    """
    has_medal: Optional[bool] = None