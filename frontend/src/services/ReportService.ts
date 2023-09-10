import { Report, ReportData } from "../models/Report";

import { ENV } from './Environment';
import { customFetch, downloadFile } from "./CustomFetch";

export class ReportService{
    public static async getReport(reportId: string): Promise<Report | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_REPORT_API_PATH}/${reportId}`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getReportData(reportId: string): Promise<ReportData | null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_REPORT_API_PATH}/${reportId}/data`,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async getReports(): Promise<Report[] | null>{
        var response: Response = await customFetch({
            uri: ENV.MODEL_REPORT_API_PATH,
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        return await response.json();
    }

    public static async downloadReport(reportId: string): Promise<null>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_REPORT_API_PATH}/${reportId}/download`,
            content_type: 'application/zip'
        });

        if(!response.ok){
            console.log(`Error: ${await response.text()}`);
            return null;
        }

        await downloadFile(response, `${reportId}.zip`);
        return null;
    }

    public static async uploadReports(data: FormData): Promise<boolean>{
        var response: Response = await customFetch({
            uri: `${ENV.MODEL_REPORT_API_PATH}/upload`,
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
}