
var testim = document.getElementById("testim"),
testimDots = Array.prototype.slice.call(document.getElementById("testim-dots").children),
testimContent = Array.prototype.slice.call(document.getElementById("testim-content").children),
testimleftArrow = document.getElementById("left-arrow"),
testimRightArrow = document.getElementById("right-arrow"),
testimSpeed = 4500,
currentSlide = 0,
currentActive = 0,
testimTimer
;

window.onload = function () {

// Testim Script
function playSlide(slide) {
    for (var k = 0; k < testimDots.length; k++) {
        testimContent[k].classList.remove("active");
        testimContent[k].classList.remove("inactive");
        testimDots[k].classList.remove("active");
    }
    if (slide < 0) {
        slide = currentSlide = testimContent.length - 1;
    }
    if (slide > testimContent.length - 1) {
        slide = currentSlide = 0;
    }
    if (currentActive != currentSlide) {
        testimContent[currentActive].classList.add("inactive");
    }
    testimContent[slide].classList.add("active");
    testimDots[slide].classList.add("active");

    currentActive = currentSlide;

    
}

testimleftArrow.addEventListener("click", function () {
    playSlide(currentSlide -= 1);
})
testimRightArrow.addEventListener("click", function () {
    playSlide(currentSlide += 1);
})

for (var l = 0; l < testimDots.length; l++) {
    testimDots[l].addEventListener("click", function () {
        playSlide(currentSlide = testimDots.indexOf(this));
    })
}
playSlide(currentSlide);

}

const container = document.querySelector(".container"), 
      pwShowHide = document.querySelectorAll(".showHidePw"),
      pwFields = document.querySelectorAll(".password"),
      signup = document.querySelector(".signup-link"),
      login = document.querySelector(".login-link");

      pwShowHide.forEach(eyeIcon => {
          eyeIcon.addEventListener("click", () => {
              pwFields.forEach(pwField => {
                  if(pwField.type === "password") {
                      pwField.type = "text";

                      pwShowHide.forEach(icon => {
                        icon.classList.replace("uil-eye-slash", "uil-eye");
                      })
                    }else {
                        pwField.type = "password";

                        pwShowHide.forEach(icon => {
                            icon.classList.replace("uil-eye", "uil-eye-slash");
                        })
                    }
              })
          })
      })


container.classList.add("active");