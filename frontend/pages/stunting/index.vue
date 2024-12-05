<template>
  <div>

  </div>
</template>

<script setup lang="ts">
import Swal from 'sweetalert2';
import { sleep } from '@antfu/utils';

// config
const config = useRuntimeConfig();
const apiUrl = config.public.apiUrl;

// State variables
const searchQuery = ref('');
const dataPemeriksaan = ref<any[]>([]);
const isLoading = ref<boolean>(false);

// Fetch Pemeriksaan data from API
const fetchPemeriksaan = async () => {
  try {
    isLoading.value = true;
    await sleep(2000); // Simulating loading delay
    const response = await useFetchApi(`${apiUrl}/auth/stunting`);
    dataPemeriksaan.value = response?.data || [];
  } catch (err) {
    await Swal.fire({
      position: 'bottom-end',
      icon: 'error',
      title: 'Gagal memuat data pemeriksaan',
      showConfirmButton: false,
      timer: 1500,
      toast: true
    });
  } finally {
    isLoading.value = false;
  }
};

// Filter data based on search query
const filteredData = computed(() => {
  return dataPemeriksaan.value.filter(item =>
      item.nama_anak.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.date.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      item.result.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Format date for better presentation
const formatDate = (date: string) => {
  const d = new Date(date);
  return d.toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric' });
};

// Delete pemeriksaan item
const handleDelete = async (id: number) => {
  Swal.fire({
    title: 'Anda yakin?',
    text: 'Anda tidak dapat mengembalikan ini!',
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    cancelButtonText: 'Batal',
    confirmButtonText: 'Ya, hapus!'
  }).then(async (result) => {
    if (result.isConfirmed) {
      try {
        await useFetchApi(`${apiUrl}/auth/pemeriksaan/${id}`, { method: 'DELETE' });
        dataPemeriksaan.value = dataPemeriksaan.value.filter(item => item.id !== id);
        await Swal.fire({
          position: 'bottom-end',
          icon: 'success',
          title: 'Sukses menghapus data pemeriksaan',
          showConfirmButton: false,
          timer: 1500,
          toast: true
        });
      } catch (err) {
        await Swal.fire({
          position: 'bottom-end',
          icon: 'error',
          title: 'Gagal menghapus data pemeriksaan',
          showConfirmButton: false,
          timer: 1500,
          toast: true
        });
      }
    }
  });
};

onMounted(() => {
  fetchPemeriksaan();
});
</script>

<style scoped>

</style>