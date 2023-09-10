import { ConfigProperty } from "./Configuration";

export interface State{
    name: string,
    last_update: string,
    state: Record<string, Record<string, ConfigProperty>>
}
