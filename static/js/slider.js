const slider = document.querySelector("#sliderD");
let sliderSection= document.querySelectorAll(".sliderD-section");
let sliderSectionLast= sliderSection[sliderSection.length-1];

const btnleft = document.querySelector("#btn--left");
const btnright = document.querySelector("#btn--right");


slider.insertAdjacentElement('afterbegin',sliderSectionLast);

function siguiente(){
	let sliderSectionFirst =document.querySelectorAll(".sliderD-section")[0];
	slider.style.marginleft ="-200%";
	slider.style.transition="all 0.5s";
	setTimeout(function(){
		slider.style.transition="none";
		slider.insertAdjacentElement('beforeend', sliderSectionFirst);
		slider.style.marginleft ="-100%";
	}, 500);
}

btnright.addEventListener('click',function(){
	siguiente();
});

function atras(){
	let sliderSection= document.querySelectorAll(".sliderD-section");
	let sliderSectionLast= sliderSection[sliderSection.length-1];
	slider.style.marginleft ="0%";
	slider.style.transition="all 0.5s";
	setTimeout(function(){
		slider.style.transition="none";
		slider.insertAdjacentElement('afterbegin',sliderSectionLast);
		slider.style.marginleft ="-100%";
	}, 500);
}

btnleft.addEventListener('click',function(){
	siguiente();
});

// Por si quiere que sea automatico
//setInterval(function(){
//	siguiente();
//},5000);