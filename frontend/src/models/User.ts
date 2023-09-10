export enum UserRole{
    admin = 0,
    user = 1,
}

export interface User {
    username: string;
    first_name?: string;
    last_name?: string;
    password?: string;
    role?: number;
}
