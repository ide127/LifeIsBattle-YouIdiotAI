import { SearchParameters } from "ofetch/dist/node";
import type {
	ApiInstance,
	ApiOptions,
} from "~/plugins/api-service-plugin/api-instance";

export class ApiServiceBase {
	protected _instance: ApiInstance;

	constructor(instance: ApiInstance) {
		this._instance = instance;
	}

	protected async get<T>(
		api: string,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		const fetchOptions = this._instance.getOptions("get", params, options);
		return $fetch<T>(fetchOptions.baseUrl + api, fetchOptions).then(
			(response) => {
				return response;
			}
		);
	}

	protected async post<T>(
		api: string,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		const fetchOptions = this._instance.getOptions(
			"post",
			params ?? {},
			options
		);
		return $fetch<T>(fetchOptions.baseUrl + api, fetchOptions).then(
			(response) => {
				return response;
			}
		);
	}

	protected async put<T>(
		api: string,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		const fetchOptions = this._instance.getOptions(
			"put",
			params ?? {},
			options
		);
		return $fetch<T>(fetchOptions.baseUrl + api, fetchOptions).then(
			(response) => {
				return response;
			}
		);
	}

	protected async delete<T>(
		api: string,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		const fetchOptions = this._instance.getOptions(
			"delete",
			params ?? {},
			options
		);
		return $fetch<T>(fetchOptions.baseUrl + api, fetchOptions).then(
			(response) => {
				return response;
			}
		);
	}

	protected async patch<T>(
		api: string,
		params?: SearchParameters,
		options?: ApiOptions
	) {
		api = api + (params?.id ? `${params.id}/` : "");
		const fetchOptions = this._instance.getOptions(
			"patch",
			params ?? {},
			options
		);
		// debug api, params, options, fetchOptions
		alert(
			"api: " +
				api +
				" params: " +
				JSON.stringify(params) +
				" options: " +
				JSON.stringify(options) +
				" fetchOptions: " +
				JSON.stringify(fetchOptions)
		);
		return $fetch<T>(fetchOptions.baseUrl + api, fetchOptions).then(
			(response) => {
				return response;
			}
		);
	}

	protected buildJsonBlob(jsonObj: any) {
		const json = JSON.stringify(jsonObj);
		return new Blob([json], {
			type: "application/json",
		});
	}
}
