const baseColors = [
  { dark: "#1f77b4", light: "#aec7e8" }, // Blue
  { dark: "#ff7f0e", light: "#ffbb78" }, // Orange
  { dark: "#2ca02c", light: "#98df8a" }, // Green
  { dark: "#d62728", light: "#ff9896" }, // Red
  { dark: "#9467bd", light: "#c5b0d5" }, // Purple
  { dark: "#8c564b", light: "#c49c94" }, // Brown
];

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
          text: "Total tokens by provider",
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
        stacked: false,
        beginAtZero: true,
        title: {
          display: true,
          text: "Tokens",
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
      label: `${model} (Total)`,
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
  });
}
