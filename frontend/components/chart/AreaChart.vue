<template>
  <div id="hs-single-area-chart">
    <client-only>
      <ApexCharts
          type="area"
          :options="computedChartOptions"
          :series="series"
          width="100%"
          height="300"
      />
    </client-only>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import ApexCharts from 'vue3-apexcharts';

const props = defineProps<{
  series: Array<{ name: string, data: number[] }>;
  categories: string[];
  color: string[];
}>();

// Computed chart options that use passed props
const computedChartOptions = computed(() => ({
  chart: {
    height: 300,
    type: "area",
    toolbar: {
      show: false,
    },
    zoom: {
      enabled: false,
    },
  },
  colors: props.color,
  legend: {
    show: false,
  },
  dataLabels: {
    enabled: false,
  },
  stroke: {
    curve: "straight",
    width: 2,
  },
  grid: {
    strokeDashArray: 2,
  },
  fill: {
    type: "gradient",
    gradient: {
      type: "vertical",
      shadeIntensity: 1,
      opacityFrom: 0.1,
      opacityTo: 0.8,
    },
  },
  xaxis: {
    type: "category",
    tickPlacement: "on",
    categories: props.categories,
    axisBorder: {
      show: false,
    },
    axisTicks: {
      show: false,
    },
    crosshairs: {
      stroke: {
        dashArray: 0,
      },
      dropShadow: {
        show: false,
      },
    },
    tooltip: {
      enabled: false,
    },
    labels: {
      style: {
        colors: "#9ca3af",
        fontSize: "10px",
        fontFamily: "Inter, sans-serif",
        fontWeight: 400,
      },
      formatter: (title: string) => {
        let t = title;
        if (t) {
          const newT = t.split(" ");
          t = `${newT[0].length > 3 ? newT[0].slice(0,3) : newT[0]} ${newT[1]?.slice(0, 3)?? ""}`;
        }
        return t;
      },
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
  tooltip: {
    x: {
      format: 'dd MMM yyyy',
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
        labels: {
          style: {
            colors: "#9ca3af",
            fontSize: "11px",
            fontFamily: "Inter, sans-serif",
            fontWeight: 400,
          },
          offsetX: -2,
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
            formatter: (value: number) => value >= 1000 ? `${value / 1000}k` : value,
          },
        },
      },
    },
  ],
}));
</script>