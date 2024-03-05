import mitt, {type Emitter, type EventType } from 'mitt';
export type EventBus = Emitter<Record<EventType, any>>;

const eventBus: EventBus = mitt();
export default eventBus;

export const eventBusReloadWithLoading = async (...callback: (() => Promise<void>)[]) => {
  eventBus.emit('@showLoading');
  for (const cb of callback) {
    await cb();
  }
  eventBus.emit('@hideLoading');
};
