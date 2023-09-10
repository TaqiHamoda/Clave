
interface CustomFetchArguments{
    uri: string;
    method?: string;
    data?: any;
    content_type?: string;
}

export async function customFetch({ uri, method, data, content_type}: CustomFetchArguments, upload_file: boolean = false): Promise<Response>{
    // Has credentials include for cookie support with CORS
    if((method == null) || (method.length == 0)){
        method = 'GET';
    }

    if((content_type == null) || (content_type.length == 0)){
        content_type = 'text/plain';
    }

    if(upload_file){
        return await fetch(uri, {
            method: method,
            credentials: 'include',
            body: data
        });
    }

    return await fetch(uri, {
        method: method,
        credentials: 'include',
        headers: {
            'Content-Type': content_type
        },
        body: JSON.stringify(data)
    });
}

export async function downloadFile(response: Response, filename: string): Promise<void>{
    const url = URL.createObjectURL(await response.blob());

    // Step 3: Trigger downloading the object using that URL
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click(); // triggering it manually
}
