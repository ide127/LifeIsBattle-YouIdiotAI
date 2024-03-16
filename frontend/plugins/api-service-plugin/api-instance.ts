import type { FetchContext, SearchParameters } from "ofetch";
import { isNaN, isNull, omitBy } from "lodash-es";

export type ApiHandler = (context: FetchContext) => Promise<void> | void;

export type ApiOptions = {
	server?: boolean;
	timeout?: number;
	headers?: Record<string, string>;
	retry?: number | false;
	responseType?: "blob" | "arrayBuffer" | "jason" | "stream" | "text";
};

type Rest = "get" | "post" | "put" | "patch" | "delete";

export class ApiInstance {
	private readonly onRequest: ApiHandler;
	private readonly onRequestError: ApiHandler;
	private readonly onResponse: ApiHandler;
	private readonly onResponseError: ApiHandler;
	private readonly timeOut: number;
	private readonly baseUrl: string | undefined;

	constructor(
		baseUrl: string | undefined,
		timeOut: number,
		onRequest: ApiHandler,
		onRequestError: ApiHandler,
		onResponse: ApiHandler,
		onResponseError: ApiHandler
	) {
		this.baseUrl = baseUrl;
		this.timeOut = timeOut;
		this.onRequest = onRequest;
		this.onRequestError = onRequestError;
		this.onResponse = onResponse;
		this.onResponseError = onResponseError;
	}

	getQueryParams(params?: SearchParameters) {
		if (!params) return undefined;

		return omitBy(params, (value: any) => isNull(value) || isNaN(value));
	}
	private getCsrfToken() {
		if (typeof document !== "undefined") {
			const cookieValue = document.cookie
				.split("; ")
				.find((row) => row.startsWith("csrftoken="));
			return cookieValue
				? decodeURIComponent(cookieValue.split("=")[1])
				: "";
		}
		return "";
	}
	public getOptions(
		method: Rest,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		let fetchOptions: any = {
			baseUrl: this.baseUrl,
			timeout: options?.timeout ?? this.timeOut,
			onRequest: this.onRequest,
			onRequestError: this.onRequestError,
			onResponse: this.onResponse,
			onResponseError: this.onResponseError,
			method: method,
			params: method === "get" ? this.getQueryParams(params) : undefined,
			body: method !== "get" ? params : undefined,
			retry: options?.retry ?? false,
			responseType: options?.responseType,
		};

		const headers: Record<string, string> = {
			// 'Content-Type': 'application/json; charset=UTF-8;',
			"X-CSRFToken": this.getCsrfToken(),
		};

		for (const key in options?.headers) {
			headers[key] = options.headers[key];
		}

		fetchOptions.headers = headers;

		return fetchOptions;
	}
}
