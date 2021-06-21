console.clear();
let am = 30;
let ptext = document.querySelector(".p-text");

document.addEventListener("click", (e) => {
	let xx = e.pageX;
	let yy = e.pageY;

	for (let i = 0; i < am; i++) {
		createCircles(xx, yy, i);
	}
});

function createCircles(x, y, tuSam) {
	let firefly = document.createElement("firefly");

	document.body.appendChild(firefly);

	let size = Math.floor(Math.random() * 5);

	firefly.style.width = `${size}px`;
	firefly.style.height = `${size}px`;

	let destinationX = x + (Math.random() - 0.5) * tuSam * 20;
	let destinationY = y + (Math.random() - 0.5) * tuSam * 20;

	let roate = (Math.random() + 1) * tuSam * 20;

	let animation = firefly.animate(
		[
			{
				transform: `translate3d(${x - tuSam}px, ${y - tuSam}px, 0)`,
				opacity: 1,
				filter: `hue-rotate(${0}deg`
			},
			{
				transform: `translate3d(${destinationX - size}px, ${
					destinationY - size
				}px, 0) rotateZ(${roate}deg)  translateX(${tuSam}px)`,
				opacity: 0.5
				// filter: `hue-rotate(${160}deg`
			},
			{
				transform: `translate3d(${destinationX}px, ${destinationY}px, 0) rotateZ(${roate}deg)  translateX(${
					tuSam * 30
				}px)`,
				opacity: 0
				//filter: `hue-rotate(${60}deg`
			}
		],
		{
			duration: 10 + Math.random() * 4000,
			easing: "ease-out",

			delay: Math.random() * 200
		}
	);

	animation.onfinish = () => {
		firefly.remove();
	};
}


