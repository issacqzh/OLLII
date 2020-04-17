// function myFunction() {
//   var dots = document.getElementById("dots");
//   var moreText = document.getElementById("more");
//   var btnText = document.getElementById("myBtn");

//   if (dots.style.display === "none") {
//     dots.style.display = "inline";
//     btnText.innerHTML = "Read more";
//     moreText.style.display = "none";
//   } else {
//     dots.style.display = "none";
//     btnText.innerHTML = "Read less";
//     moreText.style.display = "inline";
//   }
// }

$(document).ready(function(){
  $(".read_btn").click(function(){
    if($(this).text() == 'read more'){
      $(this).siblings('.dots').css("display","none");
      $(this).text('read less');
      $(this).prev().css("display","inline");
    }
    else{
      $(this).siblings('.dots').css("display","inline");
      $(this).text('read more');
      $(this).prev().css("display","none");
    }
  });

});