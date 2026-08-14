const baseColors = [
  { dark: "#1f77b4", light: "#aec7e8" }, // Blue
  { dark: "#ff7f0e", light: "#ffbb78" }, // Orange
  { dark: "#2ca02c", light: "#98df8a" }, // Green
  { dark: "#d62728", light: "#ff9896" }, // Red
  { dark: "#9467bd", light: "#c5b0d5" }, // Purple
  { dark: "#8c564b", light: "#c49c94" }, // Brown
];
const green = "#008000";
const red = "#800000";

function total_requests(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const date = item.timestamp.split("T")[0];

    if (!aggregation[date]) {
      aggregation[date] = 0;
    }

    aggregation[date] += 1;
  });

  const labels = Object.keys(aggregation).sort();

  const color = baseColors[0];
  const totalData = labels.map((date) => {
    return aggregation[date] ? aggregation[date] : 0;
  });

  const datasets = [
    {
      label: "(Total)",
      data: totalData,
      backgroundColor: color.dark,
    },
  ];

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total requests by day",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        x: {
          stacked: false,
        },
        y: {
          stacked: false,
          beginAtZero: true,
          title: {
            display: true,
            text: "Requests",
          },
        },
      },
    },
  });
}

function total_tokens(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const date = item.timestamp.split("T")[0];
    const provider = item.provider;
    const total_tokens = item.total_tokens;

    if (!aggregation[date]) {
      aggregation[date] = {};
    }

    if (!aggregation[date][provider]) {
      aggregation[date][provider] = 0;
    }
    aggregation[date][provider] += total_tokens;
  });

  const labels = Object.keys(aggregation).sort();
  const providers = Array.from(
    new Set(labels.flatMap((date) => Object.keys(aggregation[date]))),
  );

  const datasets = [];
  providers.forEach((provider, index) => {
    const color = baseColors[index];
    const totalData = labels.map((date) => {
      return aggregation[date][provider] ? aggregation[date][provider] : 0;
    });

    datasets.push({
      label: `${provider} (Total)`,
      data: totalData,
      backgroundColor: color.dark,
      stack: provider,
    });
  });

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total tokens by provider",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        x: {
          stacked: false,
        },
        y: {
          stacked: false,
          beginAtZero: true,
          title: {
            display: true,
            text: "Tokens",
          },
        },
      },
    },
  });
}

function detail_tokens(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const date = item.timestamp.split("T")[0];
    const provider = item.provider;
    const prompt_tokens = item.prompt_tokens;
    const completion_tokens = item.completion_tokens;

    if (!aggregation[date]) {
      aggregation[date] = {};
    }

    if (!aggregation[date][provider]) {
      aggregation[date][provider] = { prompt: 0, completion: 0 };
    }

    aggregation[date][provider].prompt += prompt_tokens;
    aggregation[date][provider].completion += completion_tokens;
  });

  const labels = Object.keys(aggregation).sort();
  const providers = Array.from(
    new Set(labels.flatMap((date) => Object.keys(aggregation[date]))),
  );

  const datasets = [];
  providers.forEach((provider, index) => {
    const color = baseColors[index];
    const promptData = labels.map((date) => {
      return aggregation[date][provider]
        ? aggregation[date][provider].prompt
        : 0;
    });
    const completionData = labels.map((date) => {
      return aggregation[date][provider]
        ? aggregation[date][provider].completion
        : 0;
    });

    datasets.push({
      label: `${provider} (Input)`,
      data: promptData,
      backgroundColor: color.dark,
      stack: provider,
    });

    datasets.push({
      label: `${provider} (Output)`,
      data: completionData,
      backgroundColor: color.light,
      stack: provider,
    });
  });

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Input/Output tokens by provider",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        x: {
          stacked: false,
        },
        y: {
          stacked: true,
          beginAtZero: true,
          title: {
            display: true,
            text: "Tokens",
          },
        },
      },
    },
  });
}

