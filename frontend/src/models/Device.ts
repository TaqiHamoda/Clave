import { ConfigProperty } from "./Configuration";

export interface Status{
    ready: boolean;
    running: boolean;
    issue: boolean;
    info: string;
    warning: string;
    error: string;
    carriages_count: number;
}

export interface Device{
    name: string;
    status?: Status;
    settings?: Record<string, Record<string, ConfigProperty>>;
}