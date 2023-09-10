import { customFetch } from "./CustomFetch";
import { ENV } from './Environment';

import { State } from "../models/State";

export class StateService{
    public static async getState(moduleId: string): Promise<State | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_STATE_API_PATH}/${moduleId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getStates(): Promise<State[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_STATE_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }
}
