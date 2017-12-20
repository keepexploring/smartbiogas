$(document).ready(function () {
  navToggle(); //Navigation active class
})

function navToggle() {
  var path = window.location.pathname;
  path = path.replace(/\/$/, "");
  path = decodeURIComponent(path);

  $(".nav a").each(function () {
    var href = $(this).attr('href');
    if (path.substring(0, href.length) === href) {
      $(this).closest('li').addClass('active');
    }
  });
}

  // $('#sidebar').BootSideMenu({
      //   side: "left",
      //   pushBody: false,
      //   duration: 1000
      // });