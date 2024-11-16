from ..models.stunting import Stunting
from ..models.anak import Anak
from .. import db
from decimal import Decimal

standar_tinggi_badan = {
    0: {"male": 49.4, "female": 48.6},
    1: {"male": 76.1, "female": 75.0},
    2: {"male": 85.5, "female": 84.5},
    3: {"male": 94.1, "female": 93.2},
    4: {"male": 102.4, "female": 101.4},
    5: {"male": 109.6, "female": 108.5},
    6: {"male": 116.3, "female": 115.0},
    7: {"male": 122.0, "female": 120.6},
}

standar_berat_badan = {
    0: {"male": 3.3, "female": 3.2},
    1: {"male": 10.2, "female": 9.8},
    2: {"male": 12.1, "female": 11.6},
    3: {"male": 14.0, "female": 13.5},
    4: {"male": 15.6, "female": 15.1},
    5: {"male": 17.1, "female": 16.5},
    6: {"male": 18.5, "female": 17.9},
    7: {"male": 19.9, "female": 19.2},
}

def check_stunting(anak_id):
    stunting_data = (
        db.session.query(Stunting)
        .filter_by(anak_id=anak_id)
        .order_by(Stunting.date.desc())
        .first()
    )

    if not stunting_data:
        return "Data tidak lengkap"

    anak_data = db.session.query(Anak).filter_by(id=anak_id).first()
    if not anak_data:
        return "Data anak tidak ditemukan"

    age_in_years = anak_data.age
    age_in_years = min(7, max(0, age_in_years))

    gender = anak_data.gender
    standar_tinggi = Decimal(standar_tinggi_badan[age_in_years][gender])
    standar_berat = Decimal(standar_berat_badan[age_in_years][gender])

    ipb = (Decimal(stunting_data.height) / standar_tinggi) * 100
    imt = (Decimal(stunting_data.weight) / standar_berat) * 100

    result = ""

    if ipb < 80:
        result += f"IPB: {ipb:.2f}% - Anak mengalami stunting berdasarkan tinggi badan.\n"
    else:
        result += f"IPB: {ipb:.2f}% - Anak tidak stunting berdasarkan tinggi badan.\n"

    if imt < 80:
        result += f"IMT: {imt:.2f}% - Anak mengalami stunting berdasarkan berat badan."
    else:
        result += f"IMT: {imt:.2f}% - Anak tidak stunting berdasarkan berat badan."

    return result
