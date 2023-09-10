export interface ReportData{
    user: string,
    experiment: string,
    data: [string, {base: any, carriage: any[]}][],
}

export interface Report{
    user: string,
    experiment: string,
    module: string,
    timestamp: string,
    running: boolean,
    datapoints: number,
}