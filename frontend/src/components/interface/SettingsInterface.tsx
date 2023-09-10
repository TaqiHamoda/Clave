import {
    Box,
    BoxProps,
    Flex,
    Text,
    SimpleGrid,
    VStack,
    HStack,
    Button,
    useToast
  } from "@chakra-ui/react";
import { useEffect, useState } from "react";

import { ConfigurationFormData } from "../../components/ConfigurationFormData";

import { Commands } from "../../models/Commands";
import { Device } from "../../models/Device";
import { Configuration } from "../../models/Configuration";

import { CommandsService } from "../../services/CommandsService";

export interface SettingsInterfaceProps extends BoxProps{
    config?: Configuration,
    device?: Device
}

export const SettingsInterface = (props: SettingsInterfaceProps) => {
    const {config, device, ...rest} = props;
    const [loading, setLoading] = useState<boolean>(false);
    const toast = useToast();

    useEffect(() => {
        if (device == null || config == null) { return; }

        for(var [key, value] of Object.entries(config.settings)){
            for(var [k, v] of Object.entries(value)){
                var i = document.getElementById(`settings_${key}_${k}`) as any;
                i.value = (device.settings as any)[key][k];
            }
        }
    }, []);

    if (device == null || config == null || Object.keys(config.settings).length == 0) {
        return <></>;
    }

    const onSubmit = (e: any) => {
        e.preventDefault();

        setLoading(true);

        const new_settings: Record<string, Record<string, any>> = {};
        for(var [key, value] of Object.entries(config.settings)){
            new_settings[key] = {};

            for(var [k, v] of Object.entries(value)){
                var i = document.getElementById(`settings_${key}_${k}`) as any;
                new_settings[key][k] = i.value;
            }
        }

        CommandsService.runCommand(config.name, Commands.changeSettings, {"settings": new_settings}).then(result => {
            setLoading(false);

            var error: string;

            if (typeof result === 'string') {
                error = result;
            } else if (!result.success) {
                error = result.error;
            } else {
                toast({
                    title: 'Changed Settings Successfully',
                    description: "Changed the interface's settings successfully.",
                    status: 'info',
                    duration: 9000,
                    isClosable: true,
                });
                return;
            }

            toast({
                title: 'Issue Encountered',
                description: error,
                status: 'error',
                duration: 9000,
                isClosable: true,
            });
        });
    }

    return <Box {...rest}>
        <form onSubmit={onSubmit}>
            <SimpleGrid columns={[1, 2]} gap='20px' marginTop='10px'>
                {Object.keys(config.settings).map(key => {
                    return <VStack borderRadius='md' borderWidth='1px'>
                        <Flex flexDirection='row' width='full' padding='10px'>
                            <Text fontSize='lg'> {key} </Text>
                        </Flex>

                        <SimpleGrid columns={[1, 2]} spacing='40px' width='full' padding='15px'>
                            {Object.keys(config.settings[key]).map(k => {
                                return <ConfigurationFormData name={k} id={`settings_${key}_${k}`} config={config.settings[key][k]}/>;
                            })}
                        </SimpleGrid>
                    </VStack>;
                })}
            </SimpleGrid>

            <HStack justifyContent='center' marginTop='25px'>
                <Button colorScheme='blue' isLoading={loading} title='Change Interface Settings' aria-label='Change Interface Settings' type='submit'>
                    Change Interface Settings
                </Button>
            </HStack>
        </form>
    </Box>;
}