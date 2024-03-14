export default function ({ $axios, app }) {
	$axios.onRequest((config) => {
		const csrfToken = app.$cookies.get("csrftoken");
		if (csrfToken) {
			config.headers.common["X-CSRFToken"] = csrfToken;
		}
	});
}
