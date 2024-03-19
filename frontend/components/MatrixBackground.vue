<template>
	<div>
		<canvas ref="canvasRef"></canvas>
	</div>
</template>

<script>
export default {
	name: "MatrixBackground",
	data() {
		return {
			canvas: null,
			ctx: null,
			font_size: 10,
			matrix: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}".split(
				""
			),
			drops: [],
		};
	},
	mounted() {
		this.initializeCanvas();
		this.interval = setInterval(this.draw, 35);
	},
	methods: {
		initializeCanvas() {
			this.canvas = this.$refs.canvasRef;
			this.ctx = this.canvas.getContext("2d");
			this.canvas.height = this.canvas.offsetHeight;
			this.canvas.width = this.canvas.offsetWidth;
			var columns = this.canvas.width / this.font_size;
			for (var x = 0; x < columns; x++) this.drops[x] = 1;
		},
		draw() {
			this.ctx.fillStyle = "rgba(0, 0, 0, 0.04)";
			this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
			this.ctx.fillStyle = "#158d51";
			this.ctx.font = this.font_size + "px arial";
			for (var i = 0; i < this.drops.length; i++) {
				var text =
					this.matrix[Math.floor(Math.random() * this.matrix.length)];
				this.ctx.fillText(
					text,
					i * this.font_size,
					this.drops[i] * this.font_size
				);
				if (
					this.drops[i] * this.font_size > this.canvas.height &&
					Math.random() > 0.975
				)
					this.drops[i] = 0;
				this.drops[i]++;
			}
		},
	},
	beforeDestroy() {
		clearInterval(this.interval);
	},
};
</script>

<style>
* {
	margin: 0;
	padding: 0;
}

body {
	background: black;
}
canvas {
	display: block;
}
</style>
