import React, { useState, useEffect } from "react";
import { useTheme, lighten, darken } from "@mui/material/styles";
import {
  Chart as ChartJS,
  TimeScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";
import { getChartColor } from "components/Theming";

import "chartjs-adapter-moment";
import LoadingGraph from "./LoadingGraph";

ChartJS.register(TimeScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default function MonthBarGraph({
  data,
  title,
  loading,
  colorOffset = 0,
  excludedCategories = [],
  singleCategory,
}) {
  const [formatedData, setFormatedData] = useState({ datasets: [] });
  const theme = useTheme();

  useEffect(() => {
    if (data) {
      setFormatedData({
        datasets: (data?.datasets || [])
          ?.filter((d) =>
            singleCategory
              ? d?.category === singleCategory
              : !excludedCategories?.includes(d?.category)
          )
          ?.map((d, i) => {
            const color = getChartColor(theme, i, colorOffset);
            const mainColor = d.color || color.main;
            const lightColor = d.color
              ? lighten(
                  d.color,
                  theme.palette.tonalOffset.light || theme.palette.tonalOffset
                )
              : color.light;
            const darkColor = d.color
              ? darken(
                  d.color,
                  theme.palette.tonalOffset.dark ||
                    theme.palette.tonalOffset * 1.5
                )
              : color.dark;
            return {
              data: d.data,
              label: d.category,
              color: mainColor,
              borderWidth: 1,
              backgroundColor: lightColor,
              borderColor: darkColor,
              hoverBackgroundColor: mainColor,
            };
          }),
      });
    }
  }, [data]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        stacked: true,
        type: "time",
        time: {
          unit: "month",
          tooltipFormat: "MMM YYYY",
        },
        offset: true,
      },
      y: {
        stacked: true,
        beginAtZero: true,
        grace: "5%",
        ticks: { stepSize: 1 },
      },
    },
    interaction: {
      mode: "index",
    },
    plugins: {
      title: {
        text: title || "",
        display: true,
      },
      legend: {
        display: !singleCategory,
      },
      tooltip: {
        callbacks: {
          footer: (context) => {
            const stack_values = Object.entries(context[0]?.parsed?._stacks?.y)
              ?.filter(([key]) => !key?.includes("_"))
              ?.map((entry) => entry[1]);
            return singleCategory
              ? ""
              : `Total : ${stack_values.reduce(
                  (result, item) => result + item,
                  0
                )}`;
          },
        },
      },
    },
  };

  return loading ? (
    <LoadingGraph />
  ) : (
    <Bar
      data={formatedData}
      options={options}
      style={{
        flexGrow: 1,
        minHeight: "300px",
        paddingBottom: theme.spacing(2),
      }}
    />
  );
}
