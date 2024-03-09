import { ApiServiceBase } from '~/plugins/api-service-plugin/service/ApiServiceBase';
import { ApiInstance } from '~/plugins/api-service-plugin/api-instance';

export class ChattingService extends ApiServiceBase {
    constructor(instance: ApiInstance) {
        super(instance);
    }

    /**
     * session 생성
     */
    createSession(params: any) {
        return this.post<any>('/sessions/', params);
    }

    /**
     * chatting get
     */
    getChatting() {
        return this.get<any>('/leaderboard');
    }
}
