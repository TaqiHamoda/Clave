import { ENV } from "./Environment";
import { customFetch } from "./CustomFetch";

import { User } from "../models/User";

export class AuthService{
    public static async login(user: User): Promise<User | null>{
        const result: User | null = await this.getLoggedInUser();

        if(result != null){
            return result
        }

        // If not logged in, log in
        var response: Response = await customFetch({
            uri: ENV.LOGIN_API_PATH,
            method: 'POST',
            data: user,
            content_type: 'application/json',
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await this.getLoggedInUser();
    }

    public static async logout(): Promise<boolean>{
        var response: Response = await customFetch({
            uri: ENV.LOGIN_API_PATH,
            method: 'DELETE'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return false;
        }

        return true;
    }

    public static async getLoggedInUser(): Promise<User | null>{
        // Check if user is already logged in
        var response: Response = await customFetch({
            uri: ENV.LOGIN_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        var info = await response.json();
        if(info.logged_in){
            return info.user;
        }

        return null;
    }
}