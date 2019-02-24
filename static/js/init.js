$(document).ready(function(){
    $('.sidenav').sidenav();
    $('select').formSelect();
    $(".dropdown-trigger").dropdown();
    $('.datepicker').datepicker({
      yearRange: 50 || lower,
      format: 'yyyy-mm-dd',
    });
  });