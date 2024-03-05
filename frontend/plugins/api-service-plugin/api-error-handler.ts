import mitt, {type Emitter } from 'mitt';

export type ErrorHandler = (error: any) => void;

export class ApiServiceError {
  get errorMessage(): string {
    return this._errorMessage;
  }
  get errorCode(): string {
    return this._errorCode;
  }
  private readonly _errorCode: string;
  private readonly _errorMessage: string;
  constructor(errorCode: string, errorMessage: string) {
    this._errorCode = errorCode;
    this._errorMessage = errorMessage;
  }

  toString() {
    return `errorCode:${this._errorCode}, errorMessage:${this._errorMessage}`;
  }
}

export class ApiErrorHandler {
  private _mit: Emitter<any>;

  constructor() {
    this._mit = mitt();
  }

  public runHandler(errorCode: string, params: any) {
    this._mit.emit(errorCode, params);
  }

  public addApiErrorHandler(errorCode: string, handler: ErrorHandler = $apiErrorHandler) {
    this._mit.on(errorCode, handler);
  }

  public removeApiErrorHandler(errorCode: string, handler: ErrorHandler) {
    this._mit.off(errorCode, handler);
  }
}

function $apiErrorHandler(apiServiceError: any) {
  console.log("apiServiceError.errorMessage: ", apiServiceError.errorMessage);
}

export const $error = new ApiErrorHandler();
