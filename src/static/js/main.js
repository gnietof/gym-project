$(function () {
  const navContainer = $("#nav-placeholder");

  if (navContainer.length > 0) {
    const currentPage = window.location.pathname.split("/").pop();
    navContainer.load("menu.html", function () {
      if (currentPage) {
        navContainer
          .find(`.nav-link[href*="${currentPage}"]`)
          .closest("li")
          .addClass("active");
      } else {
        navContainer.find(".navbar-brand").addClass("active");
      }
    });
  }
});
