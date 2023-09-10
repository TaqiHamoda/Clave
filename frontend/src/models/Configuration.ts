export interface ReportExperimentBoard{
    base: any;
    carriage: any;
}

export interface ConfigProperty{
    type: string;
    description: string;
    unit?: string;
    min?: number;
    max?: number;
    step?: number;
    value?: string;
    values?: any[];
    multiple?: boolean;
    independent?: boolean;
}

export interface Configuration{
    name: string;
    description: string,
    image: string,
    settings: Record<string, Record<string, ConfigProperty>>,
    report: ReportExperimentBoard,
    experiment: ReportExperimentBoard,
    state: Record<string, Record<string, ConfigProperty>>,
    commands: Record<string, Record<string, ConfigProperty>>,
}