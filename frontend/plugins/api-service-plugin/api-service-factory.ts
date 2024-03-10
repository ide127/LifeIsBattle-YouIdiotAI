import type { ApiInstance } from "~/plugins/api-service-plugin/api-instance";
import { ChattingService } from '~/plugins/api-service-plugin/service/ChattingService';

export interface IApiServices {
  chattingService: ChattingService
}

export function makeApiService(instance: ApiInstance) {
  const apiService: IApiServices = {
  chattingService : new ChattingService(instance)
  };
  return apiService;
}
