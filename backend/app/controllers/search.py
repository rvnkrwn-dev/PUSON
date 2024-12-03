from flask import Blueprint, request, jsonify
from ..models import User, Puskesmas, Posyandu, Anak, Stunting, Pemeriksaan

# Membuat blueprint untuk pencarian
search_bp = Blueprint('search', __name__)

# Menambahkan route untuk pencarian pada blueprint
@search_bp.route('/search/<table>', methods=['GET'])
def search(table):
    # Mengambil parameter pencarian dari query string
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)  # Mengatur default halaman ke 1
    per_page = request.args.get('per_page', 10, type=int)  # Mengatur default jumlah hasil per halaman ke 10

    # Pencarian pada tabel `users`
    if table == 'users':
        results = User.query.filter(
            (User.full_name.ilike(f"%{query}%")) | 
            (User.id.like(f"%{query}%")) |
            (User.email.ilike(f"%{query}%")) |
            (User.role.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [{"id": user.id, "full_name": user.full_name, "email": user.email, "role": user.role} for user in results.items]

    # Pencarian pada tabel `puskesmas`
    elif table == 'puskesmas':
        results = Puskesmas.query.filter(
            (Puskesmas.name.ilike(f"%{query}%")) |
            (Puskesmas.id.like(f"%{query}%")) |
            (Puskesmas.phone.ilike(f"%{query}%")) |
            (Puskesmas.address.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [{"id": puskesmas.id, "name": puskesmas.name, "address": puskesmas.address, "phone": puskesmas.phone} for puskesmas in results.items]

    # Pencarian pada tabel `posyandu`
    elif table == 'posyandu':
        results = Posyandu.query.filter(
            (Posyandu.name.ilike(f"%{query}%")) |
            (Posyandu.id.like(f"%{query}%")) |
            (Posyandu.phone.ilike(f"%{query}%")) |
            (Posyandu.address.ilike(f"%{query}%")) |
            (Posyandu.puskesmas_id.like(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [{"id": posyandu.id, "name": posyandu.name, "address": posyandu.address, "phone": posyandu.phone, "puskesmas_id": posyandu.puskesmas_id} for posyandu in results.items]

    # Pencarian pada tabel `anak`
    elif table == 'anak':
        results = Anak.query.filter(
            (Anak.name.ilike(f"%{query}%")) |
            (Anak.id.like(f"%{query}%")) |
            (Anak.gender.ilike(f"%{query}%")) |
            (Anak.age.like(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [
            {
                "id": anak.id,
                "name": anak.name,
                "age": anak.age,
                "gender": anak.gender,
                "posyandu_id": anak.posyandu_id,
                "posyandu_name": anak.posyandu.name if anak.posyandu else None,
                "created_at": anak.created_at,
                "updated_at": anak.updated_at,
            }
            for anak in results.items
        ]

    # Pencarian pada tabel `stunting`
    elif table == 'stunting':
        results = Stunting.query.join(Anak).filter(
            (Anak.name.ilike(f"%{query}%")) |
            (Stunting.id.like(f"%{query}%")) |
            (Stunting.height.like(f"%{query}%")) |
            (Stunting.weight.like(f"%{query}%")) |
            (Stunting.date.ilike(f"%{query}%")) |
            (Stunting.created_at.ilike(f"%{query}%")) |
            (Stunting.updated_at.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [
            {
                "id": stunting.id,
                "anak_id": stunting.anak_id,
                "anak_name": stunting.anak.name,
                "date": stunting.date,
                "height": stunting.height,
                "weight": stunting.weight,
                "created_at": stunting.created_at,
                "updated_at": stunting.updated_at,
            }
            for stunting in results.items
        ]

    # Pencarian pada tabel `pemeriksaan`
    elif table == 'pemeriksaan':
        results = Pemeriksaan.query.join(Anak).filter(
            (Anak.name.ilike(f"%{query}%")) |
            (Pemeriksaan.id.like(f"%{query}%")) |
            (Pemeriksaan.result.ilike(f"%{query}%")) |
            (Pemeriksaan.date.ilike(f"%{query}%")) |
            (Pemeriksaan.created_at.ilike(f"%{query}%")) |
            (Pemeriksaan.updated_at.ilike(f"%{query}%"))
        ).paginate(page=page, per_page=per_page, error_out=False)
        data = [
            {
                "id": pemeriksaan.id,
                "anak_id": pemeriksaan.anak_id,
                "anak_name": pemeriksaan.anak.name,
                "date": pemeriksaan.date,
                "result": pemeriksaan.result,
                "created_at": pemeriksaan.created_at,
                "updated_at": pemeriksaan.updated_at,
            }
            for pemeriksaan in results.items
        ]

    # Jika tabel tidak ditemukan
    else:
        return jsonify({"error": "Table not found"}), 404

    # Membuat URL untuk halaman berikutnya dan sebelumnya
    base_url = request.base_url
    next_url = f"{base_url}?q={query}&page={results.next_num}&per_page={per_page}" if results.has_next else None
    prev_url = f"{base_url}?q={query}&page={results.prev_num}&per_page={per_page}" if results.has_prev else None

    # Membuat respons JSON dengan pagination
    response = {
        "total": results.total,
        "pages": results.pages,
        "current_page": results.page,
        "next_page": next_url,
        "prev_page": prev_url,
        "data": data
    }

    # Mengembalikan respons JSON
    return jsonify(response), 200
