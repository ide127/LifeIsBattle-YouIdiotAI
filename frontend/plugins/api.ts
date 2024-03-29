import { ApiHandler, ApiInstance } from "./api-service-plugin/api-instance";
import {
	$error,
	ApiServiceError,
} from "~/plugins/api-service-plugin/api-error-handler";
import eventBus from "~/util/eventBus";
import { makeApiService } from "~/plugins/api-service-plugin/api-service-factory";

export default defineNuxtPlugin((app) => {
	app.hooks.hook("app:error", (err) => {
		console.log("app:error", err);
	});
	app.hooks.hook("vue:error", (err, _target, _info) => {
		console.log(`vue:error`, err);
	});

	const onRequest: ApiHandler = (context) => {
		if (context.options?.headers) {
			context.options.headers = { ...context.options.headers };
		} else {
			context.options.headers = {};
		}
	};

	const onRequestError: ApiHandler = (_context) => {
		eventBus.emit("@hideLoading");
	};

	const onResponse: ApiHandler = (_context) => {
		eventBus.emit("@hideLoading");
	};

	const onResponseError: ApiHandler = (context) => {
		eventBus.emit("@hideLoading");
		const apiServiceError = new ApiServiceError(
			context.response?._data.errorCode,
			context.response?._data.errorMessage
		);
		console.error("api:error", apiServiceError);
		$error.runHandler(context.response?._data.errorCode, apiServiceError);
	};

	const baseUrl = "https://lifeisbattle.com/server/api/game";
	// const baseUrl = "http://localhost:8000/server/api/game";

	const api = new ApiInstance(
		baseUrl,
		20000,
		onRequest,
		onRequestError,
		onResponse,
		onResponseError
	);

	const apiService = makeApiService(api);

	return {
		provide: {
			error: $error,
			api: apiService,
		},
	};
});
