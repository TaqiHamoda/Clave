import { Module } from "../models/Module";
import { Image } from "../models/Image";

import { ENV } from './Environment';
import { customFetch, downloadFile } from "./CustomFetch";

export class ModuleService{
    public static async getModule(moduleId: string): Promise<Module | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_MODULE_API_PATH}/${moduleId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getModules(): Promise<Module[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_MODULE_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getImage(moduleId: string): Promise<Image | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_MODULE_API_PATH}/${moduleId}/image`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async downloadInterface(moduleId: string): Promise<null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_MODULE_API_PATH}/${moduleId}/download`,
            content_type: 'application/zip'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        await downloadFile(response, `${moduleId}.zip`);
        return null;
    }

    public static async installModule(data: FormData): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_MODULE_API_PATH}/install`,
            method: 'POST',
            data: data,
            content_type: 'multipart/form-data'
        }, true);

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }

    public static async uninstallModule(moduleId: string): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_MODULE_API_PATH}/${moduleId}/uninstall`,
            method: 'DELETE',
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }
}