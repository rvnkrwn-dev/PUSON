-- Membuat tabel `users` untuk menyimpan data pengguna
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap pengguna
    full_name VARCHAR(100) NOT NULL, -- Nama lengkap pengguna
    email VARCHAR(100) NOT NULL UNIQUE, -- Email pengguna (harus unik)
    password VARCHAR(255) NOT NULL, -- Kata sandi pengguna
    role ENUM('super_admin', 'admin_puskesmas', 'admin_posyandu', 'user') NOT NULL, -- Peran pengguna
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    reset_token VARCHAR(100), -- Token untuk reset password (opsional)
    reset_token_expiry DATETIME -- Waktu kadaluarsa token reset password (opsional)
);

-- Membuat tabel `puskesmas` untuk menyimpan data puskesmas
CREATE TABLE puskesmas (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap puskesmas
    name VARCHAR(100) NOT NULL UNIQUE, -- Nama puskesmas (harus unik)
    address VARCHAR(255) NOT NULL, -- Alamat puskesmas
    phone VARCHAR(20) NOT NULL UNIQUE, -- Nomor telepon puskesmas (harus unik)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    CONSTRAINT unique_name UNIQUE (name), -- Menambahkan aturan unik untuk kolom `name`
    CONSTRAINT unique_phone UNIQUE (phone) -- Menambahkan aturan unik untuk kolom `phone`
);

-- Membuat tabel `posyandu` untuk menyimpan data posyandu
CREATE TABLE posyandu (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap posyandu
    puskesmas_id INT NOT NULL, -- ID puskesmas terkait
    name VARCHAR(100) NOT NULL UNIQUE, -- Nama posyandu (harus unik)
    address VARCHAR(255) NOT NULL, -- Alamat posyandu
    phone VARCHAR(20) NOT NULL UNIQUE, -- Nomor telepon posyandu (harus unik)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    FOREIGN KEY (puskesmas_id) REFERENCES puskesmas(id) ON DELETE CASCADE -- Relasi ke tabel `puskesmas`, hapus jika puskesmas dihapus
);

-- Membuat tabel `anak` untuk menyimpan data anak
CREATE TABLE anak (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap anak
    name VARCHAR(100) NOT NULL, -- Nama anak
    age INT NOT NULL, -- Usia anak
    gender ENUM('male', 'female') NOT NULL, -- Jenis kelamin anak
    posyandu_id INT, -- ID posyandu terkait
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    FOREIGN KEY (posyandu_id) REFERENCES posyandu(id) ON DELETE SET NULL -- Relasi ke tabel `posyandu`, set NULL jika posyandu dihapus
);

-- Membuat tabel `pemeriksaan` untuk menyimpan data pemeriksaan anak
CREATE TABLE pemeriksaan (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap pemeriksaan
    anak_id INT NOT NULL, -- ID anak yang diperiksa
    date DATE NOT NULL, -- Tanggal pemeriksaan
    result TEXT NOT NULL, -- Hasil pemeriksaan
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    FOREIGN KEY (anak_id) REFERENCES anak(id) ON DELETE CASCADE -- Relasi ke tabel `anak`, hapus jika anak dihapus
);

-- Membuat tabel `stunting` untuk menyimpan data stunting anak
CREATE TABLE stunting (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap data stunting
    anak_id INT NOT NULL, -- ID anak yang mengalami stunting
    date DATE NOT NULL, -- Tanggal pencatatan
    height DECIMAL(5,2) NOT NULL, -- Tinggi badan anak (maksimal 999.99)
    weight DECIMAL(5,2) NOT NULL, -- Berat badan anak (maksimal 999.99)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    FOREIGN KEY (anak_id) REFERENCES anak(id) ON DELETE CASCADE -- Relasi ke tabel `anak`, hapus jika anak dihapus
);

-- Membuat tabel `refresh_token` untuk menyimpan token refresh pengguna
CREATE TABLE refresh_token (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap token
    user_id INT NOT NULL, -- ID pengguna terkait
    token VARCHAR(1000) NOT NULL UNIQUE, -- Token (harus unik)
    expires_at TIMESTAMP NOT NULL, -- Waktu kadaluarsa token
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu pembuatan data
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, -- Waktu terakhir diperbarui
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Relasi ke tabel `users`, hapus jika pengguna dihapus
);

-- Membuat tabel `logs` untuk menyimpan log aktivitas pengguna
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY, -- Kolom ID unik untuk setiap log
    user_id INT NOT NULL, -- ID pengguna terkait
    action VARCHAR(255) NOT NULL, -- Aksi yang dilakukan
    description TEXT, -- Deskripsi detail aksi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Waktu log dicatat
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Relasi ke tabel `users`, hapus jika pengguna dihapus
);
