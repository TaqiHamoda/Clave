import { ENV } from "./Environment";
import { customFetch } from "./CustomFetch";

import { User } from "../models/User";

export class UserService{
    public static async getUser(username: string): Promise<User | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_USER_API_PATH}/${username}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getUsers(): Promise<User[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_USER_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async updateUser(username: string, user: User): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_USER_API_PATH}/${username}`,
            method: 'POST',
            data: user,
            content_type: 'application/json'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }

    public static async createUser(user: User): Promise<boolean>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_USER_API_PATH,
            method: 'PUT',
            data: user,
            content_type: 'application/json'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }

    public static async deleteUser(username: string): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_USER_API_PATH}/${username}`,
            method: 'DELETE',
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }

    public static async changePassword(username: string, new_password: string): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_USER_API_PATH}/${username}/password`,
            method: 'POST',
            data: { password: new_password },
            content_type: 'application/json'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }
}