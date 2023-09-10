import { Device } from '../models/Device';

import { ENV } from './Environment';
import { customFetch } from "./CustomFetch";

export class DeviceService{
    public static async getDevice(moduleId: string): Promise<Device | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_DEVICE_API_PATH}/${moduleId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getDevices(): Promise<Device[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_MODULE_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }
}