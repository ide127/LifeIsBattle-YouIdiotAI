import type {ApiHandler, ApiInstance} from './api-service-plugin/api-instance';
import { $error, ApiServiceError } from '~/plugins/api-service-plugin/api-error-handler';
import eventBus from "~/util/eventBus";

export default defineNuxtPlugin((app)=>{
    app.hooks.hook('app:error', (err)=>{
        console.log('app:error', err);
    })
    app.hooks.hook('vue:error', (err, _target, _info)=>{
        console.log(`vue:error`, err);
    })

    const onRequest: ApiHandler = (context) => {
        if (context.options?.headers) {
            context.options.headers = { ...context.options.headers};
        } else {
            context.options.headers = { };
        }
    };

    const onRequestError: ApiHandler = (_context) => {
        eventBus.emit('@hideLoading');
    };

    const onResponse: ApiHandler = (_context) => {
        eventBus.emit('@hideLoading');
    };

    const onResponseError: ApiHandler = (context) => {
        eventBus.emit('@hideLoading');
        const apiServiceError = new ApiServiceError(context.response?._data.errorCode, context.response?._data.errorMessage);
        console.error('api:error', apiServiceError);
        $error.runHandler(context.response?._data.errorCode, apiServiceError);
    };
})