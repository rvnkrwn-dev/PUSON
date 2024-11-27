from flask import Blueprint, jsonify
from ..models.anak import Anak
from ..models.stunting import Stunting
from ..models.posyandu import Posyandu
from ..models.puskesmas import Puskesmas
from ..models.pemeriksaan import Pemeriksaan
from ..models.user import User
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required
from ..middlewares.is_login import is_login
from ..middlewares.has_access import has_access
from .. import db
import pandas as pd
from sqlalchemy import func

stats_bp = Blueprint('stats_bp', __name__)

@stats_bp.route('/stats/jumlah-anak', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_jumlah_anak():
    # Mengambil data anak yang diperbarui dari database
    anak_data = db.session.query(Anak).all()
    
    # Konversi data ke dataframe pandas
    data = {
        "id": [a.id for a in anak_data],
        "timestamp": [a.updated_at if a.updated_at else a.created_at for a in anak_data]
    }
    df = pd.DataFrame(data)
    
    # Menghapus nilai NaT di kolom timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    
    # Mengelompokkan data berdasarkan periode
    df.set_index('timestamp', inplace=True)
    df_grouped = df.resample('M').count()
    
    # Menambahkan kolom persentase perubahan
    df_grouped['percentage_change'] = df_grouped['id'].pct_change() * 100
    
    # Mengonversi dataframe ke dictionary
    result = df_grouped.to_dict(orient='index')
    
    # Membuat output yang lebih mudah dibaca
    output = []
    for date, values in result.items():
        output.append({
            "periode": date.strftime('%Y-%m'),
            "jumlah_anak": values['id'],
            "persentase_perubahan": values.get('percentage_change', None)
        })
    
    return jsonify(output)


def is_stunting(result):
    return "Anak mengalami stunting" in result


@stats_bp.route('/stats/jumlah-stunting', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_jumlah_stunting():
    # Mengambil data pemeriksaan yang diperbarui dari database
    pemeriksaan_data = db.session.query(Pemeriksaan).all()
    
    # Konversi data ke dataframe pandas
    data = {
        "id": [p.id for p in pemeriksaan_data],
        "timestamp": [p.updated_at if p.updated_at else p.created_at for p in pemeriksaan_data],
        "result": [p.result for p in pemeriksaan_data]
    }
    df = pd.DataFrame(data)
    
    # Menentukan apakah hasil pemeriksaan menunjukkan stunting
    df['is_stunting'] = df['result'].apply(is_stunting)
    
    # Menghapus nilai NaT di kolom timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    
    # Mengelompokkan data berdasarkan periode (misalnya, per bulan)
    df.set_index('timestamp', inplace=True)
    df_grouped = df.resample('M').agg({'is_stunting': 'sum'})
    
    # Menambahkan kolom persentase perubahan
    df_grouped['percentage_change'] = df_grouped['is_stunting'].pct_change() * 100
    
    # Mengonversi dataframe ke dictionary
    result = df_grouped.to_dict(orient='index')
    
    # Membuat output yang lebih mudah dibaca
    output = []
    for date, values in result.items():
        output.append({
            "periode": date.strftime('%Y-%m'),
            "jumlah_stunting": values['is_stunting'],
            "persentase_perubahan": values.get('percentage_change', None)
        })
    
    return jsonify(output)


@stats_bp.route('/stats/total-puskesmas', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_total_puskesmas():
    # Menghitung total jumlah puskesmas dari database
    total_puskesmas = db.session.query(func.count(Puskesmas.id)).scalar()
    return jsonify({"total_puskesmas": total_puskesmas})


@stats_bp.route('/stats/total-posyandu', methods=['GET'])
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_total_posyandu():
    # Menghitung total jumlah posyandu dari database
    total_posyandu = db.session.query(func.count(Posyandu.id)).scalar()
    return jsonify({"total_posyandu": total_posyandu})


@stats_bp.route('/stats/dashboard-data', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_combined_data():
    # Mengambil data anak, stunting, dan pemeriksaan dari database
    anak_data = db.session.query(Anak).all()
    stunting_data = db.session.query(Stunting).all()
    pemeriksaan_data = db.session.query(Pemeriksaan).all()
    
    # Membuat dictionary untuk menyimpan data stunting dan pemeriksaan berdasarkan anak_id
    stunting_dict = {s.anak_id: s for s in stunting_data}
    pemeriksaan_dict = {p.anak_id: p for p in pemeriksaan_data}
    
    combined_data = []
    for anak in anak_data:
        stunting = stunting_dict.get(anak.id)
        pemeriksaan = pemeriksaan_dict.get(anak.id)
        
        if stunting and pemeriksaan:
            result_text = "Stunting" if is_stunting(pemeriksaan.result) else "Tidak Stunting"
            combined_data.append({
                "nama": anak.name,
                "gender": anak.gender,
                "usia": anak.age,
                "tinggi": str(stunting.height) if stunting else "Data tidak tersedia",
                "berat": str(stunting.weight) if stunting else "Data tidak tersedia",
                "hasil": result_text
            })
    
    return jsonify(combined_data)


@stats_bp.route('/stats/grafik-anak', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_grafik_anak():
    # Mengambil data anak dari database
    anak_data = db.session.query(Anak).all()
    
    # Konversi data ke dataframe pandas
    data = {
        "id": [a.id for a in anak_data],
        "updated_at": [a.updated_at for a in anak_data],
        "created_at": [a.created_at for a in anak_data],
        "gender": [a.gender for a in anak_data]
    }
    df = pd.DataFrame(data)
    
    # Menggabungkan kolom updated_at dan created_at
    df['timestamp'] = df['updated_at'].fillna(df['created_at'])
    
    # Menghapus nilai NaT di kolom timestamp
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.dropna(subset=['timestamp'], inplace=True)
    
    # Menentukan waktu akhir untuk memastikan hanya 12 bulan terakhir yang diambil
    end_time = datetime.now()
    start_time = end_time - pd.DateOffset(months=12)
    
    # Menambahkan kolom 'month' untuk memudahkan resampling
    df['month'] = df['timestamp'].dt.to_period('M')
    
    # Mengelompokkan data berdasarkan jenis kelamin dan periode (misalnya, per bulan)
    df_male = df[(df['gender'] == 'male') & (df['timestamp'] >= start_time)].groupby('month').size()
    df_female = df[(df['gender'] == 'female') & (df['timestamp'] >= start_time)].groupby('month').size()

    # Buat range semua bulan dalam periode yang ditentukan
    all_months = pd.period_range(start=start_time, end=end_time, freq='M')

    # Membuat output JSON sesuai format yang diinginkan
    output = []
    for month in all_months:
        output.append({
            "bulan": month.strftime('%B'),  # Mengambil nama bulan
            "jumlah_laki_laki": int(df_male.get(month, 0)),  # Mengonversi int64 ke int
            "jumlah_perempuan": int(df_female.get(month, 0))  # Mengonversi int64 ke int
        })
    
    return jsonify(output)


@stats_bp.route('/stats/all-data', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_all_data():
    # Mengambil data anak dari database
    anak_data = db.session.query(Anak).all()
    
    # Menghitung total jumlah anak
    total_anak = len(anak_data)
    total_laki_laki = sum(1 for a in anak_data if a.gender == 'male')
    total_perempuan = total_anak - total_laki_laki
    
    # Mengambil data puskesmas
    puskesmas_data = db.session.query(Puskesmas).all()
    total_puskesmas = len(puskesmas_data)
    
    # Mengambil data posyandu
    posyandu_data = db.session.query(Posyandu).all()
    total_posyandu = len(posyandu_data)
    
    # Mengambil data user
    user_data = db.session.query(User).all()
    total_user = len(user_data)
    
    return jsonify({
        "anak": {
            "total": total_anak,
            "lakiLaki": total_laki_laki,
            "perempuan": total_perempuan
        },
        "puskesmas": {
            "total": total_puskesmas
        },
        "posyandu": {
            "total": total_posyandu
        },
        "user": {
            "total": total_user
        }
    })


@stats_bp.route('/stats/grafik-stunting', methods=['GET'])
@jwt_required()
@is_login
@has_access(["super_admin", "admin_puskesmas", "admin_posyandu", "user"])
def get_grafik_stunting():
    # Menentukan waktu akhir dan waktu awal untuk 12 bulan terakhir
    end_time = datetime.now()
    start_time = end_time - timedelta(days=365)

    # Query untuk mengambil data pemeriksaan tanpa filter "mengalami stunting"
    results = (
        db.session.query(
            func.date_format(Pemeriksaan.updated_at, '%Y-%m').label('bulan'),  # Mengelompokkan berdasarkan bulan
            Pemeriksaan.result,  # Mengambil teks hasil pemeriksaan
            func.count(Pemeriksaan.id).label('total')  # Menghitung jumlah kasus
        )
        .filter(Pemeriksaan.updated_at >= start_time)  # Filter rentang waktu
        .group_by(func.date_format(Pemeriksaan.updated_at, '%Y-%m'), Pemeriksaan.result)  # Kelompokkan berdasarkan bulan dan hasil
        .all()
    )

    # Konversi hasil query ke dictionary dengan fungsi is_stunting
    data = {}
    for row in results:
        # Memeriksa apakah result mengandung "Anak mengalami stunting"
        if is_stunting(row.result):
            # Mengelompokkan hasil berdasarkan bulan
            data[row.bulan] = data.get(row.bulan, 0) + row.total

    # Membuat daftar bulan untuk 12 bulan terakhir
    all_months = []
    current_month = start_time.replace(day=1)
    while current_month <= end_time.replace(day=1):
        all_months.append(current_month)
        current_month += timedelta(days=31)
        current_month = current_month.replace(day=1)  # Pastikan di awal bulan

    # Menyusun data akhir untuk setiap bulan
    result_json = []
    for month in all_months:
        month_key = month.strftime('%Y-%m')  # Format YYYY-MM untuk pencocokan
        result_json.append({
            "bulan": month.strftime('%B'),  # Nama bulan dalam format teks (e.g., Januari)
            "total": int(data.get(month_key, 0))  # Ambil data dari dictionary, jika tidak ada gunakan 0
        })

    return jsonify(result_json)
