import { ENV } from "./Environment";
import { customFetch } from "./CustomFetch";

import { ModuleResponse } from "../models/ModuleResponse";
import { Commands } from "../models/Commands";

export class CommandsService{
    public static async runCommand(moduleId: string, command: Commands, data: any): Promise<string | ModuleResponse>{
        var response: Response = await customFetch({
            uri: `${ENV.COMMAND_API_PATH}/${moduleId}/${command}`,
            method: 'POST',
            data: data,
            content_type: 'application/json',
        });

        if(!response.ok){
            const error = await response.text();
            
            console.log(`Error: ${error}`);
            return error;
        }

        return await response.json();
    }
}