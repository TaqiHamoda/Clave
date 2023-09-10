import { customFetch } from "./CustomFetch";
import { ENV } from './Environment';

import { Configuration } from "../models/Configuration";


export class ConfigurationService{
    public static async getConfiguration(moduleId: string): Promise<Configuration | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_CONFIG_API_PATH}/${moduleId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getConfigurations(): Promise<Configuration[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_CONFIG_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }
}
