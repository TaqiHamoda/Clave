import { ReportExperimentBoard } from "./Configuration";

export interface Experiment{
    name: string;
    user: string;
    module: string;
    timestamp: string;
    parameters: ReportExperimentBoard;
}