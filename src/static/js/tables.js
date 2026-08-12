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
    if (column.label) {
      const th = document.createElement("th");
      th.textContent = column.label;
      tr.append(th);
    }
  });
  thead.append(tr);
  table.append(thead);

  const tbody = document.createElement("tbody");
  data.forEach((request) => {
    const tr = document.createElement("tr");
    columns.forEach((column) => {
      if (column.label) {
        const td = document.createElement("td");
        td.textContent = request[column.field];
        tr.append(td);
        if (column.link) {
          td.addEventListener("click", (event) => {
            window.location.href = `${column.link}?${column.field}=${request[column.field]}`;
          });
          td.style = "cursor:pointer";
        }
      }
      if (column.clazz) {
        const clazz = column.clazz[request[column.field]];
        if (clazz) {
          tr.classList.add(clazz);
        }
      }
    });
    tbody.append(tr);
  });
  table.append(tbody);
  document.getElementById(container).append(table);
}