function model_tokens(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const date = item.timestamp.split("T")[0];
    const model = item.model;
    const total_tokens = item.total_tokens;

    if (!aggregation[date]) {
      aggregation[date] = {};
    }

    if (!aggregation[date][model]) {
      aggregation[date][model] = 0;
    }
    aggregation[date][model] += total_tokens;
  });

  const labels = Object.keys(aggregation).sort();
  const models = Array.from(
    new Set(labels.flatMap((date) => Object.keys(aggregation[date]))),
  );

  const datasets = [];
  models.forEach((model, index) => {
    const color = baseColors[index];
    const totalData = labels.map((date) => {
      return aggregation[date][model] ? aggregation[date][model] : 0;
    });

    datasets.push({
      label: `${model}`,
      data: totalData,
      backgroundColor: color.dark,
      stack: model,
    });
  });

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total tokens by model",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
      scales: {
        x: {
          stacked: false,
        },
        y: {
          stacked: false,
          beginAtZero: true,
          title: {
            display: true,
            text: "Tokens",
          },
        },
      },
    },
  });
}

function model_scores(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const model = item.model;
    const ups = item.up;
    const downs = item.down;

    if (!aggregation[model]) {
      aggregation[model] = { ups: 0, downs: 0 };
    }

    aggregation[model].ups += ups;
    aggregation[model].downs += downs;
  });

  const green = "#008000";
  const red = "#800000";

  const labels = Object.keys(aggregation).sort();

  const upsData = labels.map((model) =>
    aggregation[model] ? aggregation[model].ups : 0,
  );
  const downsData = labels.map((model) =>
    aggregation[model] ? aggregation[model].downs : 0,
  );

  const datasets = [
    {
      label: "Ups",
      data: upsData,
      backgroundColor: green,
    },
    {
      label: "Downs",
      data: downsData,
      backgroundColor: red,
    },
  ];

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total votes by model",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
    },
    scales: {
      x: {
        stacked: false,
      },
      y: {
        stacked: true,
        beginAtZero: true,
        title: {
          display: true,
          text: "Votes",
        },
      },
    },
  });
}

function day_scores(container, data) {
  const aggregation = {};
  data.forEach((item) => {
    const date = item.timestamp.split("T")[0];
    const ups = item.up;
    const downs = item.down;

    if (!aggregation[date]) {
      aggregation[date] = { ups: 0, downs: 0 };
    }

    aggregation[date].ups += ups;
    aggregation[date].downs += downs;
  });

  const green = "#008000";
  const red = "#800000";

  const labels = Object.keys(aggregation).sort();

  const upsData = labels.map((date) =>
    aggregation[date] ? aggregation[date].ups : 0,
  );
  const downsData = labels.map((date) =>
    aggregation[date] ? aggregation[date].downs : 0,
  );

  const datasets = [
    {
      label: "Ups",
      data: upsData,
      backgroundColor: green,
    },
    {
      label: "Downs",
      data: downsData,
      backgroundColor: red,
    },
  ];

  new Chart(container, {
    type: "bar",
    data: {
      labels: labels,
      datasets: datasets,
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Total votes by day",
        },
        tooltip: {
          mode: "index",
          intersect: false,
        },
      },
    },
    scales: {
      x: {
        stacked: false,
      },
      y: {
        stacked: true,
        beginAtZero: true,
        title: {
          display: true,
          text: "Votes",
        },
      },
    },
  });
}

function scores(container, data) {
  const aggregation = { ups: 0, downs: 0 };
  data.forEach((item) => {
    const ups = item.up;
    const downs = item.down;

    aggregation.ups += ups;
    aggregation.downs += downs;
  });

  new Chart(container, {
    type: "pie",
    data: {
      labels: ["Total Ups", "Total Downs"],
      datasets: [
        {
          data: [aggregation.ups, aggregation.downs],
          backgroundColor: [green, red],
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      radius: "50%",
      plugins: {
        title: {
          display: true,
          text: "Total votes",
        },
      },
    },
  });
}
