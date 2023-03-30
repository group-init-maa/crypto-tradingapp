let myChart;

async function drawgraph(coin = "bitcoin") {
  const getMarketCharts = async (coinId, vsCurrency, days, interval) => {
    const url = `https://api.coingecko.com/api/v3/coins/${coinId}/market_chart?vs_currency=${vsCurrency}&days=${days}&interval=${interval}`;
    const response = await fetch(url);
    const data = await response.json();

    const timestamp_list = [];
    const price_list = [];

    const options = {
      weekday: "long",
      year: "numeric",
      month: "numeric",
      day: "numeric",
      hour: "numeric",
      minute: "numeric",
      second: "numeric",
    };

    data.prices.forEach((price) => {
      const date = new Date(price[0]);
      const dateTimeFormat = new Intl.DateTimeFormat("en-US", options);
      const parts = dateTimeFormat.formatToParts(date);
      let formattedDate = "";
      parts.forEach((part) => {
        if (part.type === "weekday") formattedDate += `${part.value}, `;
        if (part.type === "day") formattedDate += `${part.value}/`;
        if (part.type === "month") formattedDate += `${part.value}/`;
        if (part.type === "year") formattedDate += `${part.value}, `;
        if (part.type === "hour") formattedDate += `${part.value}:`;
        if (part.type === "minute") formattedDate += `${part.value}:`;
        if (part.type === "second") formattedDate += `${part.value}`;
      });
      timestamp_list.push(formattedDate);
      price_list.push(price[1]);
    });

    const raw_data = {
      labels: timestamp_list,
      datasets: [
        {
          label: `${coinId} price in ${vsCurrency}`,
          data: price_list,
          fill: false,
          borderColor: "rgb(66, 133, 244)",
          tension: 0.1,
        },
      ],
    };

    return raw_data;
  };
  const drawChart = async () => {
    const market_info = await getMarketCharts(coin, "gbp", "30", "daily");
    const ctx = document.getElementById("myChart").getContext("2d");

    if (myChart) {
      myChart.destroy();
    }

    myChart = new Chart(ctx, {
      type: "line",
      data: market_info,
    });
  };

  drawChart();
}
