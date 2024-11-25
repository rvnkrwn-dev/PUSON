<template>
  <div id="hs-multiple-area-charts">
    <client-only>
      <ApexCharts
          type="bar"
          :options="chartOptions"
          :series="chartSeries"
          width="100%"
          height="300"
      />
    </client-only>
  </div>
</template>

<script setup lang="ts">
import ApexCharts from "vue3-apexcharts";

// Define props to accept data for series and categories
const props = defineProps<{
  series: Array<{ name: string, data: number[] }>;
  categories: string[];
  color: string[];
}>();

// Set up chart options using props for dynamic data
const chartOptions = computed(() => ({
  chart: {
    type: "bar",
    height: 300,
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  colors: props.color,
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "16px",
      borderRadius: 0,
    },
  },
  legend: {
    show: false,
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    show: true,
    width: 8,
    colors: ["transparent"],
  },
  xaxis: {
    categories: props.categories,
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    crosshairs: {
      show: false,
    },
    labels: {
      style: {
        colors: "#9ca3af",
        fontSize: "10px",
        fontFamily: "Inter, sans-serif",
        fontWeight: 400,
      },
      offsetX: -2,
    },
  },
  yaxis: {
    labels: {
      align: "left",
      minWidth: 0,
      maxWidth: 140,
      style: {
        colors: "#9ca3af",
        fontSize: "10px",
        fontFamily: "Inter, sans-serif",
        fontWeight: 400,
      },
      formatter: (value: number) => (value >= 1000 ? `${value / 1000}k` : value),
    },
  },
  states: {
    hover: {
      filter: {
        type: "darken",
        value: 0.9,
      },
    },
  },
  tooltip: {
    x: {
      format: "MMMM yyyy",
    },
    y: {
      formatter: (value: number) => `${value >= 1000 ? `${value / 1000}k` : value}`,
    },
  },
  responsive: [
    {
      breakpoint: 568,
      options: {
        chart: {
          height: 300,
        },
        plotOptions: {
          bar: {
            columnWidth: "14px",
          },
        },
        stroke: {
          width: 8,
        },
        labels: {
          style: {
            colors: "#9ca3af",
            fontSize: "11px",
            fontFamily: "Inter, sans-serif",
            fontWeight: 400,
          },
          offsetX: -2,
          // formatter: (title: string) => title?.slice(0, 3),
        },
        yaxis: {
          labels: {
            align: "left",
            minWidth: 0,
            maxWidth: 140,
            style: {
              colors: "#9ca3af",
              fontSize: "11px",
              fontFamily: "Inter, sans-serif",
              fontWeight: 400,
            },
            formatter: (value: number) =>
                value >= 1000 ? `${value / 1000}k` : value,
          },
        },
      },
    },
  ],
}));

const chartSeries = computed(() => props.series);
</script>

<style scoped>

</style>