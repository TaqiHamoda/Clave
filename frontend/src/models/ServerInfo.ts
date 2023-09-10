export interface ServerInfo{
    version: string,
    server: {
        system: string,  // e.g. Windows, Linux, Darwin
        architecture: string,  // e.g. 64-bit
        machine: string,  // e.g. x86_64
        hostname: string,  // Hostname
    }
}

export interface ServerStats{
    cpu_percent: number,
    memory_free: number,
    memory_total: number,
    disk_free: number,
    disk_total: number,
}