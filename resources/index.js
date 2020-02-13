//functions for animation of the images in my portfolio when hovered over
function startSnake() {
  document.getElementById("hoverGif").src = "resources/images/snake.gif";
}
function stopSnake(){
  document.getElementById("hoverGif").src="resources/images/snake.png";
}




var slides = document.getElementsByClassName("slide");
var currentSlide = 0;
var leaving = slides[currentSlide];
var entering;
var slideInterval = setInterval(nextSlide,2000);

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function nextSlide() {

  leaving = slides[currentSlide];
  currentSlide = (currentSlide+1)%slides.length;
  entering = slides[currentSlide];
  leaving.classList.add("leaving");
  leaving.classList.remove("showing");
  entering.classList.add("showing");
  await sleep(1000);
  leaving.classList.remove("leaving");
}
