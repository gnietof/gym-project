function create_table(container, columns, data) {
  const table = document.createElement("table");
  table.classList.add(
    "table",
    "table-striped",
    "table-hover",
    "align-middle",
    "mb-0",
  );
  const thead = document.createElement("thead");
  thead.classList.add("sticky-top");
  const tr = document.createElement("tr");
  columns.forEach((column) => {
    const th = document.createElement("th");
    th.textContent = column[1];
    tr.append(th);
  });
  thead.append(tr);
  table.append(thead);

  const tbody = document.createElement("tbody");
  data.forEach((request) => {
    const tr = document.createElement("tr");
    columns.forEach((column) => {
      const td = document.createElement("td");
      td.textContent = request[column[0]];
      tr.append(td);
    });
    tbody.append(tr);
  });
  table.append(tbody);
  document.getElementById(container).append(table);
}
