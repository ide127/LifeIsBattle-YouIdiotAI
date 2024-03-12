import { ApiServiceBase } from "~/plugins/api-service-plugin/service/ApiServiceBase";
import { ApiInstance } from "~/plugins/api-service-plugin/api-instance";

export class ChattingService extends ApiServiceBase {
	constructor(instance: ApiInstance) {
		super(instance);
	}

	/**
	 * create session
	 */
	createSession(params: any) {
		return this.post<any>("/sessions/", params);
	}

	patchSession(params: any) {
		return this.patch<any>("/sessions/", params);
	}

	// create message
	createMessage(params: any) {
		return this.post<any>("/messages/", params);
	}

	// create leaderboard
	createLeaderboard(params: any) {
		return this.post<any>("/leaderboard/", params);
	}

	// get leaderboard_list
	getLeaderboardList(params: any) {
		return this.get<any>("/leaderboard/", params);
	}

	getScore(params: any) {
		return this.post<any>("/calc_score/", params);
	}
}
