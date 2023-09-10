import { ServerInfo, ServerStats } from '../models/ServerInfo';

import { ENV } from './Environment';
import { customFetch } from "./CustomFetch";

export class ServerService{
    public static async getInfo(): Promise<ServerInfo | null>{
        var response: Response = await customFetch({
            uri: `${ENV.SERVER_API_PATH}/info`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getResources(): Promise<ServerStats | null>{
        var response: Response = await customFetch({
            uri: `${ENV.SERVER_API_PATH}/resources`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }
}