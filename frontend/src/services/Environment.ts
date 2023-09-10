export class ENV{
    public static readonly SERVER_ADDRESS: string = `${process.env.REACT_APP_SERVER_ADDRESS}:${process.env.REACT_APP_SERVER_PORT}`;

    public static readonly HOME_PATH: string = '/';
    public static readonly LOGIN_PATH: string = '/login';
    public static readonly ABOUT_PATH: string = '/about';
    public static readonly MODULE_PATH: string = '/module';
    public static readonly PROFILE_PATH: string = '/profile';
    public static readonly REPORTS_PATH: string = '/reports';
    public static readonly SETTINGS_PATH: string = '/settings';
    public static readonly EXPERIMENT_PATH: string = '/experiment';

    public static readonly LOGIN_API_PATH: string = `${ENV.SERVER_ADDRESS}/login`;
    public static readonly COMMAND_API_PATH: string = `${ENV.SERVER_ADDRESS}/devices`;
    public static readonly SERVER_API_PATH: string = `${ENV.SERVER_ADDRESS}/server`;
    
    public static readonly MODEL_USER_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/users`;
    public static readonly MODEL_STATE_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/states`;
    public static readonly MODEL_MODULE_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/modules`;
    public static readonly MODEL_DEVICE_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/devices`;
    public static readonly MODEL_CONFIG_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/configurations`;
    public static readonly MODEL_REPORT_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/reports`;
    public static readonly MODEL_EXPERIMENT_API_PATH: string = `${ENV.SERVER_ADDRESS}/info/experiments`;

    // Developer Parameter
    public static readonly STATUS_REFRESH_TIMEOUT: number = 1000;  // Wait one second for update to occur
    public static readonly STATUS_CHECKIN_TIMEOUT: number = 60000;  // Every 1 minute
}