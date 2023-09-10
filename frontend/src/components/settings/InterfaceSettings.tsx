import {
    Box,
    BoxProps,
    SimpleGrid,
    Button,
    Flex,
    useToast
} from "@chakra-ui/react"  
import { useEffect, useState } from "react";
import { CloudUploadFill, TrashFill } from "react-bootstrap-icons";

import { AlertPopupButton } from "../AlertPopupButton";
import { FileUploadButton } from "../FileUploadButton";
import { Module } from "../../models/Module";
import { ModuleService } from "../../services/ModuleService";

export const InterfaceSettings = (props: BoxProps) => {
    const toast = useToast();
    const [modules, setModules] = useState<Module[]>([]);
    const [uploading, setUploading] = useState<boolean>(false);

    useEffect(() => {
        ModuleService.getModules().then(m => setModules(m != null ? m : []));
    }, []);

    const onImport = (files: FileList | null | undefined) => {
        if(files == null || files.length == 0) { return; }

        setUploading(true);

        const formData = new FormData();

        Array.from(files).forEach(file => {
            formData.append(file.name, file);
        });

        ModuleService.installModule(formData).then(result => {
            setUploading(false);

            if(result){
                toast({
                    title: 'Module Installed Successfully',
                    description: 'The module has been installed successfully. Please refresh the homepage.',
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            } else{
                toast({
                    title: 'Issue Encountered',
                    description: 'An error was encountered while installing the module. Please ensure there are no duplicates and that the zip file is properly configured.',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    }

    return <Box {...props}>
        <Flex flexDirection='row-reverse'>
            <FileUploadButton
            aria-label="Install Modules"
            title="Install Modules"
            colorScheme='green'
            variant='outline'
            multiple
            accept=".zip"
            leftIcon={ <CloudUploadFill/> }
            isLoading={uploading}
            onClick={onImport}>
                Install Modules
            </FileUploadButton>
        </Flex>
        
        <SimpleGrid columns={[1, 2, 4, 5]} gap='20px' marginTop='10px'>
            {modules.map(m => <InterfaceSettingsCard module={m}/>)}
        </SimpleGrid>
    </Box>;
}

const InterfaceSettingsCard = ( {module}: {module: Module} ) => {
    const toast = useToast();

    const uninstallInterface = (e: any) => {
        e.preventDefault();

        ModuleService.uninstallModule(module.name).then(v => {
            if(v == true){
                toast({
                    title: 'Module Uninstalled Successfully',
                    description: 'The module has been uninstalled successfully. Good riddance.',
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
            }else{
                toast({
                    title: 'Issue Encountered',
                    description: 'An error was encountered while uninstalling the module. Check the logs for more information.',
                    status: 'error',
                    duration: 9000,
                    isClosable: true,
                });
            }
        });
    }

    return <AlertPopupButton
        text='Delete Interface'
        header='Delete Interface'
        body="Are you sure? You can't undo this action afterwards."
        aria-label={`Delete Interface ${module.name}`}
        leftIcon={<TrashFill />}
        title={`Delete Interface ${module.name}`}
        colorScheme='red'
        variant='outline'
        onClick={uninstallInterface}
    >
        {module.name}
    </AlertPopupButton>;
}