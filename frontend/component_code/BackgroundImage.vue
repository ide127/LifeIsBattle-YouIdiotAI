<template>
	<div class="gradation-wrap">
		<img class="background-image" src="@/assets/imgs/neonCity.png" alt="" />
	</div>
</template>

<style>
.gradation-wrap {
	margin: 50px 0;
	position: relative;
	display: inline-block;
	width: 100%;
}
.background-image {
	width: 100%;
	height: 400px;
}
.gradation-wrap::before,
.gradation-wrap::after {
	content: "";
	position: absolute;
	left: 0;
	right: 0;
	z-index: 1;
}
.gradation-wrap::before {
	top: 0;
	height: 15%;
	background: linear-gradient(to bottom, black, transparent);
}
.gradation-wrap::after {
	bottom: 0;
	height: 20%;
	background: linear-gradient(to top, black, transparent);
}
</style>
