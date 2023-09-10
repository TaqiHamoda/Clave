import { Experiment } from "../models/Experiment";

import { ENV } from './Environment';
import { customFetch } from "./CustomFetch";

export class ExperimentService{
    public static async getExperiment(experimentId: string): Promise<Experiment | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_EXPERIMENT_API_PATH}/${experimentId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getExperiments(): Promise<Experiment[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_EXPERIMENT_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }
}